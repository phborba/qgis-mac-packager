# QGIS standalone package

Set of scripts to create MacOS standalone QGIS package (dmg)

For package details, see [details page](https://lutraconsulting.github.io/qgis-mac-packager/)

# Server Setup 

- Get Mojave server
- Get Apple Development Program for your Apple ID
- Login to the server (have static IP)
- Change default password to some secure one
- Install XCode from App Store 
- Go to Apple Developer Download page -> More and command line tools. Install both
- Sign out from the apple developer page and app store
- Open XCode and accept license
- install homebrew and QGIS deps by running `install_brew.bash`
- Update `~/.bash_profile`
```
export CLICOLOR=1
export PS1="\[\e[32m\]\u\[\e[m\]\[\e[32m\]@\[\e[m\]\[\e[32m\]\h\[\e[m\]:\[\e[34m\]\w\[\e[m\]\\$ "

# allow bash completion 
if [ -f $(brew --prefix)/etc/bash_completion ]; then
    . $(brew --prefix)/etc/bash_completion
fi

export PATH="/usr/local/sbin:$PATH"
export HOMEBREW_NO_AUTO_UPDATE=1
```
- now clone this repository
- so your folders structure is
```
  dropbox_token.txt
  qgis-mac-packager/
  builds/nightly
  builds/pr
  builds/ltr
```

1. Install deps as described above
2. Download QGIS git repository
3. Build release version with QGIS_MACAPP_BUNDLE=0 and install it to your local folder
4. Run `python3 bundler/qgis-bundler.py` to get `QGIS.app` bundle
5. Run `python3 packager/qgis-packager.py` to get `qgis.dmg` file
5. Run `python3 uploader/qgis-uploader.py` to upload to dropbox

Upload to Dropbox

1. Create App with a folder to upload a files, get a token
2. Create File ~/Projects/dropbox_token.txt and paste the token inside

# Server Update

- TODO