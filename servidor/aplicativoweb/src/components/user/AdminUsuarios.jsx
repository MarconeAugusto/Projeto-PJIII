import React, { Component } from 'react'
import { Modal, Button } from 'react-bootstrap'
import Main from '../templates/Main'
import api from '../../services/api'
import './AdminUsuarios.css'

const headerProps = {
    icon: 'users',
    title: 'Usuários',
    subtitle: 'Cadastro de usuários: Incluir, Listar, Alterar e Excluir!'
}

// const baseUrl = 'http://localhost:5000/usuario'
const initialState = {
    user: { nome: '', sobrenome: '', email: '', senha: '', senha_c: '', tipo: '', tipo_str: '', vagas: [],
            fone_residencial: '', fone_trabalho: '', celular_1: '', celular_2: '' },
    usuarios: [],
    vagas: []
}

const detalhesUsuario = {
    nome: '',
    sobrenome: '',
    email: '',
    tipo_str: '',
    dataCadastro: '',
    vagas: [],
    contato: {}
}

export default class AdminUsuarios extends Component {
    state = { ...initialState }

    componentWillMount() {
        this.setState({ modalShow: false })
        api.get("/usuario").then(resp => {
            this.setState({ usuarios: resp.data.usuarios })
        })

        api.get("/vagas").then(resp => {
            this.setState({ vagas: resp.data.vagas })
        })
    }

    clear() {
        this.setState({user: initialState.user})
    }

    save() {
        const user = this.state.user
        if (user.tipo_str === 'Administrador')
            user.tipo = 1
        else
            user.tipo = 2
            
        if (user.senha !== user.senha_c) {
            console.log("Senha confirmada errada")
            return
        }

        if (user.id) {
            api.put(`/usuario/${user.id}`, user).then(resp => {
                const usuarios = this.getUpdatedList(resp.data.usuario)
                this.setState({ user: initialState.user, usuarios })
            })
        } else {
            api.post("/usuario", user).then(resp => {
                const usuarios = this.getUpdatedList(resp.data.usuario)
                this.setState({ user: initialState.user, usuarios })
            })
        }
        
        this.removeVaga({}, true)
        // const method = user.id ? 'put' : 'post'
        // const url = user.id ? `${baseUrl}/${user.id}` : baseUrl
        // axios[method](url, user)
        //     .then(resp => {
        //         const usuarios = this.getUpdatedList(resp.data.usuario)
        //         this.setState({ user: initialState.user, usuarios })
        //     })
    }

    getUpdatedList(user, add = true) {
        const list = this.state.usuarios.filter(u => u.id !== user.id)
        if (add) list.unshift(user)
        // list.unshift(user) // poe na primeira posicao do array
        return list
    }

    updateField(event) {
        // nao é interessante alterar diretamente o state
        // pois pra isso existe a funcao setState
        // desta forma, vamos criar uma cópia através do operador spread
        const user = { ...this.state.user }
        user[event.target.name] = event.target.value
        this.setState({user})
    }

    renderDropdownTipoUsuario(){
        return (
            <div className="row">
                <div className="col-12 col-md-6">
                    <div className="form-group">
                        <label htmlFor="tipo">Tipo</label>
                        <select value={this.state.user.tipo_str} onChange={e => this.updateField(e)} name="tipo_str" className="form-control">
                            <option>Selecione</option>
                            <option value="Administrador">Administrador</option>
                            <option value="Usuario">Usuario</option>
                        </select>
                    </div>
                </div>
            </div>
        )
      }

    adicionaVaga(e) {
        const user = { ...this.state.user }
        user.vagas.push({identificador: e.target.value})
        this.setState({user})
    }

    getOptionVagas() {
        return this.state.vagas.map(vaga => {
            return (
                <option value={vaga.identificador}>{vaga.identificador}</option>
            )
        })
    }

    removeVaga(vaga, removeAll=false) {
        const vagas = []
        const user = { ...this.state.user }
        if (!removeAll) {
            user.vagas.forEach(vg => {
                if (vg.identificador !== vaga.identificador) {
                    vagas.push(vg)
                }
            })
            user.vagas = vagas
        } else {
            user.vagas = []
        }
        this.setState({user})
    }

    getCardVagas() {
        return this.state.user.vagas.map(vaga => {
            return (
                <div className="card d-inline-block" style={{width: '7rem', height: '2rem', backgroundColor: 'lightgray', margin: '2px', padding:'1px'}}>
                    {/* <div className="card-body"  style={{padding: '1px', width: '100%', height: '100%'}}> */}
                        <div class="col-sm-12 my-auto"><p className="float-left font-weight-bold text-justify my-center-align">{vaga.identificador}</p></div>
                        <div>
                        <button className="btn btn-secondary btn-sm float-right"
                            onClick={() => this.removeVaga(vaga)}
                            style={{width: '1.75rem', height: '1.75rem'}}>
                            <i className="fa fa-times"></i>
                        </button>
                        </div>
                    {/* </div> */}
                </div>
            )
        })
    }

    renderVagasUsuario(){
        return (
            <div className="row">
                <div className="col-12 col-md-6">
                    <div className="form-group">
                        <label htmlFor="vagas">Adicionar vagas</label>
                        <select value={this.state.user.vagas} onChange={e => this.adicionaVaga(e)} name="vaga_select" className="form-control">
                            <option>Selecione</option>
                            {this.getOptionVagas()}
                        </select>
                    </div>
                </div>
                <div className="col-12 col-md-6">
                    <div className="form-group">
                        <div>
                        <label htmlFor="vagasAtreladas">Vagas do Usuário</label>
                        </div>
                        {this.getCardVagas()}
                    </div>
                </div>
            </div>
        )
    }

    renderForm() {
        return (
            <div className="form">
                <div className="row">
                    <div className="col-12 col-md-6">
                        <div className="form-group">
                            <label>Nome</label>
                            <input type="text" className="form-control"
                                name="nome"
                                value={this.state.user.nome}
                                onChange={e => this.updateField(e)}
                                placeholder="Digite o nome ..." />
                        </div>
                    </div>

                    <div className="col-12 col-md-6">
                        <div className="form-group">
                            <label>Sobrenome</label>
                            <input type="text" className="form-control"
                                name="sobrenome"
                                value={this.state.user.sobrenome}
                                onChange={e => this.updateField(e)}
                                placeholder="Digite o sobrenome ..." />
                        </div>
                    </div>

                </div>

                <div className="row">
                    <div className="col-12 col-md-6">
                        <div className="form-group">
                            <label>E-mail</label>
                            <input type="text" className="form-control"
                                name="email"
                                value={this.state.user.email}
                                onChange={e => this.updateField(e)}
                                placeholder="Digite o e-mail ... " />
                        </div>
                    </div>
                </div>

                <div className="row">
                    <div className="col-12 col-md-6">
                        <div className="form-group">
                            <label>Senha</label>
                            <input type="password" className="form-control"
                                name="senha"
                                value={this.state.user.senha}
                                onChange={e => this.updateField(e)}
                                placeholder="Digite a senha ..." />
                        </div>
                    </div>

                    <div className="col-12 col-md-6">
                        <div className="form-group">
                            <label>Confirme a Senha</label>
                            <input type="password" className="form-control"
                                name="senha_c"
                                value={this.state.user.senha_c}
                                onChange={e => this.updateField(e)}
                                placeholder="Digite a senha ..." />
                        </div>
                    </div>
                </div>

                <div className="row">
                    <div className="col-12 col-md-6">
                        <div className="form-group">
                            <label>Telefone Residencial</label>
                            <input type="text" className="form-control"
                                name="fone_residencial"
                                value={this.state.user.fone_residencial}
                                onChange={e => this.updateField(e)}
                                placeholder="Digite o telefone ..." />
                        </div>
                    </div>

                    <div className="col-12 col-md-6">
                        <div className="form-group">
                            <label>Telefone Comercial</label>
                            <input type="text" className="form-control"
                                name="fone_trabalho"
                                value={this.state.user.fone_trabalho}
                                onChange={e => this.updateField(e)}
                                placeholder="Digite a senha ..." />
                        </div>
                    </div>
                </div>

                <div className="row">
                    <div className="col-12 col-md-6">
                        <div className="form-group">
                            <label>Celular 1</label>
                            <input type="text" className="form-control"
                                name="celular_1"
                                value={this.state.user.celular_1}
                                onChange={e => this.updateField(e)}
                                placeholder="Digite o celular ..." />
                        </div>
                    </div>

                    <div className="col-12 col-md-6">
                        <div className="form-group">
                            <label>Celular 2</label>
                            <input type="text" className="form-control"
                                name="celular_2"
                                value={this.state.user.celular_2}
                                onChange={e => this.updateField(e)}
                                placeholder="Digite a senha ..." />
                        </div>
                    </div>
                </div>

                    {this.renderDropdownTipoUsuario()}
                    {this.renderVagasUsuario()}


                <hr />

                <div className="row">
                    <div className="col-12 d-flex justify-content-end">
                        <button className="btn btn-primary"
                            onClick={e => this.save(e)}>
                            Salvar
                        </button>
                        <button className="btn btn-secondary ml-2"
                            onClick={e => this.clear(e)}>
                            Cancelar
                        </button>
                    </div>
                </div>

            </div>
        )
    }

    load(user) {
        user.senha = ""
        user.senha_c = ""
        api.get(`/usuario/${user.id}/contato`).then(resp => {
            user.fone_residencial = resp.data.fone_residencial
            user.fone_trabalho = resp.data.fone_trabalho
            user.celular_1 = resp.data.celular_1
            user.celular_2 = resp.data.celular_2
            this.setState({user})
        })
    }

    remove(user) {
        api.delete(`/usuario/${user.id}`).then(resp => {
            const usuarios = this.getUpdatedList(user, false)
            this.setState({usuarios})
        })
    }

    renderTable() {
        return (
            <table className="table table-hover mt-4">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Sobrenome</th>
                        <th>E-mail</th>
                        <th>Tipo</th>
                        <th>Vagas</th>
                        <th>*</th>
                    </tr>
                </thead>
                <tbody>
                    {this.renderRows()}
                </tbody>
            </table>
        )
    }

    setModalShow(val) {
        this.setState({ modalShow : val })
    }

    abreDetalhesUsuario(usuario) {
        api.get(`/usuario/${usuario.id}/contato`).then(resp => {
            detalhesUsuario.contato = resp.data
            detalhesUsuario.nome = usuario.nome
            detalhesUsuario.sobrenome = usuario.sobrenome
            detalhesUsuario.email = usuario.email
            detalhesUsuario.tipo_str = usuario.tipo_str
            detalhesUsuario.dataCadastro = usuario.dataCadastro
            detalhesUsuario.vagas = usuario.vagas
            this.setModalShow(true)
        })
    } 

    getStringVagas(vagas) {
        if (vagas === undefined) return ''

        let identificadores = []
        vagas.forEach(vg => identificadores.push(vg.identificador))
        return identificadores.join(', ')
    }

    MyVerticallyCenteredModal(props) {
        return (
          <Modal
            {...props}
            size="lg"
            aria-labelledby="contained-modal-title-vcenter"
            centered
          >
            <Modal.Header closeButton>
              <Modal.Title id="contained-modal-title-vcenter">
                <h4>{detalhesUsuario.nome} {detalhesUsuario.sobrenome} ({detalhesUsuario.tipo_str.toLowerCase()})</h4>
              </Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <br />
              <p><b>E-mail:</b> {detalhesUsuario.email}</p>
              <p><b>Data de Cadastro:</b> {detalhesUsuario.dataCadastro}</p>
              <p><b>Vagas:</b> {detalhesUsuario.vagas.map(v => v.identificador).join(', ')}</p>
              <p><b>Telefone Residencial:</b> {detalhesUsuario.contato.fone_residencial}</p>
              <p><b>Telefone Comercial:</b> {detalhesUsuario.contato.fone_trabalho}</p>
              <p><b>Celular 1:</b> {detalhesUsuario.contato.celular_1}</p>
              <p><b>Celular 2:</b> {detalhesUsuario.contato.celular_2}</p>
            </Modal.Body>
            <Modal.Footer>
              <Button onClick={props.onHide}>Fechar</Button>
            </Modal.Footer>
          </Modal>
        );
      }


    renderRows() {
        return this.state.usuarios.map(user => {
            return (
                <tr key={user.id}>
                    <td onClick={e => this.abreDetalhesUsuario(user)}>{user.nome}</td>
                    <td onClick={e => this.abreDetalhesUsuario(user)}>{user.sobrenome}</td>
                    <td onClick={e => this.abreDetalhesUsuario(user)}>{user.email}</td>
                    <td onClick={e => this.abreDetalhesUsuario(user)}>{user.tipo_str}</td>
                    <td onClick={e => this.abreDetalhesUsuario(user)}>{this.getStringVagas(user.vagas)}</td>
                    <td>
                        <button className="btn btn-warning"
                            onClick={() => this.load(user)}>
                            <i className="fa fa-pencil"></i>
                        </button>
                        <button className="btn btn-danger ml-2"
                            onClick={() => this.remove(user)}>
                            <i className="fa fa-trash"></i>
                        </button>
                    </td>

                </tr>
            )
        })
    }

    render() {
        return (
            <Main {...headerProps}>
                {this.renderForm()}
                {this.renderTable()}
                <this.MyVerticallyCenteredModal
                    show={this.state.modalShow}
                    onHide={() => this.setModalShow(false)}/>
            </Main>
        )
    }
}