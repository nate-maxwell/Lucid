SET launcherpath=%~dp0
echo %launcherpath:~0, -1%
call %launcherpath%..\..\venv\Scripts\python.exe %launcherpath%silver_launcher.py
