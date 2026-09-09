
import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        absolute_working_path = os.path.abspath(working_directory)
        
        target_directory = os.path.normpath(os.path.join(absolute_working_path, file_path))
        
        valid_target_dir = (os.path.commonpath([absolute_working_path, target_directory])== absolute_working_path)
        
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.isdir(os.path.dirname(target_directory)):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_directory), exist_ok=True)
        with open(target_directory, "w") as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
            return f"Error: {e}"


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a specified file relative to the working directory. If the file does not exist, it will be created. If the file is a directory or outside the working directory, an error message will be returned.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}