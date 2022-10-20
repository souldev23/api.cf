from app import create_app
from config import config

environment = config['development']

server = create_app(environment)

if __name__ == '__main__':
    server.run()