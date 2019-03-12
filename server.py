import os

from hermes.app import app


if __name__ == "__main__":
    debug = os.environ.get("DEBUG", False)
    app.run(host='0.0.0.0', port=8000, debug=debug)
