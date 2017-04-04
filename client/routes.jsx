import React from 'react';
import { Route } from 'react-router';

// Main Container
import Main from './main/container';

// View
import HomeView from './home/view';
import StatisticView from './statistic/view';
import LoginView from './login/view';
import RegisterView from './register/view';
import NotFoundView from './common/notFoundView';

// Auth
import requireNoAuthentication from './auth/requireNoAuthentication';
import requireAuthentication from './auth/requireAuthentication';
import determineAuth from './auth/determineAuth';


const routes = (
  <Route path="/" component={Main}>
    <Route path="home" component={requireNoAuthentication(HomeView)} />
    <Route path="statistic" component={requireAuthentication(StatisticView)} />
    <Route path="login" component={requireNoAuthentication(LoginView)} />
    <Route path="register" component={requireNoAuthentication(RegisterView)} />
    <Route path="*" component={determineAuth(NotFoundView)} />
  </Route>
);

export default routes;
