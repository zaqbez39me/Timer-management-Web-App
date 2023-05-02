import os
import secrets
import string
from pathlib import Path
from random import Random

from dotenv import load_dotenv


def main():
    secrets_file = os.path.join(Path(__file__).resolve().parent, 'secrets.env')
    load_dotenv(secrets_file)

    if not os.getenv('SECRET_ACCESS_KEY'):
        secret_access_key = secrets.token_hex(64)
        with open(secrets_file, 'a') as secret_file:
            secret_file.write(f'SECRET_ACCESS_KEY={secret_access_key}\n')

    if not os.getenv('SECRET_REFRESH_KEY'):
        secret_refresh_key = secrets.token_hex(128)
        with open(secrets_file, 'a') as secret_file:
            secret_file.write(f'SECRET_REFRESH_KEY={secret_refresh_key}\n')

    if not os.getenv('SECRET_REDIS'):
        rand = Random()
        secret_redis = ''.join(rand.choice(string.ascii_letters + string.digits) for _ in range(256))
        with open(secrets_file, 'a') as secret_file:
            secret_file.write(f'SECRET_REDIS={secret_redis}\n')


if __name__ == '__main__':
    main()
