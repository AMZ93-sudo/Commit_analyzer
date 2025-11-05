# Issue Tracker

This document tracks the issues faced during the development of the `gemini_automation.ahk` script and their resolutions.

## Issue 1: Gemini Code Assist Not Opening

*   **Problem:** The initial version of the script only opened Visual Studio Code and pressed the F1 key. It did not open the Gemini Code Assist chat window as intended.
*   **Solution:** The script was modified to send `Ctrl+Shift+P` to open the command palette, then type "Gemini: Focus on Chat View" and press Enter to specifically open the Gemini chat interface.

## Issue 2: Script Toggling System Language

*   **Problem:** The script was causing the system's input language to toggle (the equivalent of pressing `Alt+Shift`). This was due to an incorrect command being used to open the command palette.
*   **Solution:** The command was corrected from `Send("^p")` (Ctrl+P) to `Send("^+p")` (Ctrl+Shift+P) to accurately trigger the command palette in VS Code and avoid unintended system-wide shortcuts.

## Issue 3: Prompt Not Pasting into Gemini Chat

*   **Problem:** Even after opening the Gemini chat view, the script failed to paste the prompt content into the input field. This was identified as a timing issue, where the paste command was executing before the chat window was fully loaded and focused.
*   **Solution:**
    1.  An initial attempt was made to increase the `Sleep` delay to give the chat window more time to load. This was not consistently successful.
    2.  The final and successful solution was to implement a loop that attempts to paste the content multiple times. This ensures that one of the paste attempts succeeds once the chat input field is ready to receive text.
