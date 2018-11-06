# 2018 Peter Petrik (zilolv at gmail dot com)
# GNU General Public License 2 any later version

import argparse
import os
import subprocess

thisDir = os.path.dirname(os.path.realpath(__file__))
resourcesDir = os.path.join(thisDir, "resources")


class QGISPackageError(Exception):
    pass


parser = argparse.ArgumentParser(description='Package QGIS Application')

parser.add_argument('--output_directory',
                    required=True,
                    help='output directory with resulting QGIS.app files')
parser.add_argument('--timestamp', required=True)

pkg = False
dmg = True

args = parser.parse_args()
print("OUTPUT DIRECTORY: " + args.output_directory)

qgisApp = os.path.join(args.output_directory, "QGIS.app")

if not os.path.exists(qgisApp):
    raise QGISPackageError(qgisApp + " does not exists")

# TODO SIGN?
if pkg:
    print(100*"*")
    print("STEP: Create pkg installer")
    print(100*"*")
    pkgFile = args.output_directory + "/qgis_" + args.timestamp +".pkg"
    if os.path.exists(pkgFile):
        print("Removing old pkg")
        os.remove(pkgFile)

    args = ["productbuild",
            "--identifier", "co.uk.lutraconsulting.qgis",
            "--component", qgisApp,
            "/Applications",
            pkgFile
            ]
    subprocess.check_output(args)
    fsize = subprocess.check_output(["du", "-h", pkgFile])
    print("pkg done: \n" + fsize)

if dmg:
    print(100*"*")
    print("STEP: Create dmg image")
    print(100*"*")
    dmgFile = args.output_directory + "/qgis_" + args.timestamp +".dmg"
    if os.path.exists(dmgFile):
        print("Removing old dmg")
        os.remove(dmgFile)

    args = ["create-dmg",
            "--volname", "QGIS Installer",
            "--volicon", resourcesDir + "/QGIS.icns",
            "--background", resourcesDir + "/background.jpg",
            "--window-pos", "200", "120",
            "--window-size", "800", "600",
            "--icon-size", "120",
            "--icon", resourcesDir + "/qgis-icon-120x120.png" ,"200", "190",
            "--hide-extension", "QGIS.app",
            "--app-drop-link", "600", "185",
            "--eula", resourcesDir + "/EULA.txt",
            dmgFile,
            qgisApp + "/"
            ]

    subprocess.check_output(args)

    # TODO
    # args= ["codesign",
    #        "-s", "$CODESIGN_IDENTITY",
    #        "-v",
    #        dmgFile]

    fsize = subprocess.check_output(["du", "-h", dmgFile])
    print("ALL DONE\n" + fsize)
