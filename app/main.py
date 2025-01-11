import os
import sys

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
            executable = find_executable_in_path(cmd_name)
            if executable:
                os.execvp(executable, [cmd_name] + args)
            else:
                print(f"{cmd_name}: command not found")

if __name__ == "__main__":
    main()
