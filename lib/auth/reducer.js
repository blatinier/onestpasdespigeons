'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

var _enum = require('./enum');

var initialState = {
  token: null,
  isAuthenticated: false,
  isAuthenticating: false,
  isRegistering: false
};

var authReducer = function authReducer() {
  var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : initialState;
  var action = arguments[1];

  switch (action.type) {
    case _enum.LOGIN_USER_REQUEST:
      return _extends({}, state, {
        isAuthenticating: true
      });
    case _enum.LOGIN_USER_SUCCESS:
      return _extends({}, state, {
        isAuthenticating: false,
        isAuthenticated: true,
        token: action.payload.token
      });
    case _enum.LOGIN_USER_FAILURE:
      return _extends({}, state, {
        isAuthenticating: false,
        isAuthenticated: false,
        token: null
      });
    case _enum.LOGOUT_USER:
      return _extends({}, state, {
        isAuthenticated: false,
        token: null
      });
    case _enum.REGISTER_USER_REQUEST:
      return _extends({}, state, {
        isRegistering: true
      });
    case _enum.REGISTER_USER_SUCCESS:
      return _extends({}, state, {
        isAuthenticating: false,
        isAuthenticated: true,
        isRegistering: false,
        token: action.payload.token
      });
    case _enum.REGISTER_USER_FAILURE:
      return _extends({}, state, {
        isAuthenticating: false,
        isAuthenticated: false,
        isRegistering: false,
        token: null
      });
    default:
      return state;
  }
};

exports.default = authReducer;