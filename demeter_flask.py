from app import create_app, db
from app.models import Sensor, Reading, Category
from config import Config

app = create_app(Config)

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Sensor': Sensor,
        'Reading': Reading,
        'Category': Category
    }
