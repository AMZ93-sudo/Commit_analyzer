import json
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = BASE_DIR / "analysis_config.json"
DEFAULT_TEMPLATE_PATH = BASE_DIR / "commit_analysis_prompt.txt"
PROMPT_OUTPUT_PATH = BASE_DIR / "prompt.txt"
CHANGED_FILES_PATH = BASE_DIR / "changed_files.txt"


def run_command(command: List[str], *, cwd: Optional[str] = None) -> Optional[str]:
    """Runs a shell command (no shell) and returns stdout on success."""
    printable_command = " ".join(command)
    print(f"  - Executing command: {printable_command}")
    try:
        result = subprocess.run(
            command,
            check=True,
            text=True,
            capture_output=True,
            cwd=cwd,
        )
        print("  - Command executed successfully.")
        return result.stdout
    except subprocess.CalledProcessError as exc:
        print(f"  - ERROR: Command failed with exit code {exc.returncode}")
        print(f"    - Stderr: {exc.stderr.strip()}")
        return None


def copy_to_clipboard(text: str) -> None:
    """Copies the given text to the Windows clipboard."""
    try:
        subprocess.run(["clip.exe"], input=text.strip().encode("utf-8"), check=True)
        print("  - SUCCESS: Prompt copied to clipboard.")
    except FileNotFoundError:
        print("  - WARNING: clip.exe not found. Prompt not copied to clipboard.")
    except subprocess.CalledProcessError as exc:
        print(f"  - ERROR: Failed to copy to clipboard. Error: {exc}")


def load_config(config_path: Path) -> dict:
    """Loads repository/commit configuration from JSON."""
    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file '{config_path}' not found. "
            "Run analysis_manager.py to generate it or pass --repo/--commit arguments."
        )

    with config_path.open("r", encoding="utf-8") as config_file:
        data = json.load(config_file)

    for key in ("repo_path", "commit1", "commit2"):
        if key not in data or not data[key]:
            raise ValueError(f"Configuration file missing '{key}'.")
    return data


def gather_changed_files(repo_path: str, commit1: str, commit2: str) -> List[str]:
    """Returns the list of files touched between the two commits."""
    output = run_command(["git", "-C", repo_path, "diff", "--name-only", commit1, commit2])
    if output is None:
        return []
    return [line.strip() for line in output.splitlines() if line.strip()]


def save_changed_files(repo_path: str, files: List[str]) -> None:
    """Writes absolute paths for changed files so VS Code automation can open them."""
    repo_base = Path(repo_path)
    absolute_paths = []
    for rel_path in files:
        absolute_paths.append(str((repo_base / rel_path).resolve()))

    content = "\n".join(absolute_paths)
    CHANGED_FILES_PATH.write_text(content, encoding="utf-8")
    print(f"  - Wrote changed file list to {CHANGED_FILES_PATH}")


def load_template(template_path: Path) -> str:
    if not template_path.exists():
        raise FileNotFoundError(f"Prompt template not found: {template_path}")
    return template_path.read_text(encoding="utf-8")


def get_commit_details(repo_path: str, commit_ref: str) -> Dict[str, str]:
    format_str = "%H%n%an%n%ad"
    output = run_command([
        "git",
        "-C",
        repo_path,
        "show",
        "-s",
        f"--format={format_str}",
        commit_ref,
    ])
    if not output:
        return {"hash": commit_ref, "author": "Unknown", "date": "Unknown"}

    parts = output.strip().split("\n")
    return {
        "hash": parts[0] if len(parts) > 0 else commit_ref,
        "author": parts[1] if len(parts) > 1 else "Unknown",
        "date": parts[2] if len(parts) > 2 else "Unknown",
    }


def get_branch_name(repo_path: str, commit_ref: str) -> str:
    name = run_command([
        "git",
        "-C",
        repo_path,
        "name-rev",
        "--name-only",
        commit_ref,
    ])
    if name:
        cleaned = name.strip()
        if cleaned and cleaned != "undefined":
            return cleaned

    head_branch = run_command(["git", "-C", repo_path, "rev-parse", "--abbrev-ref", "HEAD"])
    return (head_branch or "unknown").strip()


def build_prompt(
    repo_path: str,
    commit1: str,
    commit2: str,
    changed_files: List[str],
    template_text: str,
    diff_output: str,
    metadata: Dict[str, Dict[str, str]],
    branch_name: str,
) -> str:
    repo_name = Path(repo_path).name or repo_path
    file_list = "\n".join(f"- {path}" for path in changed_files) or "- No tracked changes detected"
    diff_block = diff_output.strip() or "No diff output was produced."
    date_range = f"{metadata['old']['date']} -> {metadata['new']['date']}"
    author_range = f"{metadata['old']['author']} -> {metadata['new']['author']}"

    replacements = {
        "{REPO_NAME}": repo_name,
        "{COMMIT_HASH_OLD}": metadata["old"]["hash"],
        "{COMMIT_HASH_NEW}": metadata["new"]["hash"],
        "{BRANCH_NAME}": branch_name,
        "{AUTHOR_NAME}": author_range,
        "{DATE_RANGE}": date_range,
        "{FILE_LIST}": file_list,
        "{DIFF_CONTENT}": diff_block,
    }

    prompt = template_text
    for token, value in replacements.items():
        prompt = prompt.replace(token, value)

    return prompt.strip()


def persist_prompt(prompt: str) -> None:
    PROMPT_OUTPUT_PATH.write_text(prompt, encoding="utf-8")
    print(f"  - Prompt saved to {PROMPT_OUTPUT_PATH}")


def main(
    repo_path: Optional[str] = None,
    commit1: Optional[str] = None,
    commit2: Optional[str] = None,
    config_path: Path = DEFAULT_CONFIG_PATH,
    template_path: Path = DEFAULT_TEMPLATE_PATH,
):
    """Main entry point used by automation and CLI."""
    print("  - Preparing commit analysis input...")
    config: Optional[dict] = None
    if not all([repo_path, commit1, commit2]):
        config = load_config(config_path)
        repo_path = repo_path or config["repo_path"]
        commit1 = commit1 or config["commit1"]
        commit2 = commit2 or config["commit2"]

    assert repo_path and commit1 and commit2  # for type checkers
    print(f"    - Repo Path: {repo_path}")
    print(f"    - Commit 1: {commit1}")
    print(f"    - Commit 2: {commit2}")

    if not os.path.isdir(repo_path):
        raise FileNotFoundError(f"Repository path not found: {repo_path}")

    diff_output = run_command(["git", "-C", repo_path, "diff", commit1, commit2])
    if diff_output is None:
        print("  - ERROR: Git diff returned no output. Prompt not generated.")
        return None

    changed_files = gather_changed_files(repo_path, commit1, commit2)
    save_changed_files(repo_path, changed_files)

    metadata = {
        "old": get_commit_details(repo_path, commit1),
        "new": get_commit_details(repo_path, commit2),
    }
    branch_name = get_branch_name(repo_path, commit2)

    print("  - Loading prompt template...")
    template_text = load_template(template_path)
    prompt = build_prompt(
        repo_path,
        commit1,
        commit2,
        changed_files,
        template_text,
        diff_output,
        metadata,
        branch_name,
    )
    persist_prompt(prompt)
    copy_to_clipboard(prompt)
    return {"prompt": prompt, "changed_files": changed_files}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate prompt for Gemini commit analysis.")
    parser.add_argument("--repo", dest="repo_path", help="Path to the git repository")
    parser.add_argument("--commit1", help="Older/base commit hash")
    parser.add_argument("--commit2", help="Newer/target commit hash")
    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG_PATH),
        help="Optional path to analysis_config.json",
    )
    parser.add_argument(
        "--template",
        default=str(DEFAULT_TEMPLATE_PATH),
        help="Optional path to an HTML prompt template",
    )

    args = parser.parse_args()
    main(args.repo_path, args.commit1, args.commit2, Path(args.config), Path(args.template))
