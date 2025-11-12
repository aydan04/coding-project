# run_local.py
import os
import subprocess
import sys

VENV_DIR = "venv"
REQUIREMENTS_FILE = "requirements.txt"

def run_command(command, check=True):
    """Runs a command and checks for errors, exiting on failure."""
    print(f"--- Running: {' '.join(command)} ---")
    try:
        subprocess.run(command, check=check)
    except FileNotFoundError:
        print(f"Error: Command not found: {command[0]}. Make sure it's installed and in your PATH.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(command)}")
        print(f"Return code: {e.returncode}")
        sys.exit(1)

def main():
    """
    Automates the setup and execution of the project.
    1. Creates a virtual environment if it doesn't exist.
    2. Installs dependencies into the virtual environment.
    3. Runs the FastAPI application using the virtual environment's interpreter.
    """
    # Use the same Python interpreter that is running this script
    python_executable = sys.executable

    # 1. Create a virtual environment if it doesn't exist
    if not os.path.isdir(VENV_DIR):
        print(f"Creating virtual environment in '{VENV_DIR}'...")
        run_command([python_executable, "-m", "venv", VENV_DIR])
    else:
        print(f"Virtual environment '{VENV_DIR}' already exists.")

    # 2. Determine the path to the Python executable within the venv
    if sys.platform == "win32":
        venv_python = os.path.join(VENV_DIR, "Scripts", "python.exe")
    else: # macOS and Linux
        venv_python = os.path.join(VENV_DIR, "bin", "python")

    # 3. Install dependencies using the venv's pip
    print(f"Installing dependencies from {REQUIREMENTS_FILE}...")
    run_command([venv_python, "-m", "pip", "install", "-r", REQUIREMENTS_FILE])
    print("Dependencies are up to date.")

    # 4. Run the FastAPI application
    print("\\n--- Starting the application ---")
    print("You can access the API at http://127.0.0.1:8000")
    print("Interactive API docs are available at http://127.0.0.1:8000/docs")
    print("Press CTRL+C to stop the server.\\n")

    run_command([venv_python, "-m", "uvicorn", "src.main:app", "--reload"])

if __name__ == "__main__":
    main()
