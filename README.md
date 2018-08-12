# Neuropsy (formerly flanker)

## Install
[Click here to install the latest release](https://github.com/tainagdcoleman/flanker/releases/download/1.5/setup.exe)

## Dependencies
* pyyaml
* screeninfo
* openpyxl
* kivy
* python-dateutil
* Inno Setup

## For Developing
To install all dependencies:
```bash
conda config --add channels conda-forge
conda install kivy
pip install pyyaml screeninfo openpyxl python-dateutil
```

## For Building
To build on Windows, install the following dependencies:
```bash
python -m pip install --upgrade pip wheel setuptools
python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
pip install PyInstaller
```

Download [Inno Setup](http://www.jrsoftware.org/download.php/is.exe) to create a setup.exe

# Build Instructions
First, run the build python script:
```bash
python build.py
```

Then, open install.iss with Inno Setup and compile. The setup executable will be created at ***Output/setup.exe***.
