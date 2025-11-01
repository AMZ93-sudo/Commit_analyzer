@ECHO OFF
ECHO Generating prompt and copying to clipboard...
python.exe "C:\Users\20114\Gemini_commit_analyzer\commit_analyzer.py"

ECHO Starting UI automation...
START "" "C:\Users\20114\Gemini_commit_analyzer\gemini_automation.ahk"

EXIT
