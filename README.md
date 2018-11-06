# QGIS standalone package

Set of scripts to create MacOS standalone QGIS package (dmg)

# Package details

Supported MacOS El Capitan 10.11 and higher

Includes:
- QGIS
- Python 3.7
- Qt
- PyQt
- GDAL

# Developement 

## Server 

# Current server:

- MacOS El Capitan 10.11.4
- XCode 7.3.1
- Command Line Tools 7.3.1

# Server common setup

- add homebrew to `bash_profile`
```
export PATH="/usr/local/sbin:$PATH"
export HOMEBREW_NO_AUTO_UPDATE=1
```


# Bundling and Packaging

Note you need to have Apple Development Program purchased

1. Get mac on cloud, login (have static IP)
2. Go to Apple Developer Download page and download XCode for your OS and command line tools. Install
3. Open XCode and accept license
4. install homebrew and run 
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew tap osgeo/osgeo4mac
brew install git
brew install openvpn
brew install szip
brew install hdf5
brew install cython
brew link --overwrite numpy
brew install scipy
brew install netcdf
pip3 install dropbox
brew cask install xquartz
brew install qgis3 --only-dependencies 
```

# Upload to Dropbox

1. Create App with a folder to upload a files, get a token
2. Create File ~/Projects/dropbox_token.txt and paste the token inside

## Building

1. Install homebrew and follow steps on homebrew-osgeo4mac to install qgis3
2. Download QGIS git repository
3. Build release version and install it to your local folder
4. Run `python qgis-bundler.py` with python3 and with some reasonable parameters (see `run_bundler.sh`)
5. This will create .pkg file with 


Notes:

- QGIS should be built with QGIS_MACAPP_BUNDLE=0
- In principle it should work with conda deps, but not tested
- This can be probably a replacement of envisioned QGIS_MACAPP_BUNDLE=3 level (qgis/QGIS/mac/*.cmake scripts)
