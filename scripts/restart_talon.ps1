$ErrorActionPreference = "Stop"
(get-wmiobject win32_process -filter "name='talon.exe'").terminate()
Start-Process "C:\Program Files\Talon\talon.exe"