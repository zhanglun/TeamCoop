from teamcoop import create_app
from config import config


app = create_app('development')


if __name__ == '__main__':
    app.run()