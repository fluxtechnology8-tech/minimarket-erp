from views.ui.application import MinimarketApp
from core.init_db import init_db

_app = None

def main(page):
    global _app
    init_db()

    if _app is None:
        _app = MinimarketApp()
    _app.main(page)

if __name__ == "__main__":
    MinimarketApp().run()
