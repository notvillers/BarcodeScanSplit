# BarcodeScanSplit

## Extra requirements
- [Zbar](https://github.com/NaturalHistoryMuseum/pyzbar)
- [Poppler](https://poppler.freedesktop.org/) or [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows)

## Setup

### Using the config
Setup the [config file](config.py), then run it as you wish:

### Using arguments
- ```-s```, ```--source``` : Directory containing PDF files
- ```-d```, ```--destination```: Directory to store output files
- ```-b```, ```--backup```: Directory to store backup files
- ```-l```, ```--log```: Directory to store log files
- ```-t```, ```--temp```: Temporary directory to store split 
- ```-i```, ```--image```: Temporary directory to store the images
(If any of the arguments left empty the script will read its pair from [config file](config.py).)

### Running
- Windows:
```
    python splitter.py {arguments_if_needed}
    powershell.exe .\splitter.ps1
    .\splitter.bat
```
- Unix/Linux/Mac:
```
    python splitter.py {arguments_if_needed}
    ./splitter.sh
```
(Notice the premade scripts can not handle arguments at the moment.)