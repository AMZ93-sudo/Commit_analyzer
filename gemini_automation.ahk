; gemini_automation.ahk - AutoHotkey v2 (Strict v16)

; --- CONFIGURATION ---
vscode_path := "C:\Users\20114\AppData\Local\Programs\Microsoft VS Code\Code.exe"
; -------------------

try
{
    Run('"' . vscode_path . '"')
}
catch
{
    MsgBox("Error: Could not run VS Code. Check vscode_path.")
    ExitApp()
}

if !WinWait("ahk_exe Code.exe",, 15)
{
    MsgBox("Error: VS Code window not found.")
    ExitApp()
}

WinActivate("ahk_exe Code.exe")

if !WinWaitActive("ahk_exe Code.exe",, 5)
{
    MsgBox("Error: Could not activate VS Code window.")
    ExitApp()
}

Sleep(5000) ; Increased sleep to give VS Code more time to settle

Send("^+p") ; Send Ctrl+Shift+P to open the command palette
Sleep(1000)
SendInput("Gemini: Focus on Chat View{Enter}") ; Type the command to open Gemini Chat and press Enter
Sleep(5000) ; Wait for Gemini to open and focus

; Try pasting multiple times to ensure it works
Loop 3
{
    Send("^v") ; Paste the content from the clipboard
    Sleep(1000) ; Wait 1 second between attempts
}

Send("{Enter}") ; Press Enter to submit the prompt

ExitApp()
