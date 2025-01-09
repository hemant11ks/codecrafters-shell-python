import sys

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

        # Now Handling the invalid commands
        sys.stdout.write(f"{command}: command not found\n")

if __name__ == "__main__":
    main()
