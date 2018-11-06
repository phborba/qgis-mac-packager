# 2018 Peter Petrik (zilolv at gmail dot com)
# GNU General Public License 2 any later version

import subprocess
import platform
import os

def xcode():
    output = subprocess.check_output(["system_profiler", "SPDeveloperToolsDataType"], encoding='UTF-8')
    for l in output.split('\n'):
        l = l.strip()
        if l.startswith("Version:"):
            l = l.replace("Version:", "")
            l = l.strip()
            return l
    return "Unknown"

def homebrew_libs():
    exclude = ["python@2", "bash-completion", "gdal"]
    libs = []

    output = subprocess.check_output(["brew", "--prefix"], encoding='UTF-8')
    homebrew_dir = output.strip()
    if not os.path.isdir(homebrew_dir):
        raise Exception("Missing homebrew folder " + homebrew_dir)

    # List all folders immediately under this folder:
    cellar_dir = os.path.join(homebrew_dir, "Cellar")
    bottles = next(os.walk(cellar_dir))[1]
    for bottle in bottles:
        bottle_dir = os.path.join(cellar_dir, bottle)
        versions = next(os.walk(bottle_dir))[1]
        if len(versions) != 1:
            raise Exception("Multiple versions installed for " + bottle_dir)

        excluded = False
        for e in exclude:
            if bottle.endswith(e):
                excluded = True
                break
        if excluded:
            continue

        libs += ["- " + bottle + " " + str(versions[0])]

    return "\n".join(sorted(libs))

mac_ver = platform.mac_ver()[0]

print("# Package Details")
print("Package contains standalone QGIS installation.\n")
print("Minimum supported version is " + mac_ver + "\n")
print("Package was build with XCode  " + xcode() + " and following Homebrew's packages\n")
print(homebrew_libs())
