# 2018 Peter Petrik (zilolv at gmail dot com)
# GNU General Public License 2 any later version

import argparse
import shutil
import os
import glob
import subprocess

import qgisBundlerTools.otool as otool
import qgisBundlerTools.install_name_tool as install_name_tool


class QGISBundlerError(Exception):
    pass


parser = argparse.ArgumentParser(description='Create QGIS Application installer for MacOS')

parser.add_argument('--qgis_install_tree',
                    required=True,
                    help='make install destination (QGIS.app)')
parser.add_argument('--output_directory',
                    required=True,
                    help='output directory for resulting QGIS.app files')
parser.add_argument('--python',
                    required=True,
                    help='directory with python framework to bundle, something like /usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/Python')
parser.add_argument('--pyqt',
                    required=True,
                    help='directory with pyqt packages to bundle, something like /usr/local/Cellar/pyqt/5.10.1_1/lib/python3.7/site-packages/PyQt5')
parser.add_argument('--rpath_hint',
                    required=False,
                    default="")

args = parser.parse_args()

print("QGIS INSTALL TREE: " + args.qgis_install_tree)
print("OUTPUT DIRECTORY: " + args.output_directory)
print("PYTHON: " + args.python)
print("PYQT: " + args.pyqt)

if not os.path.exists(args.python):
    raise QGISBundlerError(args.python + " does not exists")

pyqtHostDir = args.pyqt
if not os.path.exists(os.path.join(pyqtHostDir, "QtCore.so")):
    raise QGISBundlerError(args.pyqt + " does not contain QtCore.so")

pythonHost = args.python
if not os.path.exists(pythonHost):
    raise QGISBundlerError(args.pyqt + " does not contain Python")

if not os.path.exists(os.path.join(args.qgis_install_tree, "QGIS.app")):
    raise QGISBundlerError(args.qgis_install_tree + " does not contain QGIS.app")


qgisApp = os.path.join(args.output_directory, "QGIS.app")
contentsDir = os.path.join(qgisApp, "Contents")
macosDir = os.path.join(contentsDir, "MacOS")
frameworksDir = os.path.join(contentsDir, "Frameworks")
libDir =os.path.join(macosDir, "lib")
qgisExe = os.path.join(macosDir, "QGIS")
pluginsDir = os.path.join(contentsDir, "PlugIns")
qgisPluginsDir = os.path.join(pluginsDir, "qgis")
pythonDir = os.path.join(contentsDir, "Resources", "python")

print(100*"*")
print("STEP 0: Copy QGIS and independent folders to build folder")
print(100*"*")

print ("Cleaning: " + args.output_directory)
if os.path.exists(args.output_directory):
    shutil.rmtree(args.output_directory)
    if os.path.exists(args.output_directory + "/.DS_Store"):
        os.remove(args.output_directory + "/.DS_Store")
else:
    os.makedirs(args.output_directory)

print("Copying " + args.qgis_install_tree)
shutil.copytree(args.qgis_install_tree, args.output_directory, symlinks=True)
if not os.path.exists(qgisApp):
    raise QGISBundlerError(qgisExe + " does not exists")

print("Copying PyQt " + pyqtHostDir)
shutil.copytree(pyqtHostDir, pythonDir + "/PyQt5", symlinks=True)
subprocess.call(['chmod', '-R', '+w', pythonDir + "/PyQt5"])

pyqttest = os.path.join(pythonDir, "PyQt5/Qt.so")
if not os.path.exists(pyqttest):
    raise QGISBundlerError(pyqttest + " does not exists")

print(100*"*")
print("STEP 1: Analyze the libraries we need to bundle")
print(100*"*")

# Find QT
qtDir = None
for framework in otool.get_binary_dependencies(qgisExe).frameworks:
    if "lib/QtCore.framework" in framework:
        path = os.path.realpath(framework)
        qtDir = path.split("/lib/")[0]
        break
if not qtDir:
    raise QGISBundlerError("Unable to find QT install directory")
print("Found QT: " + qtDir)

# Find QCA dir
qcaDir = None
for framework in otool.get_binary_dependencies(qgisExe).frameworks:
    if "lib/qca" in framework:
        path = os.path.realpath(framework)
        qcaDir = path.split("/lib/")[0]
        break
if not qcaDir:
    raise QGISBundlerError("Unable to find QCA install directory")
print("Found QCA: " + qcaDir)

# Analyze all
sys_libs = set()
libs = set()
frameworks = set()

deps_queue = set()
done_queue = set()

# initial items:
# 1. qgis executable
deps_queue.add(qgisExe)
# 2. dynamic qgis providers
deps_queue |= set(glob.glob(qgisPluginsDir + "/*.so"))
# 3. python libraries
deps_queue |= set(glob.glob(pythonDir + "/*/*.so"))
deps_queue |= set(glob.glob(pythonDir + "/*/*.dylib"))
# 4. dynamic qt providers
# TODO do we need all?
deps_queue |= set(glob.glob(qtDir + "/plugins/*/*.dylib"))
deps_queue |= set(glob.glob(qcaDir + "/lib/qt5/plugins/*/*.dylib"))
# 5. python interpreter
deps_queue.add(pythonHost)

while deps_queue:
    lib = deps_queue.pop()
    # patch @rpath, @loader_path and @executable_path
    lib_fixed = lib.replace("@rpath", args.rpath_hint)
    lib_fixed = lib_fixed.replace("@executable_path", macosDir)
    lib_fixed = lib_fixed.replace("@loader_path/../../../MacOS/..", contentsDir)
    lib_fixed = lib_fixed.replace("@loader_path/../../..", frameworksDir)
    lib_fixed = lib_fixed.replace("@loader_path/../..", contentsDir)

    if lib_fixed in done_queue:
        continue

    if not lib_fixed:
        continue

    extraInfo = "" if lib == lib_fixed else "(" + lib_fixed + ")"
    print("Analyzing " + lib + extraInfo)
    done_queue.add(lib_fixed)

    if not os.path.exists(lib_fixed):
        raise QGISBundlerError("Library missing!")

    binaryDependencies = otool.get_binary_dependencies(lib_fixed)

    sys_libs |= set(binaryDependencies.sys_libs)
    libs |= set(binaryDependencies.libs)
    frameworks |= set(binaryDependencies.frameworks)

    deps_queue |= set(binaryDependencies.libs)
    deps_queue |= set(binaryDependencies.frameworks)


msg = "\nLibs:\n\t"
msg += "\n\t".join(sorted(libs))
msg += "\nFrameworks:\n\t"
msg += "\n\t".join(sorted(frameworks))
msg += "\nSysLibs:\n\t"
msg += "\n\t".join(sorted(sys_libs))
print(msg)

print(100*"*")
print("STEP 2: Copy libraries/plugins to bundle")
print(100*"*")
for lib in libs:
    # We assume that all libraries with @ are already bundled in QGIS.app
    # TODO in conda they use rpath, so this is not true
    if not lib or "@" in lib:
        continue

    # libraries to lib dir
    # plugins to plugin dir/plugin name/, e.g. PlugIns/qgis, PlugIns/platform, ...
    if "/plugins/" in lib:
        pluginFolder = lib.split("/plugins/")[1]
        pluginFolder = pluginFolder.split("/")[0]
        target_dir = pluginsDir + "/" + pluginFolder
    else:
        target_dir = libDir

    print("Bundling " + lib + " to " + target_dir)
    try:
        # only copy if not already in the bundle
        if qgisApp not in lib:
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            shutil.copy2(lib, target_dir)

        new_file = os.path.join(target_dir, os.path.basename(lib))
        subprocess.call(['chmod', '+w', new_file])
    except:
        print("Warning: " + lib + "? double copy TODO ?")

print(100*"*")
print("STEP 3: Copy frameworks to bundle")
print(100*"*")
for framework in frameworks:
    # We assume that all libraries with @ are already bundled in QGIS.app
    # TODO in conda they use rpath, so this is not true
    if not framework or "@" in framework:
        continue

    baseFrameworkDir = os.path.join(framework, os.pardir, os.pardir, os.pardir)
    baseFrameworkDir = os.path.abspath(baseFrameworkDir)
    if not baseFrameworkDir.endswith(".framework"):
        baseFrameworkDir = os.path.join(framework, os.pardir)
        baseFrameworkDir = os.path.abspath(baseFrameworkDir)
        if not baseFrameworkDir.endswith(".framework"):
            raise QGISBundlerError("Wrong framework directory structure!")

    frameworkName = os.path.basename(baseFrameworkDir)
    print("Bundling " + baseFrameworkDir + " to " + frameworksDir)
    try:
        new_framework = os.path.join(frameworksDir, frameworkName)
        # only copy if not already in the bundle
        if qgisApp not in baseFrameworkDir:
            shutil.copytree(baseFrameworkDir, new_framework, symlinks=True)
        subprocess.call(['chmod', '-R', '+w', new_framework])
    except:
        print("Warning: " + frameworkName + "? double copy TODO ?")

libPatchedPath = "@executable_path/lib"
relLibPathToFramework = "@executable_path/../Frameworks"

print(100*"*")
print("STEP 4: Fix frameworks linker paths")
print(100*"*")
frameworks = glob.glob(frameworksDir + "/*.framework")
for framework in frameworks:
    print("Patching " + framework)
    frameworkName = os.path.basename(framework)
    frameworkName = frameworkName.replace(".framework", "")

    # patch versions framework
    last_version = None
    versions = sorted(glob.glob(os.path.join(framework, "Versions") + "/*"))
    for version in versions:
        verFramework = os.path.join(version, frameworkName)
        if os.path.exists(verFramework):
            if not os.path.islink(verFramework):
                binaryDependencies = otool.get_binary_dependencies(verFramework)
                install_name_tool.fix_lib(verFramework, binaryDependencies, contentsDir, libPatchedPath, relLibPathToFramework)
                subprocess.call(['chmod', '+x', verFramework])
            if version is not "Current":
                last_version = os.path.basename(version)
        else:
            print("Warning: Missing " + verFramework)

    # patch current version
    currentFramework = os.path.join(framework, frameworkName)
    if os.path.exists(currentFramework):
        if not os.path.islink(verFramework):
            binaryDependencies = otool.get_binary_dependencies(currentFramework)
            install_name_tool.fix_lib(currentFramework, binaryDependencies, contentsDir, libPatchedPath, relLibPathToFramework)
            subprocess.call(['chmod', '+x', currentFramework])
    else:
        if last_version is None:
            print("Warning: Missing " + currentFramework)
        else:
            print("Creating version link for " + currentFramework)
            subprocess.call(["ln", "-s", last_version, framework + "/Versions/Current"])
            subprocess.call(["ln", "-s", "Versions/Current/" + frameworkName, currentFramework])

print(100*"*")
print("STEP 5: Fix libraries/plugins linker paths")
print(100*"*")
libs = glob.glob(libDir + "/*.dylib")
libs += glob.glob(qgisPluginsDir + "/*.so")
libs += glob.glob(pluginsDir + "/*/*.dylib")
libs += glob.glob(pythonDir + "/*/*.so")
libs += glob.glob(pythonDir + "/*/*.dylib")

# note there are some libs here: /Python.framework/Versions/Current/lib/*.dylib but
# those are just links to Current/Python
for lib in libs:
    if not os.path.islink(lib):
        print("Patching " + lib)
        binaryDependencies = otool.get_binary_dependencies(lib)
        install_name_tool.fix_lib(lib, binaryDependencies, contentsDir, libPatchedPath, relLibPathToFramework)
        subprocess.call(['chmod', '+x', lib])
    else:
        print("Skipping link " + lib)

print(100*"*")
print("STEP 6: Fix executables linker paths")
print(100*"*")
exes = set()
exes.add(qgisExe)
exes.add(macosDir + "/lib/qgis/crssync")
exes |= set(glob.glob(frameworksDir + "/Python.framework/Versions/Current/bin/*"))

for exe in exes:
    if not os.path.islink(exe):
        print("Patching " + exe)
        binaryDependencies = otool.get_binary_dependencies(exe)
        try:
            install_name_tool.fix_lib(exe, binaryDependencies, contentsDir, libPatchedPath, relLibPathToFramework)
        except subprocess.CalledProcessError:
            # Python.framework/Versions/Current/bin/idle3 is not a Mach-O file ??
            pass
        subprocess.call(['chmod', '+x', exe])
    else:
        print("Skipping link " + exe)

print(100*"*")
print("STEP 7: Fix QCA_PLUGIN_PATH Qt Plugin path")
print(100*"*")
# It looks like that QCA compiled with QCA_PLUGIN_PATH CMake define
# adds this by default to QT_PLUGIN_PATH. Overwrite this
# in resulting binary library
qcaLib = os.path.join(frameworksDir, "qca-qt5.framework", "qca-qt5")
f = open(qcaLib, 'rb+')
data = f.read()
data=data.replace(bytes(qcaDir + "/lib/qt5/plugins"), bytes(qcaDir + "/xxx/xxx/plugins"))
f.seek(0)
f.write(data)
f.close()

output = subprocess.check_output(["strings", qcaLib])
if qcaLib in output:
    raise QGISBundlerError("Failed to patch " + qcaLib)

print(100*"*")
print("STEP 8: Test full tree QGIS.app")
print(100*"*")

print("Test qgis --help works")
try:
    output = subprocess.check_output([qgisExe, "--help"], stderr=subprocess.STDOUT)
except subprocess.CalledProcessError as err:
    # for some reason it returns exit 1 even when it writes help
    output = err.output
if output:
    print(output.split("\n")[0])
if "QGIS" not in output:
    raise QGISBundlerError("wrong QGIS.app installation")

print(100*"*")
print("STEP 9: Create installer")
print(100*"*")
pkgFile = args.output_directory + "/qgis.pkg"
args = ["productbuild",
        "--identifier", "co.uk.lutraconsulting.qgis",
        "--component", qgisApp,
        "/Applications",
        pkgFile
        ]
subprocess.check_output(args)
fsize = subprocess.check_output(["du", "-h", pkgFile])
print("ALL DONE\n" + fsize)