@echo off
chcp 65001 >nul 2>&1
setlocal EnableExtensions EnableDelayedExpansion
REM Репозиторий: bat в installer\ → корень ..\
REM После Install.exe: bat в {app}\ → корень = эта же папка
if exist "%~dp0scripts\updater\install_or_update.py" (
  cd /d "%~dp0"
) else (
  cd /d "%~dp0.."
)
set "ROOT=%cd%"

REM install_deps.bat — установка зависимостей 40kAI
REM
REM PyTorch (сборка):
REM   (без аргументов)  — автоопределение GPU + меню выбора (Enter = авто)
REM   auto  или  -y     — авто без меню
REM   cpu               — только CPU (PyPI)
REM   cu128 / cu126 / cu124 / cu121 — принудительно CUDA с pytorch.org

set "TORCH_CUDA=%~1"
set "SKIP_MENU=0"

if /i "%TORCH_CUDA%"=="auto" set "TORCH_CUDA=" & set "SKIP_MENU=1"
if /i "%TORCH_CUDA%"=="-y" set "TORCH_CUDA=" & set "SKIP_MENU=1"
if /i "%TORCH_CUDA%"=="ask" set "TORCH_CUDA=" & set "SKIP_MENU=0"

if /i "%TORCH_CUDA%"=="cpu" set "SKIP_MENU=1"
if /i "%TORCH_CUDA%"=="cu128" set "SKIP_MENU=1"
if /i "%TORCH_CUDA%"=="cu126" set "SKIP_MENU=1"
if /i "%TORCH_CUDA%"=="cu124" set "SKIP_MENU=1"
if /i "%TORCH_CUDA%"=="cu121" set "SKIP_MENU=1"

where python >nul 2>&1
if errorlevel 1 (
  echo [install_deps] Python not found in PATH. Install Python 3.12+.
  exit /b 1
)

echo [install_deps] Root: %ROOT%
for /f "delims=" %%v in ('python -c "import sys; print('{}.{}'.format(sys.version_info.major, sys.version_info.minor))"') do (
  echo [install_deps] Python %%v
)

call :detect_torch_variant
if not defined DETECTED_VARIANT set "DETECTED_VARIANT=cpu"
if not defined DETECT_REASON set "DETECT_REASON=GPU detection failed"

if "%SKIP_MENU%"=="0" if "%TORCH_CUDA%"=="" call :menu_torch_variant
if not "%TORCH_CUDA%"=="" (
  echo [install_deps] PyTorch: manual - %TORCH_CUDA%
) else (
  set "TORCH_CUDA=!DETECTED_VARIANT!"
  echo [install_deps] PyTorch: auto - !TORCH_CUDA! ^(!DETECT_REASON!^)
)

echo [install_deps] Installing / updating packages...
python "%ROOT%\scripts\updater\install_or_update.py" --root "%ROOT%" --torch-variant "%TORCH_CUDA%" -y
if errorlevel 1 exit /b 1

call "%ROOT%\.venv\Scripts\activate.bat"

echo.
echo [install_deps] Checking PyTorch...
python -c "import torch; v=getattr(torch,'__version__','?'); c=torch.cuda.is_available(); n=torch.cuda.get_device_name(0) if c else ''; print('  torch', v); print('  CUDA:', c, ('('+n+')') if n else '')"

echo.
echo [install_deps] Done. Package versions:
python -m pip show gym gymnasium matplotlib numpy imageio tqdm pandas scipy torch PySide6 numba 2>nul | findstr /i "Name: Version:"

endlocal
exit /b 0

:detect_torch_variant
set "DETECTED_VARIANT=cpu"
set "DETECT_REASON=no NVIDIA GPU"
for /f "usebackq tokens=1-5 delims=|" %%a in (`python "%ROOT%\scripts\detect_torch_variant.py"`) do (
  set "DETECTED_VARIANT=%%a"
  set "DETECT_GPU=%%b"
  set "DETECT_CUDA_MAJ=%%c"
  set "DETECT_CUDA_MIN=%%d"
  set "DETECT_STATUS=%%e"
)
if /i "!DETECT_STATUS!"=="ok" (
  set "DETECT_REASON=GPU: !DETECT_GPU!; driver CUDA !DETECT_CUDA_MAJ!.!DETECT_CUDA_MIN!"
) else if /i "!DETECT_STATUS!"=="no_gpu" (
  set "DETECT_REASON=NVIDIA GPU not found"
) else if /i "!DETECT_STATUS!"=="no_smi" (
  set "DETECT_REASON=nvidia-smi not found ^(install NVIDIA driver^)"
) else if /i "!DETECT_STATUS!"=="no_cuda_ver" (
  set "DETECT_REASON=GPU: !DETECT_GPU!; CUDA version unknown, using cu128"
) else if /i "!DETECT_STATUS!"=="error" (
  set "DETECT_REASON=GPU check error"
) else (
  set "DETECT_REASON=no NVIDIA GPU / nvidia-smi"
)
exit /b 0

:menu_torch_variant
echo.
echo ============================================================
echo   PyTorch build selection
echo ============================================================
echo   Auto-detected: !DETECTED_VARIANT!  -  !DETECT_REASON!
echo.
echo   [1] Auto  - use detection above ^(recommended^)
echo   [2] CPU   - no CUDA, PyPI wheel
echo   [3] cu128 - NVIDIA, CUDA 12.8+ ^(newer drivers^)
echo   [4] cu126 - NVIDIA, CUDA 12.6+
echo   [5] cu124 - NVIDIA, CUDA 12.4+
echo   [6] cu121 - NVIDIA, CUDA 12.1
echo.
set "MENU_CHOICE="
set /p "MENU_CHOICE=Your choice [1]: "
if "!MENU_CHOICE!"=="" set "MENU_CHOICE=1"
if "!MENU_CHOICE!"=="1" set "TORCH_CUDA=!DETECTED_VARIANT!" & goto :menu_done
if "!MENU_CHOICE!"=="2" set "TORCH_CUDA=cpu" & goto :menu_done
if "!MENU_CHOICE!"=="3" set "TORCH_CUDA=cu128" & goto :menu_done
if "!MENU_CHOICE!"=="4" set "TORCH_CUDA=cu126" & goto :menu_done
if "!MENU_CHOICE!"=="5" set "TORCH_CUDA=cu124" & goto :menu_done
if "!MENU_CHOICE!"=="6" set "TORCH_CUDA=cu121" & goto :menu_done
echo [install_deps] Invalid input, using auto: !DETECTED_VARIANT!
set "TORCH_CUDA=!DETECTED_VARIANT!"
:menu_done
exit /b 0
