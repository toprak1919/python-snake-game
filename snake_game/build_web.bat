@echo off
echo Building Snake Game for web deployment...
echo.
python -m pygbag --build --archive .
echo.
echo Build complete! The web.zip file in the "build" folder can be deployed to:
echo - itch.io
echo - Your own web server
echo - GitHub Pages
echo.
pause
