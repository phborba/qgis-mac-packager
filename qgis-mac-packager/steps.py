import subprocess
import os

import qgisBundlerTools.otool as otool
import qgisBundlerTools.install_name_tool as install_name_tool


class QGISBundlerError(Exception):
    pass


def clean_redundant_files(pa, cp):
    extensionsToCheck = [".a", ".pyc", ".c", ".cpp", ".h", ".hpp", ".cmake", ".prl"]
    dirsToCheck = ["/include", "/Headers", "/__pycache__", "/test", "/tests", "/examples"]

    # remove unneeded files/dirs
    for root, dirnames, filenames in os.walk(pa.qgisApp):
        for file in filenames:
            fpath = os.path.join(root, file)
            filename, file_extension = os.path.splitext(fpath)
            if any(ext==file_extension for ext in extensionsToCheck):
                print("Removing " + fpath)
                cp.rm(fpath)

        for dir in dirnames:
            dpath = os.path.join(root, dir)
            print(dpath)
            if any(ext in dpath for ext in dirsToCheck):
                print("Removing " + dpath)
                cp.rm(dpath)

    # remove broken links and empty dirs
    for root, dirnames, filenames in os.walk(pa.qgisApp):
        for file in filenames:
            fpath = os.path.join(root, file)
            real = os.path.realpath(fpath)
            if not os.path.exists(real):
                os.unlink(fpath)


def check_deps(pa, filepath, executable_path):
    binaryDependencies = otool.get_binary_dependencies(pa, filepath)
    all_binaries = binaryDependencies.libs + binaryDependencies.frameworks

    for bin in all_binaries:
        if bin:
            binpath = bin.replace("@executable_path", executable_path)
            binpath = os.path.realpath(binpath)

            if "@" in binpath:
                raise QGISBundlerError("Library/Framework " + bin + " with rpath or loader path for " + filepath)

            binpath = os.path.realpath(binpath)
            if not os.path.exists(binpath):
                raise QGISBundlerError("Library/Framework " + bin + " not exist for " + filepath)

            if pa.qgisApp not in binpath:
                raise QGISBundlerError("Library/Framework " + bin + " is not in bundle dir for " + filepath)


def test_full_tree_consistency(pa):
    print("Test qgis --help works")
    try:
        output = subprocess.check_output([pa.qgisExe, "--help"], stderr=subprocess.STDOUT, encoding='UTF-8')
    except subprocess.CalledProcessError as err:
        # for some reason it returns exit 1 even when it writes help
        output = err.output
    if output:
        print(output.split("\n")[0])
    if "QGIS" not in output:
        raise QGISBundlerError("wrong QGIS.app installation")


    print("Test that all libraries have correct link and and bundled")
    for root, dirs, files in os.walk(pa.qgisApp):
        for file in files:
            filepath = os.path.join(root, file)
            filename, file_extension = os.path.splitext(filepath)
            if file_extension in [".dylib", ".so"] and otool.is_omach_file(filepath):
                print('Checking compactness of library ' + filepath)
                check_deps(pa, filepath, os.path.realpath(pa.macosDir))
            elif not file_extension and otool.is_omach_file(filepath): # no extension == binaries
                if os.access(filepath, os.X_OK) and ("/Frameworks/" not in filepath):
                    print('Checking compactness of binaries ' + filepath)
                    check_deps(pa, filepath, os.path.dirname(filepath))
                else:
                    print('Checking compactness of library ' + filepath)
                    check_deps(pa, filepath, os.path.realpath(pa.macosDir))

    print("Test that all links are pointing to the destination inside the bundle")
    for root, dirs, files in os.walk(pa.qgisApp):
        for file in files:
            filepath = os.path.join(root, file)
            filepath = os.path.realpath(filepath)
            if not os.path.exists(filepath):
                raise QGISBundlerError(" File " + root + "/" + file + " does not exist")

            if pa.qgisApp not in filepath:
                raise QGISBundlerError(" File " + root + "/" + file + " is not in bundle dir")
