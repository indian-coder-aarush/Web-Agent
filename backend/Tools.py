import os
import subprocess

base = 'workspace'

os.makedirs(base, exist_ok=True)

def full_path(filepath):
    return os.path.join(base, filepath.lstrip("/"))

def read_file(filepath):
    try:
        with open(full_path(filepath), 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "File Path you requested was not found."

def write_file(filepath, content):
    os.makedirs(os.path.dirname(full_path(filepath)), exist_ok=True)
    try:
        with open(full_path(filepath), 'w', encoding = 'utf-8') as f:
            f.write(content)
    except FileNotFoundError:
        return "File Path you requested was not found."

def run_command(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd = base,
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Command failed (code {result.returncode}): {result.stderr.strip()}"

    except subprocess.TimeoutExpired:
        return "Command timed out."
    except Exception as e:
        return f"Command error: {str(e)}"

def safe_run_command(command):
    banned = ["rm", "del", "shutdown", "reboot", "format", "mkfs"]
    if any(b in command for b in banned):
        return "Command blocked for safety."
    return run_command(command)

def make_file(file_name):
    os.makedirs(os.path.dirname(full_path(file_name)), exist_ok=True)
    with open(full_path(file_name), "w") as f:
        f.write("")