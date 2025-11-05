@ECHO OFF
(ECHO Batch script started) > batch_log.txt

(ECHO Checking for AutoHotkey executable...) >> batch_log.txt
IF EXIST "C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe" (
    (ECHO AutoHotkey executable found.) >> batch_log.txt
) ELSE (
    (ECHO AutoHotkey executable not found.) >> batch_log.txt
    GOTO :EOF
)

(ECHO Generating prompt...) >> batch_log.txt
python.exe "D:/SWe/AI/Commit analyzer/Commit_analyzer/commit_analyzer.py" >> batch_log.txt 2>&1

(ECHO Executing AutoHotkey script...) >> batch_log.txt
"C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe" "D:\SWe\AI\Commit analyzer\Commit_analyzer\gemini_automation.ahk" >> batch_log.txt 2>&1

(ECHO Batch script finished.) >> batch_log.txt

EXIT