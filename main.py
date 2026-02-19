import subprocess
import sys

def main():
    # Check if the user provided a command to run
    if len(sys.argv) < 2:
        print("Usage: python main.py <command>")
        sys.exit(1)

    # Get the command from the command line arguments
    command = sys.argv[1:]

    try:
        # Run the command and capture the output
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Command Output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("An error occurred while running the command:")
        print(e.stderr)
if __name__ == "__main__":    
    main()