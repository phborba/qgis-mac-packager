# 2018 Peter Petrik (zilolv at gmail dot com)
# GNU General Public License 2 any later version

import subprocess
import os
from .utils import framework_name


def fix_lib(binary, depLibs, contentsPath, relLibPathToExe, relLibPathToFramework):
    binary = os.path.realpath(binary)
    p = binary.replace(contentsPath, "@executable_path/..")
    args = ["install_name_tool", "-id", p, binary]
    try:
        subprocess.check_output(args)
    except:
        print("WARNING: " + binary)

    for lib in depLibs.libs:
        # WORKAROUND # TODO REMOVE ME
        libworkaround = lib.replace("libopenblas_haswellp-r0.3.3.dylib", "libopenblasp-r0.3.3.dylib")

        args = ["install_name_tool",
                "-change", libworkaround,
                relLibPathToExe + "/" + os.path.basename(lib),
                binary]
        try:
            subprocess.check_output(args)
        except:
            print("WARNING: " + binary)

    for framework in depLibs.frameworks:
        frameworkName, frameworkDir = framework_name(framework)
        # Do not use versions lib, just the main one
        framework_path = relLibPathToFramework + "/" + frameworkName + ".framework/" + frameworkName
        args = ["install_name_tool", "-change", framework, framework_path, binary]
        subprocess.check_output(args)
