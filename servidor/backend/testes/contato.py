from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from base import Base

# contato <-> stuntman

class Contato(Base):
    __tablename__ = 'contato'

    id = Column(Integer, primary_key=True)
    telefones = Column(String)
    email = Column(String)
    whatsapp = Column(String)
    idUsuario = Column(Integer, ForeignKey('usuario.id'))
    usuario = relationship("Usuario", backref=backref("contato", uselist=False))

    def __init__(self, telefones, email, whatsapp, usuario):
        self.telefones = telefones
        self.email = email
        self.whatsapp = whatsapp
        self.usuario = usuario