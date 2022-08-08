import React from 'react'
import { Switch, Route, Redirect } from 'react-router'

import AdminUsuarios from '../user/AdminUsuarios'
import AdminInicio from '../user/AdminInicio'
import AdminVagas from '../user/AdminVagas'
import PaginaLogin from '../login/PaginaLogin'

export default props =>
    <Switch>
        <Route exact path='/' component={AdminInicio} />
        <Route path='/users' component={AdminUsuarios} />
        <Route path='/vagas' component={AdminVagas} />
        <Route path='/logout' component={PaginaLogin}/>
        {/* <Route path='/logout' component={('a') => <PaginaLogin isAuthed={true}/> */}
        <Redirect from='*' to='/' />
    </Switch>