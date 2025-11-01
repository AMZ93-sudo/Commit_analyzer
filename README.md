# Gemini Commit Analyzer Automation Tool

## 🚀 Overview

This tool automates the process of analyzing code changes between two Git commits, generating a detailed prompt for Google's Gemini Code Assist extension in Visual Studio Code, and then automatically injecting that prompt into the extension's chat window for analysis.

## ✨ Features

*   **Automated Git Diff:** Compares two specified commits in a local Git repository.
*   **Intelligent Prompt Generation:** Creates a detailed Gemini-ready prompt requesting analysis on RAM/ROM consumption, CPU load, and potential risks of the code changes.
*   **Clipboard Integration:** Copies the generated prompt directly to the system clipboard.
*   **VS Code Automation:** Automatically launches Visual Studio Code, opens the Gemini Code Assist extension, focuses the chat input, pastes the prompt, and submits it.
*   **Fully Automated Workflow:** From execution to prompt submission, the process requires minimal manual intervention.

## 📋 Prerequisites

Before running this tool, ensure you have the following installed and configured on your Windows machine:

1.  **Git:**
    *   **Description:** Version control system required for analyzing code changes.
    *   **Installation:** Download from [git-scm.com](https://git-scm.com/download/win).
    *   **Verification:** Open Command Prompt and type `git --version`.

2.  **Python 3.x:**
    *   **Description:** Required to run the `commit_analyzer.py` script.
    *   **Installation:** Download from [python.org](https://www.python.org/downloads/windows/). Ensure you check "Add Python to PATH" during installation.
    *   **Verification:** Open Command Prompt and type `python --version`.

3.  **AutoHotkey v1.x:**
    *   **Description:** Powerful scripting language for Windows automation, used to control Visual Studio Code.
    *   **Installation:** Download from [autohotkey.com](https://www.autohotkey.com/download/). Choose "v1.1 (Installer)".
    *   **Verification:** After installation, Right-click on your desktop, select "New" > "AutoHotkey Script". If you see this option, it's installed. Double-clicking an `.ahk` file should execute it.

4.  **Visual Studio Code:**
    *   **Description:** Your code editor, where Gemini Code Assist runs.
    *   **Installation:** Download from [code.visualstudio.com](https://code.visualstudio.com/).
    *   **Verification:** Ensure you can launch VS Code.

5.  **Gemini Code Assist Extension for VS Code:**
    *   **Description:** The AI assistant that will analyze your code.
    *   **Installation:** Install directly from the VS Code Extensions Marketplace (search for "Gemini Code Assist").
    *   **Verification:** Ensure the Gemini extension is enabled and you can open its chat window (default shortcut is `Alt+G`).

## 📦 Installation

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd Gemini_commit_analyzer
    ```
    (Replace `<repository_url>` with the actual URL if this project is hosted.)

2.  **Download as ZIP (if not using Git):**
    *   Download the project files as a ZIP archive.
    *   Extract the contents to a directory of your choice (e.g., `C:\Tools\Gemini_commit_analyzer`).

## ⚙️ Configuration

This tool requires minor configuration to adapt to your environment and specific analysis needs.

1.  **`commit_analyzer.py`**
    *   Open `commit_analyzer.py` in a text editor.
    *   Locate the `--- CONFIGURATION ---` section.
    *   **`repo_path`**: Update this variable with the **absolute path** to your local Git repository that you want to analyze.
    *   **`commit1`**: Set this to the hash of the **older** commit (or branch name, tag, etc.).
    *   **`commit2`**: Set this to the hash of the **newer** commit (or branch name, tag, etc.) you want to compare against `commit1`.
    
    ```python
    # Example configuration:
    repo_path = "C:/Users/YourUser/Projects/MyAwesomeRepo"
    commit1 = "abcdef123" # Older commit hash
    commit2 = "fedcba321" # Newer commit hash
    ```

2.  **`gemini_automation.ahk`**
    *   Open `gemini_automation.ahk` in a text editor.
    *   Locate the `--- CONFIGURATION ---` section.
    *   **`vscode_path`**: **Crucial!** This must be the **absolute path** to your Visual Studio Code executable (`Code.exe`).
        *   **How to find it:** Right-click your VS Code shortcut (on Desktop, Start Menu, or Taskbar), select `Properties`, and copy the path from the `Target` field. Ensure the path includes `Code.exe`.
        ```autohotkey
        ; Example configuration:
        vscode_path = "C:\Users\YourUser\AppData\Local\Programs\Microsoft VS Code\Code.exe"
        vscode_dir  = "C:\Users\YourUser\AppData\Local\Programs\Microsoft VS Code\"
        ```
    *   **`gemini_shortcut`**: Ensure this matches the keyboard shortcut you use to open the Gemini Code Assist chat window in VS Code. The default is `!g` (Alt+G).
        ```autohotkey
        ; Example configuration:
        gemini_shortcut = "!g" ; ! for Alt, ^ for Ctrl, + for Shift
        ```

## 🚀 How to Use

1.  **Ensure VS Code is Closed:** For the most reliable operation, close all instances of Visual Studio Code before running the tool. The tool will open a fresh instance.
2.  **Run the Automation:** Simply **double-click the `run_automation.bat` file** located in the project's root directory.

### Workflow

The `run_automation.bat` script will orchestrate the following:
1.  Executes `commit_analyzer.py` to get the Git diff and copy the analysis prompt to your clipboard.
2.  Launches Visual Studio Code.
3.  Sends the `Alt+G` shortcut to open the Gemini Code Assist extension.
4.  Uses the VS Code Command Palette to explicitly focus the Gemini chat input field.
5.  Pastes the prepared prompt into the Gemini chat.
6.  Sends the `Enter` key to submit the prompt for analysis.

## ⚠️ Troubleshooting

*   **"ERROR: clip.exe not found." (from Python script):** Ensure your Windows installation is not corrupted. `clip.exe` is a standard Windows utility.
*   **VS Code doesn't open or isn't detected:** Double-check the `vscode_path` and `vscode_dir` variables in `gemini_automation.ahk`. Ensure the path is exact.
*   **Gemini extension doesn't open:** Verify `gemini_shortcut` in `gemini_automation.ahk` is correct and matches your VS Code shortcut for Gemini.
*   **Prompt is not pasted/submitted:** If issues persist, there might be subtle timing differences on your system. You can try adjusting the `Sleep` durations in `gemini_automation.ahk` (e.g., `Sleep, 8000` to `Sleep, 10000`). Make small changes and test.

## 📂 Repository Structure

```
Gemini_commit_analyzer/
├── commit_analyzer.py
├── gemini_automation.ahk
└── run_automation.bat
└── README.md
```
