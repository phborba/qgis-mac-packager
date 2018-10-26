# 2018 Peter Petrik (zilolv at gmail dot com)
# GNU General Public License 2 any later version

import subprocess
import os
from .utils import framework_name


def fix_lib(binary, depLibs, contentsPath, relLibPathToExe, relLibPathToFramework):
    binary = os.path.realpath(binary)
    p = binary.replace(contentsPath, "@executable_path/..")
    args = ["install_name_tool", "-id", p, binary]
    subprocess.check_output(args)

    for lib in depLibs.libs:
        args = ["install_name_tool",
                "-change", lib,
                relLibPathToExe + "/" + os.path.basename(lib),
                binary]
        subprocess.check_output(args)

    for framework in depLibs.frameworks:
        frameworkName = framework_name(framework)
        # Do not use versions lib, just the main one
        framework_path = relLibPathToFramework + "/" + frameworkName + ".framework/" + frameworkName
        args = ["install_name_tool", "-change", framework, framework_path, binary]
        subprocess.check_output(args)
