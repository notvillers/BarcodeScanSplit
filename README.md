# BarcodeScanSplit

Reads pdf files from directory, split the pages and renames them by the barcode found on each page.

## Extra requirements
- [Zbar](https://github.com/NaturalHistoryMuseum/pyzbar)
- [Poppler](https://poppler.freedesktop.org/) or [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows)

## Arguments

### Using arguments
- ```-s```, ```--source``` : Directory containing PDF files.
- ```-d```, ```--destination```: Directory to store output files.
- ```-b```, ```--backup```: Directory to store backup files.
- ```-l```, ```--log```: Directory to store log files.
- ```-t```, ```--temp```: Temporary directory to store split.
- ```-i```, ```--image```: Temporary directory to store the images.
- ```-m```, ```--mode```: Processing mode. (```single```, ```multi```)
- ```-p```, ```--processes```: Maximum number of processes to run, by default is the number of CPU threads.

(If any of the arguments left empty the script will read its pair from the default [config](config.py) file.)

## Running
### Windows:
Example usage:
```
    python splitter.py -s docs -d out -m multi -p 4
```
```
    powershell.exe .\splitter.ps1
```
```
    .\splitter.bat
```
### Unix/Linux/Mac:
Example usage:
```
    python3 splitter.py -s docs -d out -m multi -p 4
```
```
    ./barcodescansplit.sh -s docs -d out -m multi -p 4
    
```