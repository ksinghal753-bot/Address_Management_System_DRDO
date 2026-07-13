[Setup]
AppName=ADRDE Address Management System
AppVersion=1.0.0
AppPublisher=ADRDE
DefaultDirName={autopf}\ADRDE Address Management System
DefaultGroupName=ADRDE Address Management System
OutputDir=dist
OutputBaseFilename=AddressManagementSystem_Setup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\Address_Management_System.exe
SetupIconFile=compiler:SetupClassicIcon.ico

[Files]
Source: "dist\Address_Management_System.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\ADRDE Address Management System"; Filename: "{app}\Address_Management_System.exe"
Name: "{commondesktop}\ADRDE Address Management System"; Filename: "{app}\Address_Management_System.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Run]
Filename: "{app}\Address_Management_System.exe"; Description: "{cm:LaunchProgram,ADRDE Address Management System}"; Flags: nowait postinstall skipifsilent
