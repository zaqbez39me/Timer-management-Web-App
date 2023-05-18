#!/usr/bin/env python

import os
from collections import OrderedDict
from pathlib import Path

from dotenv import load_dotenv, dotenv_values


def main():
    directory = os.path.abspath(Path(__file__).resolve().parent)
    loaded_vars = OrderedDict()
    env_files = set()
    env_examples = set()
    for file in os.listdir(directory):
        file_name = os.path.splitext(file)[0]
        if file.endswith(".env"):
            env_files.add(file_name)
            file_name = os.path.join(directory, file)
            loaded_vars.update(dotenv_values(file_name))
            load_dotenv(file_name)
        elif file.endswith(".env-example"):
            env_examples.add(file_name)
    not_created_env_files = env_examples.difference(env_files)
    for file in not_created_env_files:
        with open(os.path.join(directory, file) + '.env', "w"):
            pass
    print("export", end=" ")
    # Output environment variables in the format expected by Bash
    for key, value in loaded_vars.items():
        print(f"{key}={value}", end=" ")


if __name__ == '__main__':
    main()
