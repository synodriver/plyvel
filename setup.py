from os.path import join, dirname
from setuptools import setup
from setuptools.extension import Extension
from collections import defaultdict
from setuptools.command.build_ext import build_ext
import platform

try:
    from Cython.Build import cythonize
    has_cython = True
except ImportError:
    has_cython = False

CURRENT_DIR = dirname(__file__)

with open(join(CURRENT_DIR, 'plyvel/_version.py')) as fp:
    exec(fp.read(), globals(), locals())


def get_file_contents(filename):
    with open(join(CURRENT_DIR, filename)) as fp:
        return fp.read()


extra_compile_args = ['-Wall', '-g', '-x', 'c++', '-std=c++11']

if platform.system() == 'Darwin':
    extra_compile_args += ['-stdlib=libc++']

BUILD_ARGS = defaultdict(lambda: ["-O3", "-g0"])

for compiler, args in [
    ("msvc", ["/EHsc", "/DHUNSPELL_STATIC", "/Oi", "/O2", "/Ot"]),
    ("gcc", ["-O3", "-g0"]),
]:
    BUILD_ARGS[compiler] = args


class build_ext_compiler_check(build_ext):
    def build_extensions(self):
        compiler = self.compiler.compiler_type
        args = BUILD_ARGS[compiler]
        for ext in self.extensions:
            ext.extra_compile_args = args
        super().build_extensions()


if not has_cython:
    ext_modules = [
        Extension(
            'plyvel._plyvel',
            sources=['plyvel/_plyvel.cpp', 'plyvel/comparator.cpp'],
            libraries=['leveldb'],
            include_dirs=[r"D:\conda\envs\py310\Library\include"],
            library_dirs=[r"D:\conda\envs\py310\Library\lib", r"D:\conda\envs\py310\Library\bin"],
            extra_compile_args=extra_compile_args,
        )
    ]
else:
    ext_modules = cythonize([Extension(
        'plyvel._plyvel',
        sources=['plyvel/_plyvel.pyx', 'plyvel/comparator.cpp'],
        libraries=['leveldb'],
        include_dirs=[r"D:\conda\envs\py310\Library\include"],
        library_dirs=[r"D:\conda\envs\py310\Library\lib", r"D:\conda\envs\py310\Library\bin"],
        extra_compile_args=extra_compile_args)
    ], compiler_directives={
        "cdivision": True,
        "embedsignature": True,
        "boundscheck": False,
        "wraparound": False,
    }, )

setup(
    name='plyvel',
    description="Plyvel, a fast and feature-rich Python interface to LevelDB",
    long_description=get_file_contents('README.rst'),
    url="https://github.com/wbolster/plyvel",
    version=__version__,  # noqa: F821
    author="Wouter Bolsterlee",
    author_email="wouter@bolsterl.ee",
    ext_modules=ext_modules,
    packages=['plyvel'],
    license="BSD License",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Programming Language :: C++",
        "Programming Language :: Cython",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Database",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    cmdclass={"build_ext": build_ext_compiler_check},
)
