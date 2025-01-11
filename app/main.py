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
                # Execute the command and capture its output
                result = subprocess.run(
                    [executable] + args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                # Print the expected output
                sys.stdout.write(f"Program was passed {len(parts)} args (including program name).\n")
                sys.stdout.write(f"Arg #0 (program name): {program_name}\n")
                for i, arg in enumerate(args, start=1):
                    sys.stdout.write(f"Arg #{i}: {arg}\n")
                sys.stdout.write(result.stdout)  # Include program output if necessary
            except subprocess.CalledProcessError as e:
                sys.stderr.write(f"Error: {e}\n")
            except FileNotFoundError:
                sys.stdout.write(f"{program_name}: command not found\n")
        else:
            sys.stdout.write(f"{program_name}: command not found\n")

if __name__ == "__main__":
    main()
