; gemini_automation.ahk - Final Clipboard Version

; --- CONFIGURATION ---
vscode_path = "C:\Users\20114\AppData\Local\Programs\Microsoft VS Code\Code.exe"
vscode_dir  = "C:\Users\20114\AppData\Local\Programs\Microsoft VS Code\"
gemini_shortcut = "!g" ; ! for Alt
; -------------------

; Open Visual Studio Code and wait for it to be ready
Run, %vscode_path%, %vscode_dir%
Loop, 15
{
    if WinExist("ahk_exe Code.exe")
    {
        WinActivate, ahk_exe Code.exe
        found_window := true
        break
    }
    Sleep, 1000
}

if not found_window
{
    ExitApp ; Silently exit if window not found
}

; Give VS Code a moment to initialize before sending keys
Sleep, 2000

; Make key presses more deliberate
SendInput, %gemini_shortcut%
; Wait for VS Code and the extension to fully load.
Sleep, 8000

; Ensure VS Code is active before opening Command Palette
WinActivate, ahk_exe Code.exe
WinWaitActive, ahk_exe Code.exe

; Open Command Palette
Send, ^+p
Sleep, 1000

; Type and execute 'Gemini: Focus Chat View'
SendInput, Gemini: Focus Chat View{Enter}
Sleep, 2000 ; Wait for the view to open and focus to settle

; Wait for the Python script to copy the prompt to the clipboard
ClipWait, 5 ; Wait up to 5 seconds for clipboard to have content
if ErrorLevel
{
    ExitApp
}

; Paste the prompt from the clipboard
SendInput, ^v ; Send Ctrl+V
Sleep, 500 ; Give VS Code a moment to process the paste
SendInput, {Enter}

ExitApp
