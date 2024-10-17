"""
This script contains utility functions.
"""

import json
import os


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def create_file_path(path_as_list: list):
    """
        Constructs a file path by joining the project's root directory with the specified path components.

        Args:
            path_as_list (list): A list of strings representing the path components to be joined with the project root.

        Returns:
            str: The full file path constructed from the project root and the provided path components.
        """

    # Determine the project's root directory
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Join the project root with the elements in the path_as_list
    new_file_path = os.path.join(project_root, *path_as_list)

    return new_file_path


def load_json_data(file_path):
    # print("Current Working Directory:", os.getcwd())
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, 'r') as file:
        return json.load(file)


def load_secrets(filename='secrets.json'):
    folder=get_project_root()
    filename = os.path.join(folder, filename)
    with open(filename, 'r') as file:
        secrets = json.load(file)
    return secrets

