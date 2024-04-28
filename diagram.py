# diagram.py

from sqlalchemy import create_engine, MetaData
from eralchemy import render_er
import os

# Step 1: Reflect the database schema and generate SQLAlchemy models
def reflect_database(database_file):
    engine = create_engine(f"sqlite:///{database_file}")
    metadata = MetaData()
    metadata.reflect(bind=engine)  # Associate metadata with the engine
    return metadata

# Step 2: Render the entity-relationship diagram
def render_er_diagram(metadata, output_file):
    render_er(metadata, output_file)
    return output_file

# Example usage
def generate_er_diagram(database_file=None, output_file=None):
    if database_file is None:
        database_file = os.getenv("DATABASE_FILE")
    if output_file is None:
        output_file = 'erd_diagram.png'
    metadata = reflect_database(database_file)
    render_er_diagram(metadata, output_file)

# Example usage
if __name__ == "__main__":
    database_file = os.getenv("DATABASE_FILE")
    output_file = 'erd_diagram.png'
    generate_er_diagram(database_file, output_file)
