import os
import sys
import subprocess

def find_in_path(command):
    """
    Search for the command in the PATH environment variable directories.
    Returns the full path if found, otherwise None.
    """
    path = os.environ.get("PATH", "")
    for directory in path.split(":"):
        potential_path = os.path.join(directory, command)
        if os.path.isfile(potential_path) and os.access(potential_path, os.X_OK):
            return potential_path
    return None

def main():
    while True:
        # Display the prompt
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Get the user input
        try:
            user_input = input().strip()
        except EOFError:
            break  # Handle EOF to exit gracefully

        if not user_input:
            continue

        # Split the command into executable and arguments
        parts = user_input.split(" ")
        command, *args = parts

        # Handle built-in commands
        if command == "exit" and args == ["0"]:
            exit(0)
        elif command == "echo":
            print(" ".join(args))
        elif command == "type":
            if args:
                cmd_to_check = args[0]
                if cmd_to_check in {"echo", "exit", "type"}:
                    print(f"{cmd_to_check} is a shell builtin")
                else:
                    location = find_in_path(cmd_to_check)
                    if location:
                        print(f"{cmd_to_check} is {location}")
                    else:
                        print(f"{cmd_to_check}: not found")
            else:
                print("type: missing argument")
        else:
            # Handle external commands
            executable_path = find_in_path(command)
            if executable_path:
                try:
                    # Extract the program name from the full path
                    program_name = os.path.basename(executable_path)
                    print(f"Arg #0 (program name): {program_name}")  # Print only the program name
                    # Run the command with arguments
                    result = subprocess.run([executable_path] + args, check=True, text=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error: {e}")
                except Exception as e:
                    print(f"{command}: failed to execute. {e}")
            else:
                print(f"{user_input}: command not found")

if __name__ == "__main__":
    main()
