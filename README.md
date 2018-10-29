# PM Server

## Description


PM Server is a Python application that can be used to monitor particualte
matter measurements from a nova SDS011 sensor connected to the computer. The
application is still experimental and more or less only tested on a ubuntu 18
.04 OS. However, CIs are compiling the application into various executables
for Linux, Windows and Mac OSX. These files can be found in the
[Github Release](https://github.com/data-hydenv/pmserver/releases>) section.

There are two in this repository, either available as Python script or as
executable:

- **pm2csv.py** command line tool for saving particulate matter measurements
  into  a CSV file
- **pmserver** a browser based graphical application for monitoring
  particulate matter. The Python module is called ``pmserver``, while the
  application itself is called ``pmMonitor``.

## Releases


Both applications can either be used as Python modules or as executables. The
main advantage of Python is, that the Github version is always up-to-date, 
while the executable are only build for a new release. If you are familiar 
with Python, you can easily modify the code and reuse it. 
The main advantage of the executables is that you do not need Python 
installed at all to run the application. However, error handling will be more
complicated with the bundled versions.

Find the build status of the different versions below:

<table class="table table-striped">
<tr><th>Environment</th><th>Status</th></tr>
<tr><th>Linux / OSX</th><td><img src="https://travis-ci.org/data-hydenv/pmserver.svg?branch=master"></td></tr>
<tr><th>Windows</th><td><img src="https://ci.appveyor.com/api/projects/status/5ykoa4yjk1u4x239?svg=true"></td></tr>
</table>

latest build: https://github.com/data-hydenv/pmserver/releases

## Installation

In case you want to use one of the executables, just navigate to the latest 
release and download the executable suitable for your operation system: 
https://github.com/data-hydenv/pmserver/releases 

The other option is to download the source files from the latest release, or 
clone the whole repository (recommended). Cloning the repository will 
download the latest version of pmserver:

```bash
git clone https://data-hydenv/pmserver.git
```

Optionally, you can also download the full repository from github as a ``.zip`` 
and unzip the folder.

Next, you need to install the dependencies listed in ``requirements.txt``:

```bash
cd pmserver
pip install -r requirements
```

Now, you can run the ``pm2csv.py`` with the same Python environment like:

```bash
python pm2csv.py /dev/ttyUSB0
```

The graphical monitoring version can either be started by ``serv.py`` in the 
root directory or by ``pmserver/app.py``. The main difference is that 
``serv.py`` will additionally open a web-browser for you and point to the correct 
URL.  Unfortunately, this sometimes failes and I have no idea why. Then,
you'll have to use ``pmserver/app.py`` open the browser and point to 
``http://localhost:5000`` yourself.

## Usage

### pmMonitor

The pmMonitor just has to be started. Sometimes the application does not open
a web browser automatically. Then, with the application running, you'll have
to open a brwoser yourself and point to ``http://localhost:5000``.

## pm2csv

``pm2csv`` needs at least one argument passed, which is the device address of
the nova SDS011. In Windows, this is something like ``COM1``, ``COM2`` and so
 on.
 In Unix, the USB devices are mounted at ``/dev/ttyUSB0``, ``/dev/ttyUSB1`` 
 and so on. Plug the sensor in and out to see which address is appeaing and 
 disappearing. That's the one you need.
 
 To use the script, open a console at the location of the Python script or 
 executable and run it. 
 
 ```bash
 python pm2csv.py /dev/ttyUSB0
```

Will start recording measurements every 15 seconds into a file called 
``pm.csv`` at the same location. The new data will be appended. 
Additionally the measurements will be printed to the screen. Help 
for the usage can be view by using the --help (-h) flag:

```bash
python pm2csv.py --help
```

This will output something similar to:

```
usage: pm2csv [-h] [-b BAUDRATE] [-o OUTPUT] [-s STEP] [-q] device_path

Command line tool for saving particulate-matter measurements from a nova
SDS011 into a CSV file.

positional arguments:
  device_path           Device path of the sensor. Typically 'COM1' on Windows
                        or '/dev/ttyUSB0' on Linux.

optional arguments:
  -h, --help            show this help message and exit
  -b BAUDRATE, --baudrate BAUDRATE
                        Device baudrate for serial communication. Typical
                        values are 9600 or 57600. Defaults to 9600.
  -o OUTPUT, --output OUTPUT
                        Output file name. The new readings will be appended to
                        this file in CSV format. Defaults to 'pm.csv'.
  -s STEP, --step STEP  Step width for the measurements in seconds. It is not
                        recommended to use values smaller than 3 seconds.
                        Defaults to 15 [secs].
  -q, --quiet           Suppress printing values to the screen.

```
