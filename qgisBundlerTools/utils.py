# 2018 Peter Petrik (zilolv at gmail dot com)
# GNU General Public License 2 any later version

import os


def framework_name(framework):
    # references Version/X
    baseFrameworkDir = os.path.join(framework, os.pardir, os.pardir, os.pardir)
    baseFrameworkDir = os.path.abspath(baseFrameworkDir)
    if not baseFrameworkDir.endswith(".framework"):
        # references current
        baseFrameworkDir = os.path.join(framework, os.pardir)
        baseFrameworkDir = os.path.abspath(baseFrameworkDir)
        if not baseFrameworkDir.endswith(".framework"):
            raise Exception("Wrong framework directory structure!" + framework)

    frameworkName = os.path.basename(baseFrameworkDir)
    frameworkName = frameworkName.replace(".framework", "")

    return frameworkName