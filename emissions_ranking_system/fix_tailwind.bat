@echo off
echo Installing Tailwind PostCSS Fix...
cd ..\carba_lens_web
call npm install @tailwindcss/postcss
echo.
echo ==================================================
echo Fix Complete! 
echo Please STOP your current Vite server (Ctrl+C) and run 'npm run dev' again.
echo ==================================================
pause
