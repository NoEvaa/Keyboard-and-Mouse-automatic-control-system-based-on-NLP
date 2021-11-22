# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(6000)
block_cipher = None


a = Analysis(['main.py'],
             pathex=['yZmainui.py', 'yZagguibase.py', 'yZagguisenior.py', 'yZagcompile.py', 'yZagerrors.py', 'yZaginf.py', 'yZagtools.py', 'yZagnlpcore.py', 'yZnlp_ie.py', 'yZnlp_tc.py', 'yZagvoicer.py', 'yZnlp_voicer.py', 'E:\\project2'],
             binaries=[('Icon.ico', '.')],
             datas=[],
             hiddenimports=['random', 'jieba', 'nltk', 'numpy', 'sklearn', 'copy', 'tkinter', 'pyautogui', 'time', 'pickle', 'json', 're', 'speech_recognition', 'aip', 'requests'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
		  icon='Icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
