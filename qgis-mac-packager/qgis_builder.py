# 2018 Peter Petrik (zilolv at gmail dot com)
# GNU General Public License 2 any later version

import argparse
import glob
import os
import shutil
import qgisBundlerTools.utils as utils
import git
import subprocess
import multiprocessing

class QGISBuildError(Exception):
    pass


class Progress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print('update(%s, %s, %s, %s)'%(op_code, cur_count, max_count, message))



parser = argparse.ArgumentParser(description='Build QGIS Application with cmake')

parser.add_argument('--output_directory',
                    required=True,
                    help='output directory for resulting QGIS.app files')
parser.add_argument('-clean', action='store_true', help="start from clean build directory")
parser.add_argument('--git',
                    required=True,
                    help='git branch/tag/changeset')

verbose = False

QGIS_REPO = "https://github.com/qgis/QGIS.git/"

args = parser.parse_args()

print("OUTPUT DIRECTORY: " + args.output_directory)
print("GIT: " + args.git)
print("CLEAN: " + str(args.clean))


outDir = os.path.realpath(args.output_directory)
if not os.path.exists(outDir):
    raise QGISBuildError(args.output_directory + " does not exists")

buildDir = os.path.join(outDir, "build")
qgisDir = os.path.join(outDir, "qgis")
installDir = os.path.join(outDir, "install")

cp = utils.CopyUtils(outDir)
print(100*"*")
print("STEP 1: Get QGIS repo " + args.git)
print(100*"*")
if not os.path.exists(qgisDir):
    os.makedirs(qgisDir)
os.chdir(qgisDir)
if os.listdir(qgisDir):
   # dir is not empty
    try:
        repo = git.Repo(qgisDir)
    except git.InvalidGitRepositoryError:
        raise QGISBuildError( qgisDir + 'isn`t git repo')
else:
    # clone
    print("Cloning...")
    git.Repo.clone_from(QGIS_REPO, qgisDir, progress=Progress())

repo = git.Repo(qgisDir)
g = git.Git(qgisDir)
g.checkout(args.git)
o = repo.remotes.origin
o.pull()

print(100*"*")
print("STEP 2: Clean the build/install directory ")
print(100*"*")
if args.clean:
    print ("Cleaning: " + buildDir)
    cp.recreate_dir(buildDir)
else:
    print("Skipped, clean build not requested")
    if not os.path.exists(buildDir):
        os.makedirs(buildDir)

if args.clean:
    print ("Cleaning: " + installDir)
    cp.recreate_dir(installDir)
else:
    print("Skipped, clean build not requested")
    if not os.path.exists(installDir):
        os.makedirs(installDir)

print(100*"*")
print("STEP 3: Generate CMAKE build system")
print(100*"*")
os.chdir(buildDir)

prefix_path = "/usr/local/opt/qt5;/usr/local/opt/qt5-webkit;/usr/local/opt/qscintilla2;/usr/local/opt/qwt;/usr/local/opt/qwtpolar;"
prefix_path += "/usr/local/opt/qca;/usr/local/opt/gdal2;/usr/local/opt/gsl;/usr/local/opt/geos;/usr/local/opt/proj;"
prefix_path += "/usr/local/opt/libspatialite;/usr/local/opt/spatialindex;/usr/local/opt/fcgi;/usr/local/opt/expat;"
prefix_path += "/usr/local/opt/sqlite;/usr/local/opt/flex;/usr/local/opt/bison;/usr/local/opt/libzip;"
prefix_path += "/usr/local/opt/libtasn1;/usr/local/opt/grass7;/usr/local/opt/exiv2"

for path in prefix_path.split(";"):
    if not os.path.exists(path):
        raise QGISBuildError("Missing " + path)

env = {
    "PATH": "/usr/local/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin"
}

args = ["cmake",
        "-DCMAKE_BUILD_TYPE=Release",
        "-DCMAKE_INSTALL_PREFIX="+os.path.realpath(installDir),
        "-DCMAKE_PREFIX_PATH="+prefix_path,
        "-DQGIS_MACAPP_BUNDLE=0",
        "-DWITH_3D=TRUE",
        "-DWITH_BINDINGS=TRUE",
        qgisDir
       ]

print("run cmake command:")
print(args)
print("env:")
print(env)

try:
    result = subprocess.run(args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Combine out/err into stdout; stderr will be None
                universal_newlines=True,
                check=True,
                env=env,
                encoding='UTF-8'
            )
    print(result.stdout)
except subprocess.CalledProcessError as err:
    print(err.output)
    raise

print(100*"*")
cores = multiprocessing.cpu_count() - 1
print("STEP 4: make on " + str(cores) + " cores")
print(100*"*")
os.chdir(buildDir)

os.system("make -j"+str(cores) + " install")

print("build done")