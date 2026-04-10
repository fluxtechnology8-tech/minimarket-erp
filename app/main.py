from app.views.ui.application import MinimarketApp

_app = None

def main(page):
    global _app
    if _app is None:
        _app = MinimarketApp()
    _app.main(page)

if __name__ == "__main__":
    MinimarketApp().run()
