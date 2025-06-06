#!/usr/bin/env python

import argparse
import os
import shutil


def setup_igrf():
    if os.path.exists("igrf"):
        shutil.rmtree("igrf")
    os.system("git clone https://github.com/space-physics/igrf")
    os.chdir("igrf/")
    os.system("python -m pip install -e .")
    shutil.rmtree("igrf/.git/")
    shutil.rmtree("igrf/.github/")
    return


def clean():
    if os.path.exists("dist/"):
        shutil.rmtree("dist/")
    if os.path.exists("build/"):
        shutil.rmtree("build/")
    if os.path.exists("raid.egg-info/"):
        shutil.rmtree("raid.egg-info/")
    os.system("find . -type d -name '.ipynb_checkpoints' -exec rm -rf {} +")
    os.system("find . -type d -name '__pycache__' -exec rm -rf {} +")
    return


def build():
    os.system("isort -rc -sl .")
    os.system("autoflake --remove-all-unused-imports -i -r .")
    os.system("isort -rc -m 3 .")
    os.system("black .")
    os.system("python setup.py sdist bdist_wheel")
    return


def uplaod_pip():
    clean()
    build()
    # -u __token__ -p pypi-a3d6fd70-4f7e-4428-905c-3e53d3ae1176
    os.system("python -m twine upload dist/* --verbose")
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--igrf_build", action="store_true", help="Build the IGRF from scratch"
    )
    parser.add_argument(
        "-b", "--build", action="store_true", help="Build the project from scratch"
    )
    parser.add_argument(
        "-rm", "--clean", action="store_true", help="Cleaning pre-existing files"
    )
    parser.add_argument(
        "-rb",
        "--rebuild",
        action="store_true",
        help="Clean and rebuild the project from scratch",
    )
    parser.add_argument(
        "-upip",
        "--upip",
        action="store_true",
        help="Upload code to PIP repository",
    )
    args = parser.parse_args()
    if args.igrf_build:
        setup_igrf()
    if args.clean:
        clean()
    if args.build:
        build()
    if args.rebuild:
        clean()
        build()
    if args.upip:
        uplaod_pip()
