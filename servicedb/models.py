from sqlalchemy import Column, Integer, String

from database import Base


class Obrashenie(Base):
    __tablename__ = 'obrashenie'

    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String)
    first_name = Column(String)
    middle_name = Column(String)
    phone = Column(String)
    obrashenie = Column(String)
    