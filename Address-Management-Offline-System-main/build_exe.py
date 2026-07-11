import os
import shutil
import glob
import subprocess
import sys
import stat
import errno

def handle_remove_readonly(func, path, exc):
    import stat
    os.chmod(path, stat.S_IWRITE)
    func(path)

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Delete previous build artifacts
    print("Deleting old build artifacts...")
    for folder in ['build', 'dist']:
        path = os.path.join(root_dir, folder)
        if os.path.exists(path):
            shutil.rmtree(path, onerror=handle_remove_readonly)
            print(f"Deleted folder: {folder}/")
            
    for ext in ['*.spec', '*.exe']:
        for file in glob.glob(os.path.join(root_dir, ext)):
            os.remove(file)
            print(f"Deleted file: {os.path.basename(file)}")
            
    # 2. Entry point
    entry_point = "main.py"
    if not os.path.exists(os.path.join(root_dir, entry_point)):
        print(f"Error: Could not find entry point {entry_point}")
        return
        
    # 3 & 4. Generate fresh executable using PyInstaller
    print("Building fresh executable with PyInstaller...")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "ADRDE_Address_Management",
        "--add-data", f"assets{os.pathsep}assets",
        entry_point
    ]
    
    try:
        result = subprocess.run(cmd, check=True, cwd=root_dir, capture_output=True, text=True)
        print("PyInstaller completed successfully.")
    except subprocess.CalledProcessError as e:
        print("PyInstaller build failed!")
        print(e.stdout)
        print(e.stderr)
        return
        
    # Copy Database if exists
    print("Copying SQLite database to dist folder...")
    db_src = os.path.join(root_dir, 'data', 'address_management.db')
    dist_dir = os.path.join(root_dir, 'dist')
    if os.path.exists(db_src) and os.path.exists(dist_dir):
        db_dst = os.path.join(dist_dir, 'address_management.db')
        shutil.copy2(db_src, db_dst)
        print("Copied address_management.db to dist/")
    else:
        print("No existing database found in data/ or dist/ not found.")
        
    print("\n================ SUMMARY ================")
    print("- Deleted: build/, dist/, .spec, .exe files")
    print(f"- Build command: {' '.join(cmd)}")
    print("- Issues: None")
    print(f"- Output location: {os.path.join(dist_dir, 'ADRDE_Address_Management.exe')}")
    print("=========================================")

if __name__ == '__main__':
    main()
