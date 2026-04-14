@echo off
echo ============================================
echo  COCOMO 2 Calculator - Сборка EXE (Windows)
echo ============================================

echo [1/3] Установка зависимостей...
pip install pyinstaller --quiet

echo [2/3] Сборка исполняемого файла...
pyinstaller --onefile --windowed --name COCOMO2_Calculator cocomo2.py

echo [3/3] Готово!
echo.
echo Исполняемый файл: dist\COCOMO2_Calculator.exe
echo.
pause
