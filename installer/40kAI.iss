; 40kAI Windows installer (Inno Setup 6)
; Сборка: scripts\build_installer.bat

#define MyAppName "40kAI"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "40kAI"
#define MyAppExeName "40kAI_GUI.exe"
#define MyGuiSubDir "40kAI_GUI"
#define RepoRoot ".."

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=output
OutputBaseFilename=Install
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#MyGuiSubDir}\{#MyAppExeName}

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Tasks]
Name: "desktopicon"; Description: "Создать ярлык на рабочем столе"; GroupDescription: "Дополнительно:"; Flags: checkedonce

[Files]
; GUI (PyInstaller onedir)
Source: "{#RepoRoot}\dist\{#MyGuiSubDir}\*"; DestDir: "{app}\{#MyGuiSubDir}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Приложение
Source: "{#RepoRoot}\app\*"; DestDir: "{app}\app"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "__pycache__\*,*.pyc,gui_qt\.icon_cache\*"
Source: "{#RepoRoot}\core\*"; DestDir: "{app}\core"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "__pycache__\*,*.pyc"
Source: "{#RepoRoot}\configs\*"; DestDir: "{app}\configs"; Flags: ignoreversion recursesubdirs createallsubdirs skipifsourcedoesntexist
Source: "{#RepoRoot}\data\*"; DestDir: "{app}\data"; Flags: ignoreversion recursesubdirs createallsubdirs skipifsourcedoesntexist
Source: "{#RepoRoot}\scripts\*"; DestDir: "{app}\scripts"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "__pycache__\*,*.pyc"
Source: "{#RepoRoot}\*.py"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "{#RepoRoot}\*.bat"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "{#RepoRoot}\project_paths.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#RepoRoot}\requirements_windows.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#RepoRoot}\installer\install_deps.bat"; DestDir: "{app}"; DestName: "install_deps.bat"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyGuiSubDir}\{#MyAppExeName}"; WorkingDir: "{app}"
Name: "{group}\Установить зависимости"; Filename: "{sys}\cmd.exe"; Parameters: "/c ""{app}\install_deps.bat"" -y"; WorkingDir: "{app}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyGuiSubDir}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyGuiSubDir}\{#MyAppExeName}"; Description: "Запустить {#MyAppName}"; Flags: nowait postinstall skipifsilent shellexec; WorkingDir: "{app}"

[Code]
function PythonAvailable: Boolean;
var
  ResultCode: Integer;
begin
  Result := Exec(ExpandConstant('{cmd}'), '/c python --version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode)
    and (ResultCode = 0);
  if not Result then
    Result := Exec(ExpandConstant('{cmd}'), '/c py -3.12 --version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode)
      and (ResultCode = 0);
end;

function InitializeSetup: Boolean;
begin
  if not PythonAvailable then
  begin
    MsgBox(
      'Для установки зависимостей нужен Python 3.12+ в PATH.' + #13#10 +
      'Установите Python с python.org и отметьте "Add to PATH", затем повторите.',
      mbError, MB_OK);
    Result := False;
  end
  else
    Result := True;
end;

function RunDependencyUpdater: Boolean;
var
  ResultCode: Integer;
  Cmd, Params: string;
begin
  Cmd := ExpandConstant('{cmd}');
  Params := '/c python "' + ExpandConstant('{app}\scripts\updater\install_or_update.py') +
    '" --root "' + ExpandConstant('{app}') + '" -y --torch-variant auto';
  Result := Exec(Cmd, Params, ExpandConstant('{app}'), SW_SHOW, ewWaitUntilTerminated, ResultCode)
    and (ResultCode = 0);
  if not Result then
  begin
    Params := '/c py -3.12 "' + ExpandConstant('{app}\scripts\updater\install_or_update.py') +
      '" --root "' + ExpandConstant('{app}') + '" -y --torch-variant auto';
    Result := Exec(Cmd, Params, ExpandConstant('{app}'), SW_SHOW, ewWaitUntilTerminated, ResultCode)
      and (ResultCode = 0);
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    if not RunDependencyUpdater then
      MsgBox(
        'Зависимости установлены с ошибкой. Позже запустите:' + #13#10 +
        ExpandConstant('{app}\install_deps.bat'),
        mbInformation, MB_OK);
  end;
end;
