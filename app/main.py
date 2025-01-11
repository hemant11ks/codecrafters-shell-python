import os
import sys
import subprocess

def find_executable_in_path(command):
    """Search for an executable file in the directories listed in PATH."""
    path_dirs = os.getenv("PATH", "").split(":")  # Get directories from PATH
    for directory in path_dirs:
        full_path = os.path.join(directory, command)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path
    return None

def main():
    while True:
        # Display the prompt
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Wait for user input
        try:
            command = input().strip()
        except EOFError:  # Handle end-of-file (Ctrl+D) gracefully
            break

        if not command:
            continue

        # Parse the command and arguments
        parts = command.split()
        program_name = parts[0]
        args = parts[1:]

        # Locate the executable in PATH
        executable = find_executable_in_path(program_name)
        if executable:
            try:
                # Execute the command and print its output directly
                subprocess.run([executable] + args)
            except FileNotFoundError:
                sys.stdout.write(f"{program_name}: command not found\n")
        else:
            sys.stdout.write(f"{program_name}: command not found\n")

if __name__ == "__main__":
    main()
