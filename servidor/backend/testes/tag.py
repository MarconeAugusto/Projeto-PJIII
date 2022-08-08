from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from base import Base

# ControladorTag <-> ContactDetails

class ControladorTag(Base):
    __tablename__ = 'controlador_tag'

    id = Column(Integer, primary_key=True)
    codTag = Column(String)
    idUsuario = Column(Integer, ForeignKey('usuario.id'))
    usuario = relationship("Usuario", backref="controlador_tag")

    def __init__(self, codTag, usuario):
        self.codTag = codTag
        self.usuario = usuario