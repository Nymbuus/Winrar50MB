import zipfile
import subprocess
import os
import re


def Unzip(zip_path):
    output_folder_name = zip_path.split("\\")[-1].split(".")[0]
    extract_path = r"C:\SWIFT\Program\ADB\MyProgramTest\ExtractedFiles" + "\\" + output_folder_name  # Destination folder
    print(extract_path)

    
    output_folders = [
        os.path.join(extract_path, file)
        for file in os.listdir()
    ]

    # Extract ZIP
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    except:
        extract_path = "skip"
        output_folder_name = "skip"
        print("Skipping this file.")
    else:
        print("Extraction complete!")
    return extract_path, output_folder_name


def Zip50MB(folder_to_compress, folder_name): 
    # Configuration
    winrar_path = r"C:\Program Files\WinRAR\WinRAR.exe"  # Adjust if needed
    output_rar = r"C:\SWIFT\Program\ADB\MyProgramTest\RarParts" + "\\" + folder_name + ".rar"
    split_size = "50m"  # Change size (e.g., "500m" for 500MB, "2g" for 2GB)

    # Ensure output directory exists
    output_dir = os.path.dirname(output_rar)
    os.makedirs(output_dir, exist_ok=True)

    # WinRAR command for splitting
    command = [
        winrar_path, "a", "-m5", "-v" + split_size, "-ep1", output_rar, folder_to_compress
    ]

    # Execute command
    subprocess.run(command)

    print("Compression complete!")


def ReZiping():
    original_zip_folder = r"C:\SWIFT\Program\ADB\bug_reports_pending"
    modified_rar_folder = r"C:\SWIFT\Program\ADB\MyProgramTest\RarParts"

    
    # Function to clean filenames
    def clean_filename(filename):
        name, _ = os.path.splitext(filename)  # Remove extension
        name = re.sub(r".part01", "", name)  # Remove unwanted endings
        return name

    # Get all RAR files
    modified_rar_names = {clean_filename(file) for file in os.listdir(modified_rar_folder)
                          if not file.endswith(".part02.rar")
                             or not file.endswith(".part03.rar")
                             or not file.endswith(".part04.rar")
                             or not file.endswith(".part05.rar")}

    # Find ZIPs that need modification
    zips_to_modify = [
        os.path.join(original_zip_folder, file)
        for file in os.listdir(original_zip_folder)
        if file.endswith(".zip") and clean_filename(file) not in modified_rar_names
    ]

    for zip_path in zips_to_modify:
        extracted_path, folder_name = Unzip(zip_path)
        if extracted_path != "skip" or folder_name != "skip":
            Zip50MB(extracted_path, folder_name)


def ADBExtraction():
    folder_path = r"C:\SWIFT\Program\ADB"
    os.chdir(folder_path)  # Change working directory

    subprocess.run("adb root", shell=True)
    subprocess.run("adb remount", shell=True)
    subprocess.run("adb pull /data/user/0/com.volvocars.bugreport/bug_reports_pending/", shell=True)


ADBExtraction()
ReZiping()