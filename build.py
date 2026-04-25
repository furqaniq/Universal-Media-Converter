"""Build script for packaging the app with PyInstaller."""

import PyInstaller.__main__
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")

PyInstaller.__main__.run(
    [
        os.path.join(SRC_DIR, "main.py"),
        "--name=UniversalMediaConverter",
        "--onefile",
        "--windowed",
        "--add-data",
        f"{os.path.join(BASE_DIR, 'assets')};assets",
        "--distpath",
        os.path.join(BASE_DIR, "dist"),
        "--workpath",
        os.path.join(BASE_DIR, "build"),
        "--specpath",
        BASE_DIR,
    ]
)
