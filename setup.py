#! /usr/bin/python

import sys
import os

def main():
    if len(sys.argv) != 2:
        print("Usage: setup.py /path/to/picpython/lib")

    compiled = ["pkg-config-0.28", "tcl8.5.15"  , "tk8.5.15"       ,
                "zlib-1.2.8"     , "szip-2.1"   , "freetype-2.5.3" ,
                "hdf5-1.8.13"    , "Python-2.7" , "jpeg-6b"        ,
                "geos-3.4.2"]

    pyinstalls = ["numpy-1.8.1"   , "pexpect-2.3"     , "pmw"          ,
                  "Imaging-1.1.7" , "matplotlib-1.3.1", "basemap-1.0.7",
                  "Pyrex-0.9.9"   , "tables-3.1.1"    , "pyserial-2.7",
                  "numexpr-2.2.2" , "Cython-0.20.1"]

    set_environment_vars()

    for package in compiled:
        build(package)
    
    for package in pyinstalls:
        pyinstall(package)

def build(package):
    os.chdir("./" + package)
    configure(package)

    os.system("make")
    os.system("make install")

    if package.startswith("jpeg"):
        make_bin_dir()
    elif package.startswith("Python"):
        create_sym_links()

    os.chdir("..")

    if package.startswith("tk") or package.startswith("tcl"):
        os.chdir("..")

def pyinstall(package):
    os.chdir("./" + package)
    if package.startswith("numpy"):
        create_site()
    elif package.startswith("matplotlib"):
        os.system("cp setup.cfg.template setup.cfg")
    elif package.startswith("tables"):
        os.system('picpython setup.py build --hdf5={0} --lflags="-Xlinker -rpath"')
    os.system("picpython setup.py install")
    os.chdir("..")

def configure(package):
    configstr = "./configure --prefix=" + sys.argv[1]
    if package.startswith("tcl"):
        os.chdir("./unix")
        configstr = "./configure --enable-framework --enable-threads"
    elif package.startswith("tk"):
        os.chdir("./unix")
        configstr = "./configure --enable-framework --with-x --enable-threads"
    elif package.startswith("libpng"):
        configstr += " --libdir={0}/lib --includedir={0}/include".format(sys.argv[1])

    os.system(configstr)

def create_sym_links():
    os.system("ln -s " + sys.argv[1] + "/bin/python " 
              + sys.argv[1] + "/bin/picpython")
    os.system("ln -s " + sys.argv[1] + "/bin/picpython " 
              + "/usr/bin/picpython")

def create_site():
    with open("site.cfg", "w") as site:
        site.write("[DEFAULT]")
        site.write("library_dirs=" + sys.argv[1] + "/lib")
        site.write("library_dirs=" + sys.argv[1] + "/include")

def set_environment_vars():
    os.environ["GEOS_DIR"] = sys.argv[1]
    os.environ["HDF5_DIR"] = sys.argv[1]
    os.environ["PKG_CONFIG_PATH"] = sys.argv[1] + "/lib/pkgconfig"
    os.environ["CFLAGS"] = "-Wall -O -funroll-loops -malign-loops=2 -malign-functions=2"

def make_bin_dir():
    directory = sys.argv[1] + "/bin"

    if not os.path.exists(directory):
        os.makedirs(directory)

if __name__ == '__main__':
    main()