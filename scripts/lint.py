"""Validate agents, teams, skills, contracts and evals. Exit 1 on any error."""
from __future__ import annotations

import re
import sys

import yaml

from library import ROOT, load_library, load_yaml

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
GRADER_TYPES = {"contract", "rubric", "command", "contains", "not_contains"}
MIN_TASKS_DRAFT = 3
MIN_TASKS_VERIFIED = 10


def main() -> int:
    lib = load_library()
    errors: list[str] = list(lib.load_errors)
    warnings: list[str] = []

    allowed = set(lib.schema["fields"])
    required = set(lib.schema["required"])
    sections = lib.schema["required_sections"]
    tiers = set(lib.models.get("tiers", {}))
    names = [a.name for a in lib.agents]
    by_name = {a.name: a for a in lib.agents}

    # Skills
    for folder, (meta, body, _) in lib.skills.items():
        where = f"skills/{folder}"
        if meta.get("name") != folder:
            errors.append(f"{where}: name '{meta.get('name')}' must match folder")
        if not KEBAB.match(folder) or len(folder) > 64:
            errors.append(f"{where}: name must be kebab-case, max 64 chars")
        desc = meta.get("description", "")
        if not desc or len(desc) > 1024:
            errors.append(f"{where}: description required, max 1024 chars")

    # Agents
    for name in {n for n in names if names.count(n) > 1}:
        errors.append(f"duplicate agent name: {name}")

    for a in lib.agents:
        where = str(a.path.relative_to(ROOT))
        m = a.meta
        err = lambda msg: errors.append(f"{where}: {msg}")  # noqa: E731

        for key in sorted(set(m) - allowed):
            err(f"unknown field '{key}' (allowed: {', '.join(sorted(allowed))})")
        for key in sorted(required - set(m)):
            err(f"missing required field '{key}'")

        if a.name != a.folder:
            err(f"name '{a.name}' must match folder '{a.folder}'")
        if not KEBAB.match(a.name or ""):
            err("name must be kebab-case")
        if m.get("team") != a.team_dir:
            err(f"team '{m.get('team')}' must match folder '{a.team_dir}'")
        if m.get("role", "member") not in {"lead", "member"}:
            err("role must be lead or member")
        if not SEMVER.match(str(m.get("version", ""))):
            err("version must be semver, e.g. 0.1.0")
        if m.get("status") not in {"draft", "verified"}:
            err("status must be draft or verified")
        if m.get("model") not in tiers:
            err(f"model must be one of {sorted(tiers)}")

        desc = str(m.get("description", ""))
        if "Not for:" not in desc:
            err("description must include a 'Not for:' line")
        if len(desc) > 1024:
            err("description longer than 1024 chars")

        caps = m.get("capabilities") or []
        for c in caps:
            if c not in lib.capabilities:
                err(f"unknown capability '{c}'")
        tier = m.get("approval_tier")
        if not isinstance(tier, int) or not 0 <= tier <= 4:
            err("approval_tier must be an integer 0-4")
        else:
            if tier == 0 and ({"edit_files", "run_shell"} & set(caps)):
                err("approval_tier 0 (read-only) cannot have edit_files or run_shell")
            if "run_shell" in caps and tier < 2:
                err("run_shell needs approval_tier 2 or higher")
        if "delegate" in caps and m.get("role") != "lead":
            err("only team leads may have the delegate capability")

        for s in m.get("skills") or []:
            if s not in lib.skills:
                err(f"unknown skill '{s}'")
        for key in ("inputs", "outputs"):
            for c in m.get(key) or []:
                if c not in lib.contracts:
                    err(f"{key}: unknown contract '{c}'")
        for h in m.get("handoffs") or []:
            if h not in by_name:
                err(f"handoffs: unknown agent '{h}'")

        headings = {h.strip().lower() for h in re.findall(r"^#+\s+(.+)$", a.body, re.M)}
        for s in sections:
            if s.lower() not in headings:
                err(f"missing section '# {s}'")

        # Evals
        if not a.evals_path.exists():
            err("missing evals/tasks.yaml")
            continue
        try:
            ev = load_yaml(a.evals_path)
        except yaml.YAMLError as e:
            err(f"evals/tasks.yaml is not valid YAML: {str(e).splitlines()[-1].strip()}")
            continue
        tasks = ev.get("tasks") or []
        need = MIN_TASKS_VERIFIED if m.get("status") == "verified" else MIN_TASKS_DRAFT
        if len(tasks) < need:
            err(f"evals: {len(tasks)} tasks, need at least {need} for status '{m.get('status')}'")
        ids = [t.get("id") for t in tasks]
        for dup in {i for i in ids if ids.count(i) > 1}:
            err(f"evals: duplicate task id '{dup}'")
        for t in tasks:
            tid = t.get("id", "?")
            if not t.get("input"):
                err(f"evals/{tid}: missing input")
            for fx in t.get("fixtures") or []:
                if not (a.evals_path.parent / fx).exists():
                    err(f"evals/{tid}: fixture not found '{fx}'")
            graders = t.get("graders") or []
            if not graders:
                err(f"evals/{tid}: needs at least one grader")
            for g in graders:
                if g.get("type") not in GRADER_TYPES:
                    err(f"evals/{tid}: unknown grader type '{g.get('type')}'")
                if g.get("type") == "contract" and g.get("contract") not in lib.contracts:
                    err(f"evals/{tid}: unknown contract '{g.get('contract')}'")
            if graders and all(g.get("type") == "rubric" for g in graders):
                warnings.append(f"{where}: evals/{tid} uses only AI-judged rubrics; add a code check if possible")

    # Teams
    for team, t in lib.teams.items():
        where = f"agents/{team}/team.yaml"
        members = t.get("members") or []
        lead = t.get("lead")
        if lead not in members:
            errors.append(f"{where}: lead '{lead}' must be in members")
        if lead in by_name and by_name[lead].meta.get("role") != "lead":
            errors.append(f"{where}: lead '{lead}' must have role: lead")
        for mem in members:
            if mem not in by_name:
                errors.append(f"{where}: unknown member '{mem}'")
            elif by_name[mem].team_dir != team:
                errors.append(f"{where}: member '{mem}' belongs to team '{by_name[mem].team_dir}'")
        for r in t.get("routes") or []:
            if r.get("to") not in members:
                errors.append(f"{where}: route to '{r.get('to')}' is not a member")
    for a in lib.agents:
        t = lib.teams.get(a.team_dir)
        if t is None:
            errors.append(f"agents/{a.team_dir}: missing team.yaml")
        elif a.name not in (t.get("members") or []):
            errors.append(f"agents/{a.team_dir}/team.yaml: agent '{a.name}' is not listed in members")

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    status = "FAILED" if errors else "OK"
    print(f"\n{status}: {len(lib.agents)} agents, {len(lib.teams)} teams, "
          f"{len(lib.skills)} skills, {len(lib.contracts)} contracts, "
          f"{len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
