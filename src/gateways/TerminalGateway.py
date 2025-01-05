import subprocess

class TerminalGateway:

    def __init__(self):
        pass

    def execute_command(self, command):
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:            
            raise ValueError(f"Error executing command: {command} : {e.stderr}") from e