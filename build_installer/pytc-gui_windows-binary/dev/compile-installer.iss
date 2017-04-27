; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define DirectoryRoot "C:\Users\harmsm\Desktop"
#define MyAppName "pytc-gui"
#define MyAppVersion "1.0.1"
#define MyAppPublisher "Harms Lab, University of Oregon"
#define MyAppURL "https://github.com/harmslab/pytc-gui"
#define MyAppExeName "python.exe"
#define MyAppBits "64"
#define MyAppPythonSuffix ".amd64"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{EFB207FC-5A76-438B-BA7C-9FB86060ED5D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile={#DirectoryRoot}\pytc-gui_windows-binary\dev\LICENSE.txt
InfoBeforeFile={#DirectoryRoot}\pytc-gui_windows-binary\dev\pre-install-prompt.txt
InfoAfterFile={#DirectoryRoot}\pytc-gui_windows-binary\dev\post-install-prompt.txt
OutputBaseFilename=pytc-gui_v{#MyAppVersion}_setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "{#DirectoryRoot}\pytc-gui_windows-binary\pytc-gui\*"; DestDir: "{app}"; Flags: ignoreversion createallsubdirs recursesubdirs 

[Icons]
Name: "{commonprograms}\{#MyAppName}"; Filename: "{app}\winpython{#MyAppBits}\python-3.6.1{#MyAppPythonSuffix}\python.exe"; WorkingDir: "{app}"; Parameters: """{app}\winpython{#MyAppBits}\python-3.6.1{#MyAppPythonSuffix}\Scripts\pytc-gui.exe"""; IconFilename: "{app}\favicon.ico"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\winpython{#MyAppBits}\python-3.6.1{#MyAppPythonSuffix}\python.exe"; WorkingDir: "{app}"; Parameters: """{app}\winpython{#MyAppBits}\python-3.6.1{#MyAppPythonSuffix}\Scripts\pytc-gui.exe"""; IconFilename: "{app}\favicon.ico"; Tasks: desktopicon
