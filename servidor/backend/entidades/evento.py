from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from entidades.base import Base

class TipoEvento(object):
    SAIU_AUT_OK = 1
    SAIU_AUT_NOK = 2
    ESTACIONOU_AUT_OK = 3
    ESTACIONOU_AUT_NOK = 4

    evento_str = {
        SAIU_AUT_OK: 'Saiu com autenticacao OK',
        SAIU_AUT_NOK: 'Saiu sem autenticacao',
        ESTACIONOU_AUT_OK: 'Estacionou com autenticacao OK',
        ESTACIONOU_AUT_NOK: 'Estacionou sem autenticacao'
    }

    lista_estados = [
        SAIU_AUT_OK, SAIU_AUT_NOK,
        ESTACIONOU_AUT_OK, ESTACIONOU_AUT_NOK
    ]

class Evento(Base):
    '''
    Relacao one to many com vaga
    '''
    __tablename__ = 'evento'

    id = Column(Integer, primary_key=True)
    tipo = Column(Integer)
    vaga_id = Column(String, ForeignKey('vaga.identificador'), nullable=False)
    data = Column(DateTime)
    # vaga_identificador = Column(Integer, ForeignKey('vaga.identificador'), nullable=False)
    # vaga_id = Column(Integer, ForeignKey('vaga.id'), primary_key=True)

    def __init__(self, tipo, vaga_id, data=None):
        self.tipo = tipo
        self.vaga_id = vaga_id
        self.data = data if data is not None else datetime.now()


    def converteParaJson(self, mqtt=False):
        eventoJson = {
            'id': self.id,
            'tipo': TipoEvento.evento_str[self.tipo],
            'tipo_int': self.tipo,
            'data': self.data if not mqtt else datetime.strftime(self.data, "%a, %-d %b %Y %H:%M:%S GMT"),
            'identificadorVaga': self.vaga_id
        }
        return eventoJson
