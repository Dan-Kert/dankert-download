@echo off
REM Запуск основного скрипта dankert_download с передачей всех аргументов
REM Если Python не найден, вывести ошибку

where py >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python не найден в PATH.
    exit /b 1
)

py -Werror -Xdev "%~dp0dankert_download\__main__.py" %*
