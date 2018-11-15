# 2018 Peter Petrik (zilolv at gmail dot com)
# GNU General Public License 2 any later version

import subprocess
import platform
import os
import time


def timestamp():
    ts = time.gmtime()
    return time.strftime("%Y-%m-%d %H:%M:%S", ts)


def brew_prefix():
    output = subprocess.check_output(["brew", "--prefix"], encoding='UTF-8')
    homebrew_dir = output.strip()
    if not os.path.isdir(homebrew_dir):
        raise Exception("Missing homebrew folder " + homebrew_dir)
    return homebrew_dir

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

    homebrew_dir = brew_prefix()

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


def check_py_version(name):
    cmd = "import {}; print({}.__version__)".format(name, name)
    try:
        output = subprocess.check_output(["python3", "-c", cmd], encoding='UTF-8')
        return output.strip()
    except:
        print("Unable to detect version for " + name)
        return ""


def python_libs():
    exclude = ["dropbox", "__pycache__"]
    libs = {}
    homebrew_dir = brew_prefix()

    # List all folders immediately under this folder:
    sitepackages = os.path.join(homebrew_dir, "lib/python3.7/site-packages/")
    pkgs = next(os.walk(sitepackages))[1]
    for pkg in pkgs:
        pkg_dir = os.path.join(sitepackages, pkg)
        excluded = False
        for e in exclude:
            if e in pkg_dir:
                excluded = True
                break
        if excluded:
            continue

        # e.g. decorator-4.3.0.dist-info
        if "dist-info" in pkg:
            parts = pkg.replace(".dist-info", "").split("-")
            libs[parts[0]] = parts[1]
        elif "-py3.7.egg-info" in pkg:
            # e.g numpy-1.15.4-py3.7.egg-info/
            parts = pkg.replace("-py3.7.egg-info", "").split("-")
            libs[parts[0]] = parts[1]
        else:
            if os.path.isdir(pkg_dir):
                if pkg not in libs:
                    libs[pkg] = check_py_version(pkg)

    ret = []
    for lk in libs.keys():
        ret += ["- " + lk + " " + libs[lk]]

    return "\n".join(sorted(ret))


def get_computer_info():
    mac_ver = platform.mac_ver()[0]

    msg = ""
    msg += "Minimum supported MacOS version is " + mac_ver + "\n\n"
    msg += "Package was built with XCode " + xcode() + "\n\n"
    msg += "Used Homebrew's packages\n\n"
    msg += homebrew_libs() + "\n\n"
    msg += "Used Python3 modules\n\n"
    msg += python_libs() + "\n\n"
    msg += "Updated: " + timestamp()

    return msg


# print to stdout
print(get_computer_info())