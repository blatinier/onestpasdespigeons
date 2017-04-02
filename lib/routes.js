'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _reactRouter = require('react-router');

var _container = require('./main/container');

var _view = require('./home/view');

var _view2 = require('./statistic/view');

var _view3 = require('./login/view');

var _view4 = require('./register/view');

var _notFoundView = require('./common/notFoundView');

var _utils = require('./auth/utils');

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

// View
var routes = _react2.default.createElement(
  _reactRouter.Route,
  { path: '/', component: _container.Main },
  _react2.default.createElement(_reactRouter.Route, { path: 'home', component: (0, _utils.requireNoAuthentication)(_view.HomeView) }),
  _react2.default.createElement(_reactRouter.Route, { path: 'statistic', component: (0, _utils.requireAuthentication)(_view2.StatisticView) }),
  _react2.default.createElement(_reactRouter.Route, { path: 'login', component: (0, _utils.requireNoAuthentication)(_view3.LoginView) }),
  _react2.default.createElement(_reactRouter.Route, { path: 'register', component: (0, _utils.requireNoAuthentication)(_view4.RegisterView) }),
  _react2.default.createElement(_reactRouter.Route, { path: '*', component: (0, _utils.determineAuth)(_notFoundView.NotFoundView) })
);

// Auth


// Main Container
exports.default = routes;