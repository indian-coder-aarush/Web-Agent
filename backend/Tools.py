import os
import subprocess

def read_file(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "File Path you requested was not found."

def write_file(filepath, content):
    try:
        with open(filepath, 'w', encoding = 'utf-8') as f:
            f.write(content)
    except FileNotFoundError:
        return "File Path you requested was not found."

def run_command(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=180
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
    with open(file_name, "w") as f:
        f.write("")