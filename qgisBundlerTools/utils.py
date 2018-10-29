# 2018 Peter Petrik (zilolv at gmail dot com)
# GNU General Public License 2 any later version

import os


def framework_name(framework):
    path = framework
    while path:
        path = os.path.abspath(path)
        if path.endswith(".framework"):
            break
        path = os.path.join(path, os.pardir)

    if not path:
        raise Exception("Wrong framework directory structure!" + framework)

    frameworkName = os.path.basename(path)
    frameworkName = frameworkName.replace(".framework", "")

    return frameworkName, path