from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DeploymentScriptTests(unittest.TestCase):
    def test_package_deploy_script_preserves_data_and_restarts_service(self) -> None:
        script_path = ROOT / "scripts" / "deploy_package.sh"
        self.assertTrue(script_path.exists(), script_path)
        script = script_path.read_text(encoding="utf-8")
        raw_script = script_path.read_bytes()

        self.assertTrue(script.startswith("#!/usr/bin/env bash"))
        self.assertNotIn(b"\r\n", raw_script)
        self.assertIn('DEFAULT_TARGET="/opt/idle-game"', script)
        self.assertIn('DEFAULT_SERVICE="idle-game"', script)
        self.assertIn("systemctl stop", script)
        self.assertIn("systemctl start", script)
        self.assertIn("--exclude '/data/'", script)
        self.assertIn("tar -xzf", script)
        self.assertIn("unzip -q", script)
        self.assertNotIn("rm -rf \"$TARGET\"", script)

    def test_shell_scripts_are_archived_with_lf_line_endings(self) -> None:
        attributes = (ROOT / ".gitattributes").read_text(encoding="utf-8")

        self.assertIn("*.sh text eol=lf", attributes)

    def test_deployment_docs_reference_package_script(self) -> None:
        docs = (ROOT / "docs" / "deployment.md").read_text(encoding="utf-8")

        self.assertIn("scripts/deploy_package.sh", docs)
        self.assertIn("sudo /opt/idle-game/scripts/deploy_package.sh", docs)
        self.assertIn("preserves `/opt/idle-game/data`", docs)
