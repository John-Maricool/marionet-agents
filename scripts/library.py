"""Shared loaders for the agent library."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.S)


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def split_frontmatter(text: str) -> tuple[dict, str]:
    m = FRONTMATTER.match(text)
    if not m:
        raise ValueError("missing YAML frontmatter (file must start with ---)")
    meta = yaml.safe_load(m.group(1)) or {}
    if not isinstance(meta, dict):
        raise ValueError("frontmatter must be a mapping")
    return meta, m.group(2)


@dataclass
class Agent:
    path: Path
    team_dir: str
    folder: str
    meta: dict
    body: str

    @property
    def name(self) -> str:
        return self.meta.get("name", "")

    @property
    def evals_path(self) -> Path:
        return self.path.parent / "evals" / "tasks.yaml"


@dataclass
class Library:
    schema: dict
    models: dict
    capabilities: dict
    contracts: dict
    skills: dict
    agents: list[Agent] = field(default_factory=list)
    teams: dict = field(default_factory=dict)
    load_errors: list[str] = field(default_factory=list)


def load_library(root: Path = ROOT) -> Library:
    lib = Library(
        schema=load_yaml(root / "schema" / "agent.schema.yaml"),
        models=load_yaml(root / "models.yaml"),
        capabilities=load_yaml(root / "capabilities.yaml").get("capabilities", {}),
        contracts={p.stem: load_yaml(p) for p in sorted((root / "contracts").glob("*.yaml"))},
        skills={},
    )
    for skill_md in sorted((root / "skills").glob("*/SKILL.md")):
        try:
            meta, body = split_frontmatter(skill_md.read_text(encoding="utf-8"))
            lib.skills[skill_md.parent.name] = (meta, body, skill_md.parent)
        except (ValueError, yaml.YAMLError) as e:
            lib.load_errors.append(f"{skill_md.relative_to(root)}: {e}")
    for team_dir in sorted(p for p in (root / "agents").iterdir() if p.is_dir()):
        team_file = team_dir / "team.yaml"
        if team_file.exists():
            try:
                lib.teams[team_dir.name] = load_yaml(team_file)
            except yaml.YAMLError as e:
                lib.load_errors.append(f"{team_file.relative_to(root)}: not valid YAML: {str(e).splitlines()[-1].strip()}")
        for agent_md in sorted(team_dir.glob("*/agent.md")):
            try:
                meta, body = split_frontmatter(agent_md.read_text(encoding="utf-8"))
                lib.agents.append(Agent(agent_md, team_dir.name, agent_md.parent.name, meta, body))
            except (ValueError, yaml.YAMLError) as e:
                lib.load_errors.append(f"{agent_md.relative_to(root)}: {e}")
    return lib
