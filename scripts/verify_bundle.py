#!/usr/bin/env python3
"""Install in isolated roots; check skill loading, persona and core tool binding.

Run from a compatible protoAgent checkout, passing this bundle's committed repo.
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path


def main(source: str) -> None:
    sys.path.insert(0, str(Path.cwd()))
    with tempfile.TemporaryDirectory(prefix="writer-bundle-") as temp:
        root = Path(temp)
        os.environ.update(
            PROTOAGENT_BOX_ROOT=str(root / "box"),
            PROTOAGENT_HOME=str(root / "instance"),
            PROTOAGENT_PLUGINS_DIR=str(root / "plugins"),
            PROTOAGENT_PLUGINS_LOCK=str(root / "plugins.lock"),
        )
        import yaml
        from graph.config import LangGraphConfig
        from graph.plugins import installer
        from graph.plugins.loader import load_plugins
        from graph.skills.loader import parse_skill_md
        from graph.workspaces.manager import apply_bundle_config_inputs, register_project_inputs
        from tools.fs_tools import build_fs_tools
        from tools.onboard_tools import build_onboard_tools

        summary = installer.install(str(Path(source).resolve()))
        assert summary["skipped_builtin"] == ["technical_writer"], summary
        config = summary["config"]
        config["plugins"] = {"enabled": summary["enabled"], "plugins_dir": str(root / "plugins")}
        # Model a supplied managed checkout without touching the operator's projects.
        project = root / "project"
        project.mkdir()
        path = root / "config.yaml"
        path.write_text(yaml.safe_dump(config), encoding="utf-8")
        lock = root / "plugins.lock"
        written = apply_bundle_config_inputs(path, lock, {"technical_writer.project": str(project)})
        assert written == ["technical_writer.project"], written
        assert register_project_inputs(path, lock) == [str(project)]
        assert yaml.safe_load(path.read_text())["projects"][0]["write"] is True
        cfg = LangGraphConfig.from_yaml(str(path))
        loaded = load_plugins(cfg)
        meta = next(m for m in loaded.meta if m["id"] == "technical_writer")
        assert meta["loaded"], meta
        skills = [parse_skill_md(p) for directory in loaded.skill_dirs
                  if Path(directory).parent.name == "technical_writer"
                  for p in Path(directory).glob("*/SKILL.md")]
        assert len(skills) == 6 and all(s and s.prompt_template and not s.user_only for s in skills)
        preset = Path("config/soul-presets/technical-writer.md").read_text(encoding="utf-8")
        assert all(f"`{s.name}`" in preset for s in skills)
        names = {t.name for t in build_fs_tools(cfg) + build_onboard_tools(cfg)}
        expected = {"read_file", "write_file", "edit_file", "search_files", "find_files",
                    "list_projects", "run_command", "onboard_project", "register_local_project"}
        assert expected <= names, expected - names
        assert cfg.filesystem_run_requires_approval
        print("PASS: installed bundle, loaded six retrievable skills and persona, bound core tools for a sample project")
        print("Not exercised: model behavior, native UI, authenticated shipping, media capture/playback")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_bundle.py /path/to/committed/bundle")
    main(sys.argv[1])
