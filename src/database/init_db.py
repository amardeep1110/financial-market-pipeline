from src.database.db import engine
from src.database.models import Base


def initialize_database():
    """
    Create all database tables.
    """

    Base.metadata.create_all(engine)


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully!")
