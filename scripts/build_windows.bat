@echo off
REM build_windows.bat - One-click build script for Windows
REM
REM Produces a self-contained "Arbiter.exe" inside scripts\dist\.
REM The bundle embeds Python and every required library, so it can run on
REM machines that do not have Python installed.
REM
REM Usage (from any directory):
REM   scripts\build_windows.bat
REM
REM Requirements on the build machine:
REM   - Python 3.10+ with pip

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
REM Remove trailing backslash
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "REPO_ROOT=%SCRIPT_DIR%\.."
set "SRC_DIR=%REPO_ROOT%\src"
set "REQ_FILE=%REPO_ROOT%\requirements.txt"

echo =^> Installing/upgrading PyInstaller and project dependencies...
pip install --upgrade pip
if errorlevel 1 goto :error

pip install --upgrade pyinstaller
if errorlevel 1 goto :error

pip install -r "%REQ_FILE%"
if errorlevel 1 goto :error

echo =^> Building Arbiter.exe with PyInstaller...
pyinstaller ^
  --name "Arbiter" ^
  --windowed ^
  --noconfirm ^
  --clean ^
  --distpath "%SCRIPT_DIR%\dist" ^
  --workpath "%SCRIPT_DIR%\build" ^
  --specpath "%SCRIPT_DIR%" ^
  --paths "%SRC_DIR%" ^
  --add-data "%SRC_DIR%\ui;ui" ^
  --hidden-import "webview" ^
  --hidden-import "webview.platforms.winforms" ^
  --hidden-import "webview.platforms.edgechromium" ^
  --hidden-import "webview.platforms.mshtml" ^
  --hidden-import "py4swiss" ^
  --collect-all "webview" ^
  "%SRC_DIR%\mainGUI.py"
if errorlevel 1 goto :error

echo.
echo =^> Build complete!
echo     Standalone executable: %SCRIPT_DIR%\dist\Arbiter\Arbiter.exe
goto :eof

:error
echo.
echo ERROR: Build failed. Check the output above for details.
exit /b 1
