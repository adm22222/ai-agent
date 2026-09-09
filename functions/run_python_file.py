import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
            absolute_working_path = os.path.abspath(working_directory)
    
            target_directory = os.path.normpath(os.path.join(absolute_working_path, file_path))
    
            valid_target_dir = os.path.commonpath([absolute_working_path, target_directory]) == absolute_working_path
    
            if not valid_target_dir:
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

            if not os.path.isfile(target_directory):
                return f'Error: "{file_path}" does not exist or is not a regular file'
            if not file_path.endswith(".py"):
                return f'Error: "{file_path}" is not a Python file'
            
            absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))
            command = ["python", absolute_file_path]

            if args:
                command.extend(args)

            process = subprocess.run(command,capture_output=True, text=True,timeout=30, cwd=absolute_working_path)

            if process.returncode != 0:
                return f"Process exited with code {process.returncode}"

            if not process.stdout and not process.stderr:
                return "No output produced"


            output = ""
            if process.stdout:
                output += f"STDOUT: {process.stdout}"
            if process.stderr:
                output += f"STDERR: {process.stderr}"
            return output
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file relative to the working directory, returning the output as a string. If the file is not a Python file or does not exist, an error message will be returned.", 
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Optional list of arguments to pass to the Python file",
                },
            },
        },
    },
}      