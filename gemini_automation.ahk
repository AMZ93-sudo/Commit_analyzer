; gemini_automation.ahk - AutoHotkey v2 (Strict v16)

; --- CONFIGURATION ---
vscode_path := "C:\Users\20114\AppData\Local\Programs\Microsoft VS Code\Code.exe"
changed_files_path := A_ScriptDir . "\changed_files.txt"
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

Sleep(5000) ; Give VS Code time to finish loading

OpenChangedFiles(changed_files_path)
PastePrompt()

ExitApp()

OpenChangedFiles(fileListPath)
{
    if !FileExist(fileListPath)
    {
        return
    }

    try
    {
        fileContent := FileRead(fileListPath, "UTF-8")
    }
    catch
    {
        return
    }

    files := StrSplit(fileContent, "`n")
    for filePath in files
    {
        trimmed := Trim(filePath, " `r`t")
        if (trimmed = "")
        {
            continue
        }

        Send("^p")
        Sleep(500)
        SendText(trimmed)
        Sleep(600)
        Send("{Enter}")
        Sleep(900)
    }

    ; Close the quick-open box so subsequent automation doesn't type into it
    Send("{Esc}")
    Sleep(400)
}

EnsureGeminiChatActive()
{
    WinActivate("ahk_exe Code.exe")
    Sleep(200)
    Send("{Esc}")
    Sleep(200)
    RunPaletteCommand("Gemini Code Assist: Open Chat")
    RunPaletteCommand("Gemini: Focus on Chat View")
}

RunPaletteCommand(commandText)
{
    Send("^+p")
    Sleep(700)
    Send("^a")
    Sleep(150)
    SendText(">" . commandText)
    Sleep(250)
    Send("{Enter}")
    Sleep(3500)
}

PastePrompt()
{
    if !ClipWait(5)
    {
        MsgBox("Clipboard data not found. Ensure commit_analyzer.py ran successfully.")
        return
    }

    EnsureGeminiChatActive()
    Sleep(400)
    Send("^a")
    Sleep(250)
    Send("^v")
    Sleep(800)

    Send("{Enter}")
    Sleep(1200)
}
