@echo off
echo Initializing Carba Lens Project...
cd ..
if exist carba_lens_web (
    echo Directory carba_lens_web already exists. Skipping creation.
) else (
    echo Creating Vite App...
    call npm create vite@latest carba_lens_web -- --template react
)

cd carba_lens_web
echo Installing Dependencies...
call npm install
echo Installing Tailwind...
call npm install -D tailwindcss postcss autoprefixer
call npx tailwindcss init -p
echo Installing UI Libraries...
call npm install lucide-react recharts framer-motion clsx tailwind-merge
echo.
echo ==========================================
echo Setup Complete! You can now start the server with:
echo cd carba_lens_web
echo npm run dev
echo ==========================================
pause
