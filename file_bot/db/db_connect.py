import datetime

from sqlalchemy import Column, DateTime, Integer, LargeBinary, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from keys.keys import DB_NAME, DB_PASSWORD, DB_USER

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}", echo=True
)

Base = declarative_base()


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    image = Column(LargeBinary)


Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine, autoflush=True)
