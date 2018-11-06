# QGIS standalone package

Set of scripts to create MacOS standalone QGIS package (dmg)

For package details, see [details page](https://lutraconsulting.github.io/qgis-mac-packager/)

# Server Setup 

we use http://maccloud.me Mini server for nightly builds

- MacOS El Capitan 10.11.6
- XCode 8.2
- Homebrew 

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

## Building

1. Install deps as described above
2. Download QGIS git repository
3. Build release version with QGIS_MACAPP_BUNDLE=0 and install it to your local folder
4. Run `python3 bundler/qgis-bundler.py` to get `QGIS.app` bundle
5. Run `python3 packager/qgis-packager.py` to get `qgis.dmg` file
5. Run `python3 uploader/qgis-uploader.py` to upload to dropbox

# Upload to Dropbox

1. Create App with a folder to upload a files, get a token
2. Create File ~/Projects/dropbox_token.txt and paste the token inside
