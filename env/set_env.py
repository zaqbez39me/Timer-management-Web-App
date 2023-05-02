#!/usr/bin/env python

import os
from collections import OrderedDict
from pathlib import Path

from dotenv import load_dotenv, dotenv_values


def main():
    directory = os.path.abspath(Path(__file__).resolve().parent)
    loaded_vars = OrderedDict()

    for file in os.listdir(directory):
        if file.endswith(".env"):
            file_name = os.path.join(directory, file)
            loaded_vars.update(dotenv_values(file_name))
            load_dotenv(file_name)

    print("export", end=" ")
    # Output environment variables in the format expected by Bash
    for key, value in loaded_vars.items():
        print(f"{key}={value}", end=" ")


if __name__ == '__main__':
    main()