@echo off
REM ============================================================
REM  Resets Murdle to a brand new player - just double-click.
REM  Deletes YOUR saved coins, solved cases and purchases.
REM  (Your friends' saves are on their own computers - this
REM   never touches them.)
REM ============================================================

echo Closing Murdle if it is open...
taskkill /IM Murdle.exe /F >nul 2>&1

echo Deleting saved progress...
del "%APPDATA%\Murdle\save_data.json" >nul 2>&1
del "%~dp0save_data.json" >nul 2>&1
del "%~dp0dist\save_data.json" >nul 2>&1

echo.
echo ============================================================
echo  Done! Next time you open Murdle, you start as a new player.
echo ============================================================
pause
