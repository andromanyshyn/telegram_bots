from sqlalchemy import create_engine, Column, Integer, DateTime, LargeBinary
from keys.keys import DB_USER, DB_PASSWORD, DB_NAME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}", echo=True
)

Base = declarative_base()


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    image = Column(LargeBinary)


Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

with open(r'C:\Users\Andrew\TelegramBots\file_bot\images\2023-07-23.png', 'rb') as file:
    img = file.read()

image = Image(image=img)
session.add(image)
session.commit()
session.close()
