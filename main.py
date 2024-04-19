import subprocess

def run_python_script(script_path):
    try:
        subprocess.run(["python", script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_path}: {e}")

def main():
    # List of Python script paths to execute
    python_scripts = [
        "scrapper_main.py",
        "convert_main.py"
    ]

    # Execute each Python script one after another
    for script in python_scripts:
        print(f"Executing {script}...")
        run_python_script(script)
        print(f"Execution of {script} completed.\n")

if __name__ == "__main__":
    main()
