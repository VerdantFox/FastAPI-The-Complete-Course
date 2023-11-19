from pathlib import Path

import jinja_partials
from fastapi.templating import Jinja2Templates

WEB_APP = Path(__file__).parent.parent / "web_app"
TEMPLATES_DIR = WEB_APP / "templates"
STATIC_DIR = WEB_APP / "static"

templates = Jinja2Templates(directory=TEMPLATES_DIR)
jinja_partials.register_starlette_extensions(templates)
