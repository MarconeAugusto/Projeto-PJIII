import sys
from flask import Flask, jsonify, Blueprint
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from apirest.utils.auth import generate_token, verify_token, requires_auth_user, requires_auth_admin

# sys.path.insert(0, '..')
from apiservico.servico_usuario import servicoUsuario

bp_usuario = Blueprint('bp_usuario', __name__)

# curl -i http://localhost:5000/usuario
@bp_usuario.route('/usuario', methods=['GET'])
# @requires_auth_admin
def obtem_usuarios():
    resp = {'usuarios': servicoUsuario.obtem(comVagas=True)}
    return jsonify(resp)

# curl -i http://localhost:5000/usuario/1
@bp_usuario.route('/usuario/<int:idUsuario>', methods=['GET'])
@requires_auth_user
def obtem_usuario(idUsuario):
    resp = {'usuario': servicoUsuario.obtem(idUsuario)}
    return jsonify(resp)

# curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/usuario/<ID>
@bp_usuario.route('/usuario/<int:idUsuario>', methods=['DELETE'])
# @requires_auth_admin
def remove_usuario(idUsuario):
    resp = servicoUsuario.removeUsuario(idUsuario)
    if 'erro' in resp:
        abort(resp['erro'], resp.get('msg'))

    return make_response(jsonify(resp), 201)


# curl -i -H "Content-Type: application/json" -X POST -d '{"identificadorVaga": "A01", "novoEstado": 1}' http://localhost:5000/usuario
# curl -i -H "Content-Type: application/json" -X POST -d '{"nome":"Joao","sobrenome":"Silva","email":"joao","senha":"1234","tipo":2}' http://localhost:5000/usuario
# curl -i -H "Content-Type: application/json" -X POST -d '{"nome":"Vinicius","sobrenome":"Souza","email":"vini","senha":"1234"}' http://localhost:5000/usuario
# curl -i -H "Content-Type: application/json" -X POST -d '{"nome":"Vinicius","sobrenome":"Souza","email":"vini","senha":"1234","tipo":1}' http://localhost:5000/usuario
@bp_usuario.route('/usuario', methods=['POST'])
# @requires_auth_admin
def adiciona_usuario():
    if not request.json:
        abort(400)
    
    resp = servicoUsuario.adiciona(request.json)
    if 'erro' in resp:
        abort(resp['erro'], resp.get('msg'))

    return make_response(jsonify(resp), 201)

# curl -i -H "Content-Type: application/json" -X POST -d '{"nome":"Vinicius","sobrenome":"Souza","email":"vini","senha":"1234","tipo":1}' http://localhost:5000/usuario/1
@bp_usuario.route('/usuario/<int:idUsuario>', methods=['PUT'])
# @requires_auth_admin
def altera_usuario(idUsuario):
    if not request.json:
        abort(400)

    print(str(request.json))
    resp = servicoUsuario.alteraUsuario(idUsuario, request.json)
    if 'erro' in resp:
        abort(resp['erro'], resp.get('msg'))

    return jsonify(resp)

# curl -i http://localhost:5000/usuario/1/contato
@bp_usuario.route('/usuario/<int:idUsuario>/contato', methods=['GET'])
# @requires_auth_user
def obtem_contato(idUsuario):
    resp = servicoUsuario.obtemContato(idUsuario)
    if 'erro' in resp:
        abort(resp['erro'], resp.get('msg'))
    return jsonify(resp)

# curl -i http://localhost:5000/usuario/1/vagas
@bp_usuario.route('/usuario/<int:idUsuario>/vagas', methods=['GET'])
@requires_auth_user
def obtem_vagas(idUsuario):
    resp = servicoUsuario.obtemVagas(idUsuario)
    if 'erro' in resp:
        abort(resp['erro'], resp.get('msg'))
    return jsonify(resp)


# curl -i http://localhost:5000/usuarios/vagas
@bp_usuario.route('/usuarios/vagas', methods=['GET'])
@requires_auth_admin
def obtem_usuarios_vagas():
    resp = {'usuarios': servicoUsuario.obtem(comVagas=True)}
    return jsonify(resp)

# curl -i -H "Content-Type: application/json" -X POST -d '{"email":"pedro@email.com.br", "senha": "1234"}' http://localhost:5000/usuario/loginemail
# curl -i -H "Content-Type: application/json" -X POST -d '{"email":"vini@email.com.br", "senha": "1234"}' http://localhost:5000/usuario/login
@bp_usuario.route("/usuario/login", methods=["POST"])
def create_token():
    if not request.json:
        abort(404)

    usuario = servicoUsuario.checkLogin(request.json)
    if 'erro' in usuario:
        abort(usuario['erro'], usuario.get('msg'))

    resp = {'token': generate_token(usuario)}
    resp['tipo'] = usuario.get('tipo')
    resp['nome'] = usuario.get('nome')
    resp['vagas'] = usuario.get('vagas')
    resp['id'] = usuario.get('id')
   

    return jsonify(resp)


@bp_usuario.route("/usuario/check_token", methods=["POST"])
def is_token_valid():
    incoming = request.get_json()
    is_valid = verify_token(incoming["token"])

    if is_valid:
        return jsonify(token_is_valid=True)
    else:
        return jsonify(token_is_valid=False), 403

# curl -i -H "Authorization: eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MDIwNTE1OCwiZXhwIjoxNTcxNDE0NzU4fQ.eyJpZCI6MiwiZW1haWwiOiJwZWRyb0BlbWFpbC5jb20uYnIiLCJ0aXBvIjoyfQ.GiWRFBXNgBE4Y6GQRneTtvzcRi8yectSE07TapXLyXHivRt8kOsEUP57XWwjx6u2RlTOBQi7VmSBb7UrUY0mEQ" http://localhost:5000/usuario/teste_auth_user
# curl -i -H "Authorization: eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MDIwNTE1OCwiZXhwIjoxNTcxNDE0NzU4fQ.eyJpZCI6MiwiZW1haWwiOiJwZWRyb0BlbWFpbC5jb20uYnIiLCJ0aXBvIjoyfQ.GiWRFBXNgBE4Y6GQRneTtvzcRi8yectSE07TapXLyXHivRt8kOsEUP57XWwjx6u2RlTOBQi7VmSBb7UrUY0mEQ" http://localhost:5000/usuario/teste_auth_admin

# curl -i http://localhost:5000/usuario/responsaveis/1
@bp_usuario.route('/usuario/responsaveis/<int:idVaga>', methods=['GET'])
# @requires_auth_admin
def obtem_responsaveis(idVaga):
    resp = {'responsaveis': servicoUsuario.obtemResponsaveis(idVaga)}
    return jsonify(resp)
