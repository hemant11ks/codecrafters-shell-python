import os
import sys

# List of supported built-in commands
BUILTINS = {"echo", "exit", "type"}

def find_executable_in_path(command):
    """Searching for an executable file in the directories listed in PATH."""
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
        command = input().strip()

        # Handle the exit command
        if command.startswith("exit"):
            parts = command.split()
            if len(parts) == 2 and parts[1].isdigit():
                exit_code = int(parts[1])
                sys.exit(exit_code)
            else:
                sys.stdout.write("exit <code>\n")
                continue

        # Handle the echo command
        if command.startswith("echo "):
            echo_args = command[5:]  # Everything after "echo "
            sys.stdout.write(f"{echo_args}\n")
            continue

        # Handle the type command
        if command.startswith("type "):
            cmd_name = command[5:]  # Extract the command name

            # Check if it's a shell builtin
            if cmd_name in BUILTINS:
                sys.stdout.write(f"{cmd_name} is a shell builtin\n")
            else:
                # Check if it's an executable in PATH
                executable_path = find_executable_in_path(cmd_name)
                if executable_path:
                    sys.stdout.write(f"{cmd_name} is {executable_path}\n")
                else:
                    sys.stdout.write(f"{cmd_name}: not found\n")
            continue

        # Handle invalid commands
        sys.stdout.write(f"{command}: command was not found\n")

if __name__ == "__main__":
    main()
