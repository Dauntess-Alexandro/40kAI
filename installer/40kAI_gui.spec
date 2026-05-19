# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec: 40kAI GUI (PySide6 + QML)
import os
from pathlib import Path

ROOT = Path(SPEC).resolve().parent.parent
GUI = ROOT / "app" / "gui_qt"

a = Analysis(
    [str(GUI / "main.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[
        (str(GUI / "qml"), "qml"),
        (str(GUI / "assets"), "assets"),
    ],
    hiddenimports=[
        "PySide6.QtQuick",
        "PySide6.QtQml",
        "PySide6.QtQuickControls2",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "torch",
        "torchvision",
        "torchaudio",
        "matplotlib",
        "scipy",
        "pandas",
        "gym",
        "gymnasium",
        "numba",
        "imageio",
        "tqdm",
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="40kAI_GUI",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(GUI / "assets" / "40kai_icon.ico"),
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="40kAI_GUI",
)
