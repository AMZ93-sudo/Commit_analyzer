import subprocess
import os

def run_command(command):
    """Runs a shell command and returns its output."""
    print(f"  - Executing command: {command}")
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True, shell=True)
        print("  - Command executed successfully.")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"  - ERROR: Command failed with exit code {e.returncode}")
        print(f"  - Stderr: {e.stderr}")
        return None

def copy_to_clipboard(text):
    """Copies the given text to the Windows clipboard."""
    try:
        subprocess.run(["clip.exe"], input=text.strip().encode("utf-8"), check=True)
        print("  - SUCCESS: Prompt copied to clipboard.")
    except FileNotFoundError:
        print("  - ERROR: clip.exe not found. Could not copy to clipboard.")
    except subprocess.CalledProcessError as e:
        print(f"  - ERROR: Failed to copy to clipboard. Error: {e}")

def main():
    """Main function to analyze commits and generate a prompt."""
    print("  - Reading configuration...")
    # --- CONFIGURATION ---
    repo_path = "D:\SWe\AI\Test_myrepo"
    commit1 = "a4b0d2eeccc79c166c1d43550e51ebbadac110d4"
    commit2 = "7885d11f436fa71ca9720fe7e0e8c8129cac5785"
    # -------------------
    print(f"    - Repo Path: {repo_path}")
    print(f"    - Commit 1: {commit1}")
    print(f"    - Commit 2: {commit2}")

    if not os.path.isdir(repo_path):
        print(f"  - ERROR: Repository path not found: {repo_path}")
        return

    git_diff_command = f'git -C "{repo_path}" diff {commit1} {commit2}'
    diff_output = run_command(git_diff_command)

    if diff_output:
        print("  - Git diff successful. Generating prompt...")
        prompt = f"""
Analyze the following code changes and provide a detailed analysis of the impact on the system from RAM/ROM consumption and runtime CPU load perspectives.

**Code Changes:**
```diff
{diff_output}
```

**Analysis Request:**
1.  **RAM/ROM Consumption:**
    *   How do the changes affect the memory footprint of the application?
    *   Are there any new data structures or variables that would increase memory usage?
    *   Are there any optimizations that would reduce memory usage?

2.  **CPU Load:**
    *   How do the changes affect the CPU load during runtime?
    *   Are there any new algorithms or computations that would increase CPU usage?
    *   Are there any optimizations that would reduce CPU usage?

3.  **Potential Risks:**
    *   Are there any potential performance bottlenecks introduced by these changes?
    *   Are there any risks of memory leaks or excessive resource consumption?

Please provide a detailed and quantitative analysis where possible.
"""
        copy_to_clipboard(prompt)
    else:
        print("  - ERROR: Git diff returned no output. Prompt not generated.")

if __name__ == "__main__":
    main()