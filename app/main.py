import os
import sys
import shlex
from dataclasses import dataclass
import subprocess
from typing import TextIO

PATH = os.environ["PATH"]
COMMANDS = ["type", "pwd", "echo", "cd", "exit"]

@dataclass
class Command:
    bin: str
    args: list[str]
    stdout: TextIO = sys.stdout
    stderr: TextIO = sys.stderr

    def __post_init__(self):
        redirect = ""
        output = ""
        args: list[str] = []
        for i, arg in enumerate(self.args):
            if arg in {">", ">>", "1>", "2>", "1>>", "2>>"}:
                redirect = arg
                output = " ".join(self.args[i + 1 :])
                break
            else:
                args.append(arg)
        self.args = args
        if not redirect:
            return
        match redirect:
            case ">" | "1>":
                self.stdout = open(output, "w")
            case ">>" | "1>>":
                self.stdout = open(output, "a+")
            case ">" | "2>":
                self.stderr = open(output, "w")
            case ">>" | "2>>":
                self.stderr = open(output, "a+")
            case _:
                raise ValueError(f"Invalid redirect: {redirect}")

def parseInput(text: str) -> Command:
    args = shlex.split(text)
    return Command(bin=args[0], args=args[1:])

def get_executable_path(bin: str) -> str | None:
    for path in PATH.split(os.pathsep):
        fp = os.path.join(path, bin)
        if os.path.exists(fp):
            return fp
    return None

def main():
    # Display the welcome message when the shell starts
    print("Welcome to the shell made by Hrishin Debnath (BRAHMIN)")

    sys.stdout.write("$ ")
    while True:
        result = input()
        command = parseInput(result)
        str_args = " ".join(command.args)
        stdout = command.stdout
        stderr = command.stderr
        try:
            match command.bin:
                case "type":
                    if str_args in COMMANDS:
                        print(f"{str_args} is a shell builtin", file=stdout)
                    elif path := get_executable_path(str_args):
                        print(f"{str_args} is {path}", file=stdout)
                    else:
                        print(f"{str_args}: not found", file=stderr)
                case "exit":
                    sys.exit(0)
                case "echo":
                    print(str_args, file=stdout)
                case "cd":
                    if str_args == "~":
                        os.chdir(os.path.expanduser("~"))
                    elif os.path.exists(str_args):
                        os.chdir(str_args)
                    else:
                        print(f"cd: {str_args}: No such file or directory", file=stderr)
                case "pwd":
                    print(os.getcwd(), file=stdout)
                case _:
                    try:
                        subprocess.run(
                            [command.bin, *command.args],
                            stdout=command.stdout,
                            stderr=command.stderr,
                        )
                    except Exception:
                        print(f"{result}: command not found", file=stderr)
        finally:
            if stdout is not sys.stdout:
                stdout.close()
            if stderr is not sys.stderr:
                stderr.close()
        sys.stdout.write("$ ")

if __name__ == "__main__":
    main()

# End