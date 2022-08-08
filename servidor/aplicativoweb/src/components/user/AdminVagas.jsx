import React, { Component } from 'react'
// import axios from 'axios'
import Main from '../templates/Main'
import api from '../../services/api'

const headerProps = {
    icon: 'car',
    title: 'Vagas',
    subtitle: 'Cadastro de vagas: Incluir, Listar, Alterar e Excluir!'
}

// const baseUrl = 'http://localhost:5000/vaga'
const initialState = {
    vaga: { id: '', identificador: '', tipo: '', codigo: '', tipo_str: ''},
    vagasDisponiveis: [],
    vagasIndisponiveis: []
}

export default class Vagas extends Component {
    state = { ...initialState }

    componentWillMount() {
        api.get("/vagas").then(resp => {
            this.setState({ vagasDisponiveis: resp.data.vagas })
        })

        api.get("/indisponiveis").then(resp => {
            this.setState({ vagasIndisponiveis: resp.data.vagas })
        })

    }

    clear() {
        this.setState({vaga: initialState.vaga})
    }

    save() {
        const vaga = this.state.vaga

        if (vaga.id) {
            api.put(`/vaga/${vaga.id}`, vaga).then(resp => {
                const vagas = this.getUpdatedList(resp.data.vaga)
                this.setState({ vaga: initialState.vaga, vagasDisponiveis: vagas })
            })
        } else {
            api.post("/vaga", vaga).then(resp => {
                const vagas = this.getUpdatedList(resp.data.vaga)
                this.setState({ vaga: initialState.vaga, vagasDisponiveis: vagas })
            })
        }
        
        // const method = vaga.id ? 'put' : 'post'
        // const url = vaga.id ? `${baseUrl}/${vaga.id}` : baseUrl
        // axios[method](url, vaga)
        //     .then(resp => {
        //         const vagas = this.getUpdatedList(resp.data.vaga)
        //         this.setState({ vaga: initialState.vaga, vagasDisponiveis: vagas })
        //     })
    }

    getUpdatedList(vaga, add = true) {
        const list = this.state.vagasDisponiveis.filter(v => v.id !== vaga.id)
        if (add) list.unshift(vaga)
        // list.unshift(user) // poe na primeira posicao do array
        return list
    }

    updateField(event) {
        // nao é interessante alterar diretamente o state
        // pois pra isso existe a funcao setState
        // desta forma, vamos criar uma cópia através do operador spread
        const vaga = { ...this.state.vaga }
        vaga[event.target.name] = event.target.value
        if (event.target.name === 'tipo_str') {
            vaga.tipo = event.target.value === 'Comum' ? 1 : 2
        }
        this.setState({vaga})
    }

    renderDropdownTipoVaga(){
        return (
        <div class="col-12 col-md-6">
            <div class="form-group">
                <label for="tipo">Tipo</label>
                <select value={this.state.vaga.tipo_str} onChange={e => this.updateField(e)} name="tipo_str" class="form-control">
                    <option>Selecione</option>
                    <option value="Comum">Comum</option>
                    <option value="Preferencial">Preferencial</option>
                </select>
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
                            <label>Identificador</label>
                            <input type="text" className="form-control"
                                name="identificador"
                                value={this.state.vaga.identificador}
                                onChange={e => this.updateField(e)}
                                placeholder="Digite o identificador ..." />
                        </div>
                    </div>
                    <div className="col-12 col-md-6">
                        <div className="form-group">
                            <label>Código RFID</label>
                            <input type="text" className="form-control"
                                name="codigo"
                                value={this.state.vaga.codigo}
                                onChange={e => this.updateField(e)}
                                placeholder="Digite o código RFID ... " />
                        </div>
                    </div>
                </div>

                <div className="row">
                    {this.renderDropdownTipoVaga()}
                </div>

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

    load(vaga) {
        this.setState({ vaga })
    }

    remove(vaga) {
        let disponivel = false
        if (this.state.vagasDisponiveis.filter(v => v.id === vaga.id).length > 0)
            disponivel = true

        api.delete(`/vaga/${vaga.id}`).then(resp => {
            const vagas = this.getUpdatedList(vaga, false)
            if (disponivel)
                this.setState({ vagasDisponiveis: vagas })
            else
                this.setState({ vagasinDisponiveis: vagas })
        })

        // axios.delete(`${baseUrl}/${vaga.id}`).then(resp => {
        //     const vagas = this.getUpdatedList(vaga, false)
        //     if (disponivel)
        //         this.setState({ vagasDisponiveis: vagas })
        //     else
        //         this.setState({ vagasIndisponiveis: vagas })
        // })
    }

    renderTable() {
        return (
            <table className="table mt-4">
                <thead>
                    <tr>
                        <th>Identificador</th>
                        <th>Código</th>
                        <th>Tipo</th>
                        <th>*</th>
                    </tr>
                </thead>
                <tbody>
                    {this.renderRowsIndisponiveis()}
                    {this.renderRowsDisponiveis()}
                </tbody>
            </table>
        )
    }

    renderRowsDisponiveis() {
        return this.state.vagasDisponiveis.map(vaga => {
            return (
                <tr key={vaga.id}>
                    <td>{vaga.identificador}</td>
                    <td>{vaga.codigo}</td>
                    <td>{vaga.tipo_str}</td>
                    <td>
                        <button className="btn btn-warning"
                            onClick={() => this.load(vaga)}>
                            <i className="fa fa-pencil"></i>
                        </button>
                        <button className="btn btn-danger ml-2"
                            onClick={() => this.remove(vaga)}>
                            <i className="fa fa-trash"></i>
                        </button>
                    </td>

                </tr>
            )
        })
    }

    renderRowsIndisponiveis() {
        return this.state.vagasIndisponiveis.map(vaga => {
            return (
                <tr key={vaga.id}>
                    <td>{vaga.identificador}</td>
                    <td>{vaga.codigo}</td>
                    <td>{vaga.tipo_str}</td>
                    <td>
                        <button className="btn btn-warning"
                            onClick={() => this.load(vaga)}>
                            <i className="fa fa-pencil"></i>
                        </button>
                        <button className="btn btn-danger ml-2"
                            onClick={() => this.remove(vaga)}>
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
            </Main>
        )
    }
}