import sys

# Creating list of Built in commands
BUILTINS = {"echo", "exit", "type"}

def main():
    while True:

        sys.stdout.write("$ ")
        sys.stdout.flush()

        command = input().strip()

        # Handle the exit command
        if command.startswith("exit"):
            # Splitting the command to extract the exit
            parts = command.split()
            if len(parts) == 2 and parts[1].isdigit():
                exit_code = int(parts[1])
                sys.exit(exit_code)
            else:
                sys.stdout.write("Usage: exit <code>\n")
                continue

        # If user type echo command
        if command.startswith("echo "):
            # Extract the arguments and print them
            echo_args = command[5:]  # Everything after "echo "
            sys.stdout.write(f"{echo_args}\n")
            continue

        # Handling the type command
        if command.startswith("type "):
            cmd_name = command[5:] # Here extracting the command name
            if cmd_name in BUILTINS:
                sys.stdout.write("f{cmd_name} is a shell builtin\n")
            else:
                sys.stdout.write("f{cmd_name}: not found\n")
            continue

        # Now Handling the invalid commands
        sys.stdout.write(f"{command}: command not found\n")

if __name__ == "__main__":
    main()
