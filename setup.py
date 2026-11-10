"""Build extension for compiling Cython"""
import os
#from pathlib import Path
from os.path import join

from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
from numpy import get_include


EXTERNAL              = "external"
SRCDIR                = "src"
INCDIR                = "include"

CYTHON_LANGUAGE_LEVEL = 3
CYTHON_LANGUAGE       = "c++"
CYTHON_INCLUDES       = [
                         INCDIR,
                         join(EXTERNAL, "signalsmith-stretch")
                        ]

if os.name == 'nt':  # Windows (MSVC)
    CYTHON_COMPILE_ARGS = ['/O2', '/Oi', '/Ot', '/arch:AVX2']
else:  # Linux / macOS (GCC / Clang)
    CYTHON_COMPILE_ARGS = ['-O2', '-march=native', '-ffast-math']

'''
def find_pyx(base_dir) -> list[Extension]:
    extensions = []
    base_path = Path(base_dir)

    for pyx_file in base_path.rglob("*.pyx"):
        rel_path = pyx_file.relative_to(base_path.parent)
        module_name = str(rel_path.with_suffix('')).replace(os.sep, '.')

        ext = Extension(
            module_name,
            sources=[str(pyx_file)],
            include_dirs=[get_include()] + CYTHON_INCLUDES,
            extra_compile_args=["-O2"], # 2 optimization level
            language=CYTHON_LANGUAGE
        )
        extensions.append(ext)
    return extensions

def find_all(path=".") -> list[Extension]:
    print("Scanning Cython packages...")
    ext_modules = []

    pkgs = find_packages(path)
    for pkg in pkgs:
        print(f"Scanning {pkg}...")
        ext_modules += find_pyx(Path(pkg))
    print("Found", str(len(ext_modules)), "Cython sources")

    return ext_modules
'''

extensions = [
    Extension(
        "osm_player.sampler",
        sources=[join("osm_player", "sampler.pyx")],
        include_dirs=[get_include()] + CYTHON_INCLUDES,
        extra_compile_args=CYTHON_COMPILE_ARGS,
        language=CYTHON_LANGUAGE
    ),
    Extension(
        "osm_player._stretch",
        sources=[join("osm_player", "_stretch.pyx"), join(SRCDIR, "stretch_wrapper.cpp")],
        include_dirs=[get_include()] + CYTHON_INCLUDES,
        extra_compile_args=CYTHON_COMPILE_ARGS,
        language=CYTHON_LANGUAGE
    ),
    Extension(
        "osm_player.stretch",
        sources=[join("osm_player", "stretch.pyx")],
        include_dirs=[get_include()] + CYTHON_INCLUDES,
        extra_compile_args=CYTHON_COMPILE_ARGS,
        language=CYTHON_LANGUAGE
    )
]

setup(
    packages=find_packages(),
    ext_modules=cythonize(extensions,
                          compiler_directives={'language_level': CYTHON_LANGUAGE_LEVEL}
                         )
)
