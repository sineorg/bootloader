import os
import zipfile

def zip_folder_contents(folder_name):
    if not os.path.isdir(folder_name):
        print(f"Folder '{folder_name}' does not exist.")
        return

    zip_filename = f"{folder_name}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_name):
            # Add empty directories
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if not os.listdir(dir_path):
                    relative_path = os.path.relpath(dir_path, folder_name)
                    zipf.write(dir_path, relative_path + '/')

            # Add files
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, folder_name)
                zipf.write(file_path, relative_path)

    print(f"Created {zip_filename} with contents of '{folder_name}'.")

zip_folder_contents('profile')
zip_folder_contents('program')
