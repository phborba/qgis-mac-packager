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
- to upload to Dropbox
    1. Create App with a folder to upload a files, get a token
    2. Create File ~/Projects/dropbox_token.txt and paste the token inside
- copy `run_cronjob` one folder above
- to Code Signing 
    - You need application certificate from https://developer.apple.com/account
    - Generate production/development signing identify
    - Get cer file and scp to the server
    - Double click on cer file and install it on the server
    - On Machine where you created request, export private key and copy and install on server too.
    - `security find-identity -v` to find existing identities 
    - create `sing_identity.txt` with the ID of your identity
- so your folders structure is
```
  dropbox_token.txt
  sign_identity.txt
  run_cronjob.bash
  qgis-mac-packager/
  builds/
  logs/
```
- Run `run_*.bash` to build nightly/ltr/pr releases
- Nightly releases should be set as cronjobs once per day (use tabs!)
``` 
crontab -e
0   12  *   *   *  bash /Users/lutra/qgis/run_cronjob.bash > /Users/lutra/qgis/logs/cron.log 2>&1
``` 

# Server Update

- update brew
- update cronjob
- remove build/* folders for clean build
- update docs/README.md with new set of used libs

