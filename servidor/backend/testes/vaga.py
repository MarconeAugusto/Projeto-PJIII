from sqlalchemy import Column, String, Integer

from base import Base

# vaga <-> actor

class Vaga(Base):
    __tablename__ = 'vaga'

    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    status = Column(Integer)

    def __init__(self, tipo, status=0):
        self.tipo = tipo
        self.status = status