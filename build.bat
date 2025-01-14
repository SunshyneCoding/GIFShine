@echo off
echo 🔨 Setting up build environment...

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 🌱 Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate

:: Install requirements
echo 📦 Installing requirements...
pip install -r requirements.txt
pip install pyinstaller

:: Create executable with PyInstaller
echo 🏗️ Building executable...
pyinstaller .\resources\gif_gui.spec

:: Create CLI version
echo 🔧 Building CLI version...
pyinstaller .\resources\gif_cli.spec

:: Deactivate virtual environment
echo 🔌 Deactivating virtual environment...
deactivate

echo ✨ Build complete! Executables are in the dist folder.
pause
