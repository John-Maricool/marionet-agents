"""Install marionet-agents into your AI tool.

Examples:
  python scripts/install.py --list
  python scripts/install.py --tool claude-code                       # all agents into this folder's project
  python scripts/install.py --tool claude-code --global              # all agents for every project (~/.claude)
  python scripts/install.py --tool cursor --team engineering,security --dest ~/code/my-app
  python scripts/install.py --tool gemini-cli --agent senior-mobile-engineer,senior-backend-engineer
  python scripts/install.py --tool prompts --dest ~/marionet-prompts  # plain system prompts for any chat app or API
  python scripts/install.py --tool codex --team engineering --dry-run

Install never deletes files. It adds or overwrites only the agent and skill files it writes.
"""
from __future__ import annotations

import argparse
import sys
import tempfile
from dataclasses import replace
from pathlib import Path

from convert import TARGETS
from library import load_library

GLOBAL_OK = {"claude-code", "cursor", "gemini-cli", "codex"}


def pick(lib, teams: list[str], agents: list[str]):
    chosen = lib.agents
    if teams:
        unknown = sorted(set(teams) - set(lib.teams))
        if unknown:
            sys.exit(f"unknown team(s): {', '.join(unknown)}. Run with --list.")
        chosen = [a for a in chosen if a.team_dir in teams]
    if agents:
        names = {a.name for a in lib.agents}
        unknown = sorted(set(agents) - names)
        if unknown:
            sys.exit(f"unknown agent(s): {', '.join(unknown)}. Run with --list.")
        chosen = [a for a in lib.agents if a.name in agents] if not teams else [a for a in chosen if a.name in agents]
    used_skills = {s for a in chosen for s in (a.meta.get("skills") or [])}
    return replace(lib, agents=chosen, skills={k: v for k, v in lib.skills.items() if k in used_skills})


def print_list(lib) -> None:
    order = ["leadership"] + sorted(t for t in lib.teams if t != "leadership")
    for team in order:
        members = [a for a in lib.agents if a.team_dir == team]
        lead = lib.teams[team]["lead"]
        print(f"\n{team} ({len(members)})")
        for a in sorted(members, key=lambda a: (a.name != lead, a.name)):
            print(f"  {a.name}{'  (lead)' if a.name == lead else ''}")
    print(f"\n{len(lib.agents)} agents. Tools: {', '.join(TARGETS)}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--tool", choices=list(TARGETS), help="which tool to install for")
    p.add_argument("--team", default="", help="comma-separated teams (default: all)")
    p.add_argument("--agent", default="", help="comma-separated agent names (default: all in the chosen teams)")
    p.add_argument("--dest", default=".", help="project folder to install into (default: current folder)")
    p.add_argument("--global", dest="global_", action="store_true", help="install into your home folder for all projects")
    p.add_argument("--dry-run", action="store_true", help="show what would be written, write nothing")
    p.add_argument("--list", action="store_true", help="list teams and agents")
    args = p.parse_args()

    lib = load_library()
    if lib.load_errors:
        print("\n".join(lib.load_errors))
        return 1
    if args.list:
        print_list(lib)
        return 0
    if not args.tool:
        p.error("--tool is required (or use --list)")

    if args.global_ and args.tool not in GLOBAL_OK:
        p.error(f"--global is not available for {args.tool}; use --dest")
    dest = Path.home() if args.global_ else Path(args.dest).expanduser().resolve()
    if not args.global_ and args.tool != "prompts" and not dest.is_dir():
        p.error(f"--dest folder does not exist: {dest}")

    split = lambda s: [x.strip() for x in s.split(",") if x.strip()]  # noqa: E731
    sub = pick(lib, split(args.team), split(args.agent))
    if not sub.agents:
        p.error("no agents selected")

    warnings: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        staged = Path(tmp)
        TARGETS[args.tool](sub, staged, warnings.append)
        files = sorted(f for f in staged.rglob("*") if f.is_file())
        for f in files:
            target = dest / f.relative_to(staged)
            if args.dry_run:
                print(f"would write {target}")
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(f.read_bytes())

    verb = "Would install" if args.dry_run else "Installed"
    print(f"{verb} {len(sub.agents)} agents and {len(sub.skills)} skills for {args.tool} into {dest}")
    for w in warnings:
        print(f"note: {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
