'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var Main = function Main(_ref) {
  var children = _ref.children;
  return _react2.default.createElement(
    'section',
    null,
    _react2.default.createElement(
      'div',
      null,
      children
    )
  );
};

Main.propTypes = {
  children: _react.PropTypes.node
};

exports.default = Main;