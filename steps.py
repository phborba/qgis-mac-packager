import subprocess
import os

import qgisBundlerTools.otool as otool
import qgisBundlerTools.install_name_tool as install_name_tool

class QGISBundlerError(Exception):
    pass


def step8(qgisApp, qgisExe, macosDir):
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


    print("Test that all libraries have correct link and and bundled")
    for root, dirs, files in os.walk(qgisApp):
        if "/Headers/" in root:
            continue

        for file in files:
            filepath = os.path.join(root, file)
            filename, file_extension = os.path.splitext(filepath)
            if file_extension in [".dylib", ".so", ""] and otool.is_omach_file(filepath):
                print('Checking compactness of ' + filepath)
                binaryDependencies = otool.get_binary_dependencies(filepath)
                all_binaries = binaryDependencies.libs + binaryDependencies.frameworks

                for bin in all_binaries:
                    if bin:
                        binpath = bin.replace("@executable_path", os.path.realpath(macosDir))
                        binpath = os.path.realpath(binpath)

                        if "@" in binpath:
                            raise QGISBundlerError("Library/Framework " + bin + " with rpath or loader path for " + filepath)

                        binpath = os.path.realpath(binpath)
                        if not os.path.exists(binpath):
                            raise QGISBundlerError("Library/Framework " + bin + " not exist for " + filepath)

                        if qgisApp not in binpath:
                            raise QGISBundlerError("Library/Framework " + bin + " is not in bundle dir for " + filepath)

            # else:
            #     print('S--', file)