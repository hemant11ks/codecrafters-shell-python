import os
import sys
import subprocess

# List of shell built-ins
BUILT_INS = {"echo", "exit", "type"}

def find_executable_in_path(command):
    """Search for an executable file in the directories listed in PATH."""
    path_dirs = os.getenv("PATH", "").split(":")  # Get directories from PATH
    for directory in path_dirs:
        full_path = os.path.join(directory, command)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path
    return None

def handle_type_command(args):
    """Handle the 'type' command."""
    if len(args) < 1:
        return

    command = args[0]
    if command in BUILT_INS:
        print(f"{command} is a shell builtin")
    else:
        executable = find_executable_in_path(command)
        if executable:
            print(f"{command} is {executable}")
        else:
            print(f"{command}: not found")

def execute_external_command(command, args):
    """Execute an external program."""
    executable = find_executable_in_path(command)
    if executable:
        # Execute the command using subprocess
        try:
            process = subprocess.run([executable] + args, check=True)
        except subprocess.CalledProcessError:
            print(f"{command}: error while executing")
    else:
        print(f"{command}: command not found")

def main():
    while True:
        # Display the prompt
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Wait for user input
        try:
            command_line = input().strip()
        except EOFError:  # Handle end-of-file (Ctrl+D) gracefully
            break

        if not command_line:
            continue

        # Parse the command and arguments
        parts = command_line.split()
        cmd_name = parts[0]
        args = parts[1:]

        # Handle built-in commands
        if cmd_name == "exit":
            break
        elif cmd_name == "type":
            handle_type_command(args)
        elif cmd_name == "echo":
            print(" ".join(args))
        else:
            # Handle external commands
            execute_external_command(cmd_name, args)

if __name__ == "__main__":
    main()
