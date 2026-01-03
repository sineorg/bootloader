import os
import shutil
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

program_path = os.getenv('PROGRAM')
profile_path = os.getenv('PROFILE')

if not program_path or not profile_path:
    raise ValueError("Missing PROGRAM or PROFILE in .env")

# Source folders
utils_src = os.path.join('.', 'utils')
program_src = os.path.join('.', 'program')

if not os.path.isdir(utils_src):
    raise FileNotFoundError(f"Missing ./utils at {utils_src}")
if not os.path.isdir(program_src):
    raise FileNotFoundError(f"Missing ./program at {program_src}")

# Destination paths
chrome_utils_dest = os.path.join(profile_path, 'chrome', 'utils')

# Ensure chrome dir exists
os.makedirs(os.path.join(profile_path, 'chrome'), exist_ok=True)

# Overwrite utils entirely
if os.path.exists(chrome_utils_dest):
    shutil.rmtree(chrome_utils_dest)
shutil.copytree(utils_src, chrome_utils_dest)

# Ensure PROGRAM dir exists
os.makedirs(program_path, exist_ok=True)

def merge_copy(src, dst):
    """
    Recursively copy src into dst with merge semantics:
    - If a file/directory doesn't exist in dst, copy it.
    - If a file exists in dst with the same name, overwrite the file.
    - If a directory exists in dst with the same name, recurse (do not delete other contents).
    - Do NOT remove anything that exists only in dst.
    """
    for name in os.listdir(src):
        s = os.path.join(src, name)
        d = os.path.join(dst, name)
        if os.path.isdir(s):
            # If destination is a file with same name, replace it with a directory copy
            if os.path.isfile(d):
                os.remove(d)
            if not os.path.exists(d):
                # If directory doesn't exist, copy whole subtree
                shutil.copytree(s, d)
            else:
                # Directory exists: recurse without deleting other contents
                merge_copy(s, d)
        else:
            # s is a file: ensure parent exists then copy (overwrite)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)

# Merge copy contents of ./program into PROGRAM (no deletions of existing items)
merge_copy(program_src, program_path)

print("Done: utils overwritten and program merged without deleting existing items.")
