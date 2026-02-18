from backend.database import engine
from backend.models import Base


def init():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init()
    print("PostgreSQL tables created ✅")
