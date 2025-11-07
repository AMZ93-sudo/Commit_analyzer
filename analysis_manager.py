"""Upper-level manager script for configuring and running commit analysis."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "analysis_config.json"
BATCH_SCRIPT_PATH = BASE_DIR / "run_automation.bat"


def run_command(command: list[str], cwd: Optional[str] = None) -> subprocess.CompletedProcess[str]:
    """Executes a command and raises a descriptive error on failure."""
    try:
        return subprocess.run(
            command,
            check=True,
            text=True,
            capture_output=True,
            cwd=cwd,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"Command '{' '.join(command)}' failed with exit code {exc.returncode}: {exc.stderr.strip()}"
        ) from exc


def run_batch_script(batch_path: Path) -> None:
    """Launches the run_automation.bat workflow through cmd.exe."""
    if not batch_path.exists():
        raise FileNotFoundError(f"Automation script not found: {batch_path}")

    try:
        subprocess.run([
            "cmd.exe",
            "/c",
            str(batch_path),
        ], check=True)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"Automation batch failed with exit code {exc.returncode}. Check batch_log.txt for details."
        ) from exc


def validate_repo(repo_path: Path) -> None:
    """Ensures the repository path exists and contains a .git directory."""
    if not repo_path.exists():
        raise FileNotFoundError(f"Repository path does not exist: {repo_path}")
    if not repo_path.is_dir():
        raise NotADirectoryError(f"Repository path is not a directory: {repo_path}")
    if not (repo_path / ".git").exists():
        raise FileNotFoundError(f"No .git directory found in: {repo_path}")


def validate_commit(repo_path: Path, commit_ref: str) -> None:
    """Ensures the commit reference resolves to an actual commit."""
    run_command(["git", "-C", str(repo_path), "rev-parse", "--verify", f"{commit_ref}^{{commit}}"])


def write_config(repo_path: Path, commit1: str, commit2: str, config_path: Path) -> None:
    """Writes the JSON configuration consumed by commit_analyzer.py."""
    payload = {
        "repo_path": str(repo_path),
        "commit1": commit1,
        "commit2": commit2,
    }
    config_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Configure repository/commit inputs for the Gemini commit analyzer pipeline.",
    )
    parser.add_argument("--repo", required=True, help="Absolute path to the target git repository")
    parser.add_argument("--commit1", required=True, help="Baseline (older) commit hash or ref")
    parser.add_argument("--commit2", required=True, help="Target (newer) commit hash or ref")
    parser.add_argument(
        "--config",
        default=str(CONFIG_PATH),
        help="Optional path for the generated JSON config (defaults to analysis_config.json)",
    )
    parser.add_argument(
        "--generate-prompt",
        action="store_true",
        help="Immediately invoke commit_analyzer.py after writing the config (optional when running the batch pipeline).",
    )
    parser.add_argument(
        "--skip-automation",
        action="store_true",
        help="Prepare config only; do not launch run_automation.bat after completion.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    repo_path = Path(args.repo).expanduser()
    commit1 = args.commit1.strip()
    commit2 = args.commit2.strip()
    config_path = Path(args.config).expanduser()

    print("[manager] Validating repository path...")
    validate_repo(repo_path)

    print("[manager] Validating commit references...")
    validate_commit(repo_path, commit1)
    validate_commit(repo_path, commit2)

    print(f"[manager] Writing configuration to {config_path} ...")
    write_config(repo_path, commit1, commit2, config_path)
    print("[manager] Configuration updated successfully.")

    if args.generate_prompt:
        print("[manager] Triggering prompt generation via commit_analyzer.py ...")
        from commit_analyzer import main as analyzer_main

        analyzer_main(str(repo_path), commit1, commit2, config_path)
        print("[manager] Prompt generation completed.")

    if args.skip_automation:
        print("[manager] Automation skipped (per --skip-automation flag). Run run_automation.bat later if needed.")
        return

    print(f"[manager] Launching automated VS Code workflow via {BATCH_SCRIPT_PATH} ...")
    run_batch_script(BATCH_SCRIPT_PATH)
    print("[manager] Automation completed. Check batch_log.txt and Gemini output for results.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # surface actionable errors to the user
        print(f"[manager][ERROR] {exc}")
        sys.exit(1)
