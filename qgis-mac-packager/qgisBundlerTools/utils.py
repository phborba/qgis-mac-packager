# 2018 Peter Petrik (zilolv at gmail dot com)
# GNU General Public License 2 any later version

import os
import shutil


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


def resolve_libpath(pa, lib_path):
    # loader path should be really resolved here, because
    # it is relative to this binary
    if "@loader_path" in lib_path:
        if os.path.exists(lib_path.replace("@loader_path/../../../MacOS/..", pa.contentsDir)):
            lib_path = lib_path.replace("@loader_path/../../../MacOS/..", pa.contentsDir)
        elif os.path.exists(lib_path.replace("@loader_path/../../..", pa.frameworksDir)):
            lib_path = lib_path.replace("@loader_path/../../..", pa.frameworksDir)
        elif os.path.exists(lib_path.replace("@loader_path/../..", pa.contentsDir)):
            lib_path = lib_path.replace("@loader_path/../..", pa.contentsDir)
        elif os.path.exists("/usr/local/lib" + lib_path.replace("@loader_path/.dylibs", "")):
            lib_path = "/usr/local/lib" + lib_path.replace("@loader_path/.dylibs", "")
        elif os.path.exists("/usr/local" + lib_path.replace("@loader_path", "")):
            lib_path = "/usr/local" + lib_path.replace("@loader_path", "")
        else:
            for binary in []:
                if os.path.exists(os.path.dirname(binary) + "/" + lib_path.replace("@loader_path", "")):
                    lib_path = os.path.dirname(binary) + "/" + lib_path.replace("@loader_path", "")
                    break
                elif os.path.exists(pa.pysitepackages + "/" + os.path.basename(os.path.dirname(binary)) + lib_path.replace("@loader_path","")):
                    lib_path = pa.pysitepackages + "/" + os.path.basename(os.path.dirname(binary)) + lib_path.replace("@loader_path", "")
                    break

    return lib_path


# to make sure we
# NEVER NEVER NEVER
# deletes something outside
# the build directory
class CopyUtils:
    def __init__(self, outdir):
        self.outdir = outdir

    def _is_in_out_dir(self, name):
        if self.outdir not in name:
            realpath = os.path.realpath(name)
            if self.outdir not in realpath:
                raise Exception("Trying to do file operation outsite bundle directory! " + name)

    def recreate_dir(self, name):
        if os.path.exists(name):
            self.rmtree(name)
            if os.path.exists(name + "/.DS_Store"):
                self.remove(name + "/.DS_Store")
        else:
            os.makedirs(name)

    def remove(self, name):
        self._is_in_out_dir(name)
        os.remove(name)

    def rmtree(self, name):
        self._is_in_out_dir(name)
        shutil.rmtree(name)

    def symlink(self, src, dest):
        self._is_in_out_dir(dest)
        if os.path.isabs(src):
            self._is_in_out_dir(src)
        else:
            self._is_in_out_dir(os.path.dirname(dest) + "/" + src)
        try:
            os.symlink(src, dest)
        except:
            print( dest + " -> " + src)
            raise

    def unlink(self, name):
        self._is_in_out_dir(name)
        os.unlink(name)

    def copy(self, src, dest):
        self._is_in_out_dir(dest)
        shutil.copy2(src, dest)

    def copytree(self, src, dest, symlinks):
        self._is_in_out_dir(dest)
        shutil.copytree(src, dest, symlinks=symlinks)