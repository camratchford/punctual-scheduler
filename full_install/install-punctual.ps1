# Variables
$NSSMPath  = Join-Path -Path $ENV:LOCALAPPDATA -ChildPath NSSM
$PuncPath = Join-Path -Path $ENV:LOCALAPPDATA -ChildPath PuncTesty
$ServiceName = "Punkytest"

# Create space for NSSM
if (-not (Test-Path -Path $NSSMPath)) {
    New-Item -Path $NSSMPath -ItemType Directory > $null
}

# Download NSSM
Write-Host "Donwloading nssm.exe"
Invoke-WebRequest -URI "https://nssm.cc/release/nssm-2.24.zip" -OutFile (Join-Path -Path $NSSMPath -ChildPath "nssm-2.24.zip")
Expand-Archive -Path (Join-Path -Path $NSSMPath -ChildPath "nssm-2.24.zip") -DestinationPath $NSSMPath
Copy-Item -Path (Join-Path -Path $NSSMPath -ChildPath "nssm-2.24\win64\nssm.exe") -Destination $NSSMPath
Remove-Item -Path (Join-Path -Path $NSSMPath -ChildPath "nssm-2.24.zip")
Remove-Item -Path (Join-Path -Path $NSSMPath -ChildPath "nssm-2.24") -Recurse

# Create space for punc
if (-not (Test-Path -Path $PuncPath)) {
    New-Item -Path $PuncPath -ItemType Directory > $null
}

# Download punc
Write-Host "Donwloading punc.exe"
Invoke-WebRequest -URI "https://github.com/camratchford/punctual-scheduler/files/10593845/punc.zip" -OutFile (Join-Path -Path $PuncPath -ChildPath "punc.zip")
Expand-Archive -Path (Join-Path -Path $PuncPath -ChildPath "punc.zip") -DestinationPath $PuncPath
Remove-Item -Path (Join-Path -Path $PuncPath -ChildPath "punc.zip")

# Create folder structure for punc
$LogPath = Join-Path -Path $PuncPath -ChildPath logs
if (-not (Test-Path -Path $LogPath)) {
    New-Item -Path $LogPath -ItemType Directory > $null
}

$ScriptsPath = Join-Path -Path $PuncPath -ChildPath scripts
if (-not (Test-Path -Path $ScriptsPath)) {
    New-Item -Path $ScriptsPath -ItemType Directory > $null
}

$TasksFile = Join-Path -Path $PuncPath -ChildPath tasks.yml
if (-not (Test-Path -Path $TasksFile)) {
    New-Item -Path $TasksFile -ItemType File > $null
    Add-Content -Path $TasksFile -Value "@
tasks:
  - name: 'Backup Photos'
    state: present
    first_run:
      value: '2/11/23 19:20:00'
      format: '%m/%d/%y %H:%M:%S'
    frequency:
      value: 1
      format: '%d'
    action:
      name: 'backup_photos'
      action_type: 'python'
      path: '.\scripts\backup_photos.py'
    toast:
      title: 'Backup Photos'
      message: Photos are being backed up
@"
}

$ConfigFile = Join-Path -Path $PuncPath -ChildPath config.yml
if (-not (Test-Path -Path $ConfigFile)) {
    New-Item -Path $ConfigFile -ItemType File > $null
    Add-Content -Path $ConfigFile -Value "@
logs_dir: .\logs
log_config:
  version: 1
  disable_existing_loggers: True
  formatters:
    brief:
      format: '%(message)s'
      use_colors: True
    verbose:
      format: |
        %(asctime)s:
          Level:   %(levelname)s
          File:    %(filename)s
          LineNo:  %(lineno)d
          Msg:     %(message)s
  handlers:
    file:
      class : logging.handlers.RotatingFileHandler
      formatter: verbose
      filename: punctual.log
      maxBytes: 1048576 # 1MB
      backupCount: 3
    console:
      class : logging.StreamHandler
      formatter: brief
      level   : DEBUG
      stream  : ext://sys.stdout
  loggers:
    ez_temp:
      handlers:
        - file
        - console
      level: DEBUG
      propagate: False
@"
}

# Register Punc as service
Write-Host "Registering punc.exe as a service"
$Cred = $(Get-Credential)
$UserName = $Cred.UserName
$pwd = $cred.Password
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($pwd)
$Password = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

$NSSMExec = (Join-Path -Path $NSSMPath -ChildPath "nssm.exe")
$PuncExe = (Join-Path -Path $NSSMPath -ChildPath "punc.exe")

Start-Process -FilePath $NSSMExec -ArgumentList @("install", $ServiceName, $PuncExe) -Credential $Cred
Start-Process -FilePath $NSSMExec -ArgumentList @("set", $ServiceName, "AppDirectory", $PuncPath) -Credential $Cred
Start-Process -FilePath $NSSMExec -ArgumentList @("set", $ServiceName, "AppExit", "Default", "Restart") -Credential $Cred
Start-Process -FilePath $NSSMExec -ArgumentList @("set", $ServiceName, "Description", "Punctual Task Scheduler") -Credential $Cred
Start-Process -FilePath $NSSMExec -ArgumentList @("set", $ServiceName, "DisplayName", "Punctual") -Credential $Cred
Start-Process -FilePath $NSSMExec -ArgumentList @("set", $ServiceName, "ObjectName", $UserName, $Password) -Credential $Cred
Start-Process -FilePath $NSSMExec -ArgumentList @("set", $ServiceName, "Start", "SERVICE_DELAYED_AUTO_START") -Credential $Cred
Start-Process -FilePath $NSSMExec -ArgumentList @("set", $ServiceName, "Type", "SERVICE_WIN32_OWN_PROCESS") -Credential $Cred

