@echo off
REM ============================================================
REM  Builds Murdle.exe - just double-click this file.
REM  It must be in the same folder as Murdle.py.
REM ============================================================

cd /d "%~dp0"

echo Installing PyInstaller (the tool that makes the .exe)...
py -m pip install pyinstaller

echo.
echo Building Murdle.exe... this can take a minute or two.
py -m PyInstaller --noconfirm --onefile --windowed --name Murdle ^
    --add-data "assets;assets" ^
    --add-data "sounds;sounds" ^
    --hidden-import main ^
    --hidden-import Store ^
    --hidden-import case_001 ^
    --hidden-import case_002 ^
    Murdle.py

echo.
echo ============================================================
echo  Done! Your game is here:  dist\Murdle.exe
echo ============================================================
pause
