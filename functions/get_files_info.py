import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_working_path = os.path.abspath(working_directory)

        target_directory = os.path.normpath(os.path.join(absolute_working_path, directory))

        valid_target_dir = (os.path.commonpath([absolute_working_path, target_directory])== absolute_working_path)

        if not valid_target_dir:
            return f'Error: Cannot list {directory} as it is outside the permitted working directory'

        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'

        result = ""

        files = os.listdir(target_directory)

        for file in files:
            full_path = os.path.join(target_directory, file)
            file_size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)

            result += f"- {file}: file_size={file_size} bytes, is_dir={is_dir}\n"

        return result

    except Exception as e:
        return f"Error: {e}"
