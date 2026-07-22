"""Create the configured SQLAlchemy database schema."""

from app.database.database import Base, engine
from app.database.models import Evaluation  # Import registers the model with Base.

Base.metadata.create_all(bind=engine)

print("Database created successfully!")
