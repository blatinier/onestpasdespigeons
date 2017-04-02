'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.getToken = exports.createUser = exports.parseJSON = undefined;

var _axios = require('axios');

var _axios2 = _interopRequireDefault(_axios);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var parseJSON = exports.parseJSON = function parseJSON(response) {
  return response.data;
};

var createUser = exports.createUser = function createUser(email, password) {
  return _axios2.default.post('api/auth/create_user', { email: email, password: password });
};

var getToken = exports.getToken = function getToken(email, password) {
  return _axios2.default.post('api/auth/get_token', { email: email, password: password });
};