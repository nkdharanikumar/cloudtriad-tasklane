from dotenv import load_dotenv

load_dotenv()  # loads variables from a local .env file if present

from app import create_app  # noqa: E402
from app.config import Config  # noqa: E402

app = create_app()

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
