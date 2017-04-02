'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.loginUserRequest = loginUserRequest;
exports.loginUserSuccess = loginUserSuccess;
exports.loginUserFailure = loginUserFailure;
exports.logout = logout;
exports.logoutAndRedirect = logoutAndRedirect;
exports.redirectToRoute = redirectToRoute;
exports.loginUser = loginUser;
exports.registerUserRequest = registerUserRequest;
exports.registerUserSuccess = registerUserSuccess;
exports.registerUserFailure = registerUserFailure;
exports.registerUser = registerUser;

var _reactRouter = require('react-router');

var _enum = require('./enum');

var _common = require('../utils/common');

function loginUserRequest() {
  return {
    type: _enum.LOGIN_USER_REQUEST
  };
}

function loginUserSuccess(token) {
  localStorage.setItem('token', token);
  return {
    type: _enum.LOGIN_USER_SUCCESS,
    payload: {
      token: token
    }
  };
}

function loginUserFailure(error) {
  localStorage.removeItem('token');
  return {
    type: _enum.LOGIN_USER_FAILURE,
    payload: {
      status: error.status
    }
  };
}

function logout() {
  localStorage.removeItem('token');
  return {
    type: _enum.LOGOUT_USER
  };
}

function logoutAndRedirect() {
  return function (dispatch) {
    dispatch(logout());
    _reactRouter.browserHistory.push('/');
  };
}

function redirectToRoute(route) {
  return function () {
    _reactRouter.browserHistory.push(route);
  };
}

function loginUser(email, password) {
  return function (dispatch) {
    dispatch(loginUserRequest());
    return (0, _common.getToken)(email, password).then(_common.parseJSON).then(function (response) {
      try {
        dispatch(loginUserSuccess(response.token));
        _reactRouter.browserHistory.push('/main');
      } catch (e) {
        dispatch(loginUserFailure({
          response: {
            status: 403,
            statusText: 'Invalid token'
          }
        }));
      }
    }).catch(function (error) {
      dispatch(loginUserFailure(error));
    });
  };
}

function registerUserRequest() {
  return {
    type: _enum.REGISTER_USER_REQUEST
  };
}

function registerUserSuccess(token) {
  localStorage.setItem('token', token);
  return {
    type: _enum.REGISTER_USER_SUCCESS,
    payload: {
      token: token
    }
  };
}

function registerUserFailure(error) {
  localStorage.removeItem('token');
  return {
    type: _enum.REGISTER_USER_FAILURE,
    payload: {
      status: error.status,
      statusText: error.statusText
    }
  };
}

function registerUser(email, password) {
  return function (dispatch) {
    dispatch(registerUserRequest());
    return (0, _common.createUser)(email, password).then(_common.parseJSON).then(function (response) {
      try {
        dispatch(registerUserSuccess(response.token));
        _reactRouter.browserHistory.push('/main');
      } catch (e) {
        dispatch(registerUserFailure({
          response: {
            status: 403,
            statusText: 'Invalid token'
          }
        }));
      }
    }).catch(function (error) {
      dispatch(registerUserFailure(error));
    });
  };
}