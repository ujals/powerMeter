import subprocess

# Function to run a Python script
def run_script(script_name):
    result = subprocess.run(['python', script_name], capture_output=True, text=True)
    print(f"Running {script_name}...")
    print(result.stdout)
    print(result.stderr)

# List of scripts to run
scripts = ['three_phase.py', 'single_phase.py']

# Run each script
for script in scripts:
    run_script(script)
