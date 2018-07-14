from app import app, db
from app.models import Sensor, Reading, Category

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Sensor': Sensor,
        'Reading': Reading,
        'Category': Category
    }