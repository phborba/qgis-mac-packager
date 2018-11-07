import subprocess
import os

import qgisBundlerTools.otool as otool
import qgisBundlerTools.install_name_tool as install_name_tool

class QGISBundlerError(Exception):
    pass


def step8(pa):
    print(100*"*")
    print("STEP 8: Test full tree QGIS.app")
    print(100*"*")

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
            if file_extension in [".dylib", ".so", ""] and otool.is_omach_file(filepath):
                print('Checking compactness of ' + filepath)
                binaryDependencies = otool.get_binary_dependencies(pa, filepath)
                all_binaries = binaryDependencies.libs + binaryDependencies.frameworks

                for bin in all_binaries:
                    if bin:
                        binpath = bin.replace("@executable_path", os.path.realpath(pa.macosDir))
                        binpath = os.path.realpath(binpath)

                        if "@" in binpath:
                            raise QGISBundlerError("Library/Framework " + bin + " with rpath or loader path for " + filepath)

                        binpath = os.path.realpath(binpath)
                        if not os.path.exists(binpath):
                            raise QGISBundlerError("Library/Framework " + bin + " not exist for " + filepath)

                        if pa.qgisApp not in binpath:
                            raise QGISBundlerError("Library/Framework " + bin + " is not in bundle dir for " + filepath)

    print("Test that all links are pointing to the destination inside the bundle")
    for root, dirs, files in os.walk(pa.qgisApp):
        for file in files:
            filepath = os.path.join(root, file)
            filepath = os.path.realpath(filepath)
            if not os.path.exists(filepath):
                raise QGISBundlerError(" File " + root + "/" + file + " does not exist")

            if pa.qgisApp not in filepath:
                raise QGISBundlerError(" File " + root + "/" + file + " is not in bundle dir")
