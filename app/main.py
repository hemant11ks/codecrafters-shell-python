import sys

def main():
    while True:
        
        sys.stdout.write("$ ")
        sys.stdout.flush()

        
        command = input().strip()

        if command.startswith("exit"):
            # Spliting the exit command
            parts = command.split()
            if len(parts) == 2 and parts[1].isdigit():
                exit_code = int(parts[1])
                sys.exit(exit_code)
            else:
                sys.stdout.write("Usage: exit <code>\n")
                continue

        
        sys.stdout.write(f"{command}: command not found\n")

if __name__ == "__main__":
    main()
