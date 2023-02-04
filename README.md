<h1 align="center">Punctual</h1>
<p align="center">
Better task scheduling in Windows OS
</p>

---

> <p align="center">
>  This is a work in progress, subject to many changes and new instabilities / brokenness.
> </p>

## Introduction

- Windows task scheduler sucks
  - It uses XML (XML sucks)
  - Debugging failed tasks sucks (it doesn't ever tell you why)
  - You have to write some jank PowerShell / CMD script to execute anything else
  - Doesn't tell you when something ran.

- Punctual does not suck (or at least sucks a bit less)
  - Uses YAML
  - Has extensible logging via the Python Standard Library `logging` package
  - You provide the path to the file you want ran, and it runs it.
  - Issues a Windows 10 'Toast' notification (optional)


## Getting started

### Installing compiled binary

```powershell
# Find a good spot for the application
$PuncPath = "$ENV:LOCALAPPDATA\punctual"
New-Item -Path $PuncPath -ItemType Directory
Set-Location $PuncPath

# Download the executable
Invoke-WebRequest -Uri "https://github.com/camratchford/punctual-scheduler/files/10593845/punc.zip" -OutFile "$PuncPath\punctual.zip"
# Extract the zip file
Expand-Archive -Path "$PuncPath\punctual.zip" -DestinationPath $PuncPath
Remove-Item -Path "$PuncPath\punctual.zip"
```

> ❗ The executable to run will be `$PuncPath\punc.exe`

### Installing from pip

```powershell
# Find a good spot for the application
$PuncPath = "$ENV:LOCALAPPDATA\punctual"
New-Item -Path $PuncPath -ItemType Directory
Set-Location $PuncPath

# Create a virtual environment 
python -m venv venv
# Git needs to be installed and in $ENV:PATH
.\venv\Scripts\pip.exe install git+https://github.com/camratchford/punctual-scheduler
```

> ❗ The executable to run will be `$PuncPath\venv\Scripts\punc.exe`

### Create the logs folder

```powershell
New-Item -Path "$PuncPath\logs" -ItemType Directory
```

### Creating a config file

Create the task config, located in: `$PuncPath\config.yml`
```yaml
logs_dir: C:\Users\testuser\AppData\Local\punctual\logs

# Python logging explained at https://docs.python.org/3/library/logging.config.html#dictionary-schema-details
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



```

### Give it a script to run

- At this moment, punctual only executes arbitrary Python scripts.
- PowerShell / CMD scripts, CLI executables and other actionable resources are in the works.
- Passing arguments to the scripts is also currently in development.

```powershell
# Create the scripts folder (or don't! you will be providing the absolute path anyways)
New-Item -Path $PuncPath\scripts -ItemType Directory
```

Create a Python file within your chosen scripts folder location.



```python
# C:\Users\testuser\AppData\local\punctual\scripts\test.py

from datetime import datetime


def main():
    with open(r"C:\Users\cameron\PycharmProjects\punctual\test\test_output.txt", "a+") as writer:
        writer.write(f"The time is {str(datetime.now())}\n")


if __name__ == "__main__":
    main()

```

### Creating a task file

Create the task file, located in: `$PuncPath\tasks.yml`

> ❗ Information on format codes can be found in [Python's 'datetime' documentation](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes)

> ❗ The value of action -> name must be unique

```yaml
tasks:
  - name: Test task
    first_run:
      value: 09/19/22 13:55:26
      format: '%m/%d/%y %H:%M:%S'
    frequency:
      value: 10
      format: '%S'
    action:
      name: time_tracker
      path: C:\Users\testuser\AppData\local\punctual\scripts\test.py
    toast:
      title: Time Tracker
      message: Time has been recorded
```

### Run

Before setting it up as a service, run the application (to see if everything is working with the outputs to stdout and stderr in front of you)

```powershell
# Set the environment variable for the application folder
$ENV:PUNCPATH = $PuncPath

# If you downloaded the compiled binary
.\punc.exe

# If you installed it with pip in a virtual environment
.\venv\Scripts\punc.exe

```

### Set up as a service

If everything ran correctly

- This application is meant to be run as a service. You can just run it as a background task in PowerShell, and it works. Alternatively, you can execute it via a CMD script in the startup folder. 
  - There's not really a 'perfect' way to automate the creation of a service that runs the application.
  - I've had success using [NSSM](https://nssm.cc/) to register it as one.
  - The settings I use are:
    - Environment: `PUNCPATH="<value of $PuncPath>"`
    - Start-up type: Automatic (Delayed start)
    - Run as: `<the account you log in as>`
  - The rest of the settings are up to you


## Author
[Cam Ratchford](https://github.com/camratchford)

## License
[CC0 1.0 Universal](./LICENSE)
