@echo off
setlocal
cd /d "%~dp0"

py -3.12 -c "import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 12) and sys.maxsize > 2**32 else 1)" >nul 2>nul
if not errorlevel 1 goto use_py

python -c "import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 12) and sys.maxsize > 2**32 else 1)" >nul 2>nul
if not errorlevel 1 goto use_python

echo SETUP FAILED: approved 64-bit Python 3.12 was not found.
exit /b 1

:use_py
py -3.12 "%~dp0setup_environment.py" %*
exit /b %errorlevel%

:use_python
python "%~dp0setup_environment.py" %*
exit /b %errorlevel%
