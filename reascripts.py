import os
from dotenv import load_dotenv

# load .env from project root
load_dotenv()

# now pulled from your .env (with a fallback if missing)
# Ensure REAPER_PATH is correct and accessible.
# If REAPER_PATH points to a system directory (e.g., Program Files on Windows, /usr/bin on Linux/macOS),
# you might need to run the script with administrator/sudo privileges.
REAPER_PATH = os.getenv("REAPER_PATH") or "/default/path/to/REAPER"
# For testing, you can print this path to verify it's what you expect:
# print(f"REAPER_PATH is set to: {REAPER_PATH}")

def register_scripts():
    """
    Registers custom scripts into REAPER's reaper-kb.ini file.
    Handles potential PermissionError exceptions during file operations.
    """
    custom_scripts_dir = "./custom_scripts"
    
    try:
        # Attempt to list files in the custom_scripts directory.
        # Potential PermissionError if the script doesn't have read access to this directory.
        print(f"Attempting to list scripts in: {os.path.abspath(custom_scripts_dir)}")
        my_scripts = os.listdir(custom_scripts_dir)
        if not my_scripts:
            print(f"No scripts found in {custom_scripts_dir}. Please ensure scripts exist there.")
            return
        print(f"Found scripts: {my_scripts}")
    except FileNotFoundError:
        print(f"Error: The directory '{custom_scripts_dir}' was not found.")
        print("Please ensure this directory exists in the same location as your script, or provide the correct path.")
        return
    except PermissionError:
        print(f"PermissionError: Could not access the directory '{custom_scripts_dir}'.")
        print("Please check if you have read permissions for this directory.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while listing scripts: {e}")
        return

    # Construct the path to reaper-kb.ini
    # Ensure REAPER_PATH is correctly set in your .env file or the default is appropriate.
    custom_script_path = os.path.join(REAPER_PATH, "reaper-kb.ini")
    print(f"Target configuration file: {custom_script_path}")

    # Get the current working directory to build absolute paths for scripts
    cwd = os.getcwd()

    for filename in my_scripts:
        # Original line: filepath = os.path.join(cwd, "tools", filename)
        # Corrected to use custom_scripts_dir as the base for the script files.
        # If your scripts are indeed in a "tools" subdirectory relative to cwd,
        # then the original line was correct. However, typically, if you list files
        # from "./custom_scripts", the full path would also be based on that.
        script_source_path = os.path.join(custom_scripts_dir, filename)
        filepath = os.path.abspath(script_source_path) # Get absolute path
        
        # Check if the script file actually exists before trying to add it
        if not os.path.isfile(filepath):
            print(f"Warning: Script file '{filename}' not found at '{filepath}'. Skipping.")
            continue

        custom_string = f'SCR 4 0 jj_{filename.replace(".", "_")} "allday_script: {filename}" "{filepath}"' # Ensure filename in ID is safe
        print(f"Preparing to add/check entry for: {filename}")

        try:
            # Attempt to open, read, and possibly write to reaper-kb.ini.
            # This is a common place for PermissionError if the script doesn't have
            # read/write access to this file or its directory.
            
            # First, check if the directory for reaper-kb.ini exists
            reaper_config_dir = os.path.dirname(custom_script_path)
            if not os.path.isdir(reaper_config_dir):
                print(f"Error: The directory for REAPER configuration '{reaper_config_dir}' does not exist.")
                print(f"Please ensure REAPER_PATH ('{REAPER_PATH}') is set correctly.")
                return # Stop if the directory doesn't exist

            # Check if the file exists, create if not (though REAPER usually creates this)
            if not os.path.exists(custom_script_path):
                print(f"Warning: '{custom_script_path}' not found. Attempting to create it.")
                # If the file doesn't exist, we can't read it, so just open in 'w' to create, then 'a' to append.
                # However, the logic below assumes it might exist and reads from it.
                # For simplicity, let's assume REAPER creates this file. If not, writing directly might be an issue.
                # A robust solution might involve creating it with some default content if absolutely necessary.
                # For now, we'll proceed assuming it should exist or be creatable.
                try:
                    with open(custom_script_path, 'a') as ini_file_test_create: # Try to create/touch file
                        pass # Just ensure it can be opened for append (which creates if not exists)
                    print(f"Successfully touched/created '{custom_script_path}' (if it was missing).")
                except PermissionError:
                    print(f"PermissionError: Could not create or access '{custom_script_path}'.")
                    print("Please check write permissions for the directory and file.")
                    continue # Skip this script if config file is inaccessible

            # Proceed with r+
            with open(custom_script_path, 'r+') as ini_file:
                existing_content = ini_file.read()
                if custom_string in existing_content:
                    print(f"Script '{filename}' already registered. Skipping.")
                    continue
                
                # If not found, go to the beginning and prepend the new script line
                ini_file.seek(0)
                ini_file.write(custom_string + "\n" + existing_content)
                print(f"Successfully registered script: {filename}")

        except PermissionError:
            print(f"PermissionError: Could not read/write to '{custom_script_path}'.")
            print("Please check if you have read and write permissions for this file and its directory.")
            print(f"Try running the script with administrator/sudo privileges if '{REAPER_PATH}' is a protected location.")
            continue # Continue to the next script if this one fails
        except FileNotFoundError:
            print(f"Error: The REAPER configuration file '{custom_script_path}' was not found during r+ open.")
            print(f"Please ensure REAPER_PATH ('{REAPER_PATH}') is correct and the file exists.")
            continue
        except Exception as e:
            print(f"An unexpected error occurred while processing '{filename}': {e}")
            continue
    print("Script registration process finished.")

if __name__ == "__main__":
    print("Starting script registration...")
    register_scripts()
