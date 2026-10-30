import os
from app import create_app

app = create_app(config_name=os.environ.get("FLASK_ENV", "default"))

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")