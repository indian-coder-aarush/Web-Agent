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
        with open(filepath, 'w') as f:
            f.write(content)
    except FileNotFoundError:
        return "File Path you requested was not found."

def run_command(command):
    try:
        out = check_output(command, text=True)
        return out
    except CalledProcessError as e:
        return "Command failed: " + e.returncode + " " + e.output