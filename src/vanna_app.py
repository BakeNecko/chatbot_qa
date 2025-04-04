from vanna.flask import VannaFlaskApp
from src.vanna_train import get_vanna

if __name__ == '__main__':
    vn = get_vanna()
    app = VannaFlaskApp(vn)
    app.run()
