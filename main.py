# test_console.py
import subprocess

# Befehl, der in der neuen Konsole ausgeführt wird
command = 'echo Hallo aus der neuen Konsole! & pause'

# Öffnet ein neues Konsolenfenster unter Windows
subprocess.Popen(
    ['cmd', '/c', command],
    creationflags=subprocess.CREATE_NEW_CONSOLE
)
