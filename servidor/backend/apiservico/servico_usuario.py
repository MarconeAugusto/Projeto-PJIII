from entidades.usuario import Usuario
from entidades.base import Session
from entidades.vaga import Vaga
from entidades.contato import Contato


class ServicoUsuario(object):
    def obtem(self, idUsuario=None, comVagas=False):
        session = Session()
        usuarios = None

        if idUsuario is not None:
            usuarios = session.query(Usuario).filter(Usuario.id == idUsuario).first()
        else:
            usuarios = session.query(Usuario).all()

        usuariosJson = None
        if usuarios is not None:
            if type(usuarios) == list:
                usuariosJson = [usr.converteParaJson(comVagas) for usr in usuarios]
            else:
                usuariosJson = usuarios.converteParaJson(comVagas)

        session.close()
        return usuariosJson

    def novoUsuarioDadosValidados(self, dados):
        dadosObrigatorios = ['nome', 'sobrenome', 'email', 'senha', 'tipo']
        return all(dado in dados for dado in dadosObrigatorios)

    def adiciona(self, dados):
        if not self.novoUsuarioDadosValidados(dados):
            # Faltando parametros.. retorna um erro
            return {'erro': 400, 'msg': 'Parametros incompletos'}

        usuario = Usuario(dados['nome'], dados['sobrenome'], dados['email'], dados['senha'], dados['tipo'])

        usuarioJson = {}
        session = Session()
        try:
            if 'vagas' in dados:
                if type(dados['vagas']) != list:
                    return {'erro': 400, 'msg': 'Lista de vagas mal formatada'}

                vagas = []
                for vg in dados['vagas']:
                    vaga = session.query(Vaga).filter(Vaga.identificador == vg['identificador']).first()

                    if vaga is None:
                        return {'erro': 404, 'msg': 'Vaga nao encontrada'}

                    vagas.append(vaga)

                if len(vagas):
                    usuario.setaVagas(vagas)

            session.add(usuario)

            fone_residencial = dados.get('fone_residencial', None)
            fone_trabalho = dados.get('fone_trabalho', None)
            celular_1 = dados.get('celular_1', None)
            celular_2 = dados.get('celular_2', None)
            contato = Contato(usuario, fone_residencial=fone_residencial, fone_trabalho=fone_trabalho,
                              celular_1=celular_1, celular_2=celular_2)
            session.add(contato)

            session.commit()
            usuarioJson = usuario.converteParaJson(comVagas=True)
        except Exception as e:
            print(str(e))
            return {'erro': 500, 'msg': 'Erro ao adicionar usuario', 'exc': str(e)}
        finally:
            session.close()

        return {'msg': 'Usuario adicionado', 'usuario': usuarioJson}

    def alteraUsuario(self, idUsuario, dados):
        session = Session()
        usuarioJson = {}

        try:
            usuario = session.query(Usuario).filter(Usuario.id == idUsuario).first()
            if usuario is None:
                return {'erro': 404, 'msg': 'Usuario nao encontrado'}

            vagas = None
            if 'vagas' in dados:
                if type(dados['vagas']) != list:
                    return {'erro': 400, 'msg': 'Lista de vagas mal formatada'}

                vagas = []
                for vg in dados['vagas']:
                    vaga = session.query(Vaga).filter(Vaga.identificador == vg['identificador']).first()

                    if vaga is None:
                        return {'erro': 404, 'msg': 'Vaga nao encontrada'}

                    vagas.append(vaga)

            for attr, val in usuario.__dict__.items():
                if attr in dados:
                    valor = dados[attr] if attr != 'senha' else Usuario.getHashSenha(dados['senha'])
                    setattr(usuario, attr, valor)

            if vagas is not None:
                usuario.setaVagas(vagas)

            chavesContato = ['fone_residencial', 'fone_trabalho', 'celular_1', 'celular_2']
            if any(c in dados for c in chavesContato):
                contatoUsuarioBD = usuario.contato
                if contatoUsuarioBD is not None:
                    for attr, val in contatoUsuarioBD.__dict__.items():
                        if attr in dados:
                            setattr(contatoUsuarioBD, attr, dados[attr])
                else:
                    fone_residencial = dados.get('fone_residencial', None)
                    fone_trabalho = dados.get('fone_trabalho', None)
                    celular_1 = dados.get('celular_1', None)
                    celular_2 = dados.get('celular_2', None)

                    contato = Contato(usuario, fone_residencial=fone_residencial, fone_trabalho=fone_trabalho,
                                      celular_1=celular_1, celular_2=celular_2)
                    session.add(contato)

            session.commit()
            usuarioJson = usuario.converteParaJson(comVagas=True)

        except Exception as e:
            print(str(e))
            return {'erro': 500, 'msg': 'Erro ao alterar usuario', 'exc': str(e)}
        finally:
            session.close()

        return {'msg': 'Usuario alterado', 'usuario': usuarioJson}

    def _obtemUsuarioPorId(self, sessao, idUsuario):
        usuario = sessao.query(Usuario).filter(Usuario.id == idUsuario).first()
        return usuario

    def obtemContato(self, idUsuario):
        session = Session()

        try:
            usuario = self._obtemUsuarioPorId(session, idUsuario)
            if usuario is None:
                return {'erro': 404, 'msg': 'Usuario nao encontrado'}

            contato = usuario.contato
            if contato is None:
                return {}
            else:
                return usuario.contato.converteParaJson()

        except Exception as e:
            return {'erro': 500, 'msg': 'Erro ao obter contato do usuario', 'exc': str(e)}
        finally:
            session.close()

    def obtemVagas(self, idUsuario):
        sessao = Session()

        usuario = self._obtemUsuarioPorId(sessao, idUsuario)
        if usuario is None:
            sessao.close()
            return {'erro': 404, 'msg': 'Usuario nao encontrado'}

        vagas = usuario.obtemVagas()
        sessao.close()
        vagasJson = [vg.converteParaJson() for vg in vagas]
        return vagasJson

    def removeUsuario(self, idUsuario):
        usuarioJson = {}
        session = Session()
        try:
            usuario = session.query(Usuario).filter(Usuario.id == idUsuario).first()

            if usuario is None:
                return {'erro': 404, 'msg': 'Usuario nao encontrado'}

            usuarioJson = usuario.converteParaJson()
            session.delete(usuario)
            session.commit()
        except Exception as e:
            print(str(e))
            return {'erro': 500, 'msg': 'Erro ao remover usuario', 'exc': str(e)}
        finally:
            session.close()

        return {'msg': 'Usuario removido', 'usuario': usuarioJson}

    def checkLogin(self, dados):
        if 'email' not in dados or 'senha' not in dados:
            return {'erro': 400, 'msg': 'Parametros incompletos'}

        session = Session()
        usuario = session.query(Usuario).filter(Usuario.email == dados['email']).first()

        if not usuario:
            session.close()
            return {'erro': 403, 'msg': 'Usuario nao encontrado'}

        vagas = []
        if len(usuario.obtemVagas()):
            vagas = [vaga.converteParaJson() for vaga in usuario.obtemVagas()]

        session.close()

        if not Usuario.checkSenha(dados['senha'], usuario.senha):
            return {'erro': 401, 'msg': 'Senha invalida'}

        return {'id': usuario.id, 'email': usuario.email, 'tipo': usuario.tipo, 'nome': usuario.nome, 'vagas': vagas}

    def obtemResponsaveis(self, idVaga):
        # if 'idVaga' not in dados:
        #     return {'erro': 400, 'msg': 'Parametros incompletos'}

        # idVaga = dados['idVaga']
        session = Session()

        try:
            # Artist.query.filter(Artist.albums.any(genre_id=genre.id)).all()
            responsaveisResp = []
            responsaveis = session.query(Usuario).filter(Usuario.vagas.any(id=idVaga)).all()

            for responsavel in responsaveis:
                responsaveisResp.append(responsavel.converteParaJson(comContato=True))

            return responsaveisResp
        except Exception as e:
            return {'erro': 500, 'msg': 'Erro ao obter responsaveis', 'exc': str(e)}
        finally:
            session.close()


servicoUsuario = ServicoUsuario()
