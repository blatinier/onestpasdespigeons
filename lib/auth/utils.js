'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _reactRedux = require('react-redux');

var _redux = require('redux');

var _reactRouter = require('react-router');

var _axios = require('axios');

var _actions = require('../auth/actions');

var actionCreators = _interopRequireWildcard(_actions);

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var mapStateToProps = function mapStateToProps(state) {
  return {
    token: state.auth.token,
    isAuthenticated: state.auth.isAuthenticated
  };
};

var mapDispatchToProps = function mapDispatchToProps(dispatch) {
  return (0, _redux.bindActionCreators)(actionCreators, dispatch);
};

var requireNoAuthentication = function requireNoAuthentication(MyComponent) {
  var notAuthenticatedComponent = function (_Component) {
    _inherits(notAuthenticatedComponent, _Component);

    function notAuthenticatedComponent(props) {
      _classCallCheck(this, notAuthenticatedComponent);

      var _this = _possibleConstructorReturn(this, (notAuthenticatedComponent.__proto__ || Object.getPrototypeOf(notAuthenticatedComponent)).call(this, props));

      _this.state = {
        loaded: false
      };
      return _this;
    }

    _createClass(notAuthenticatedComponent, [{
      key: 'componentWillMount',
      value: function componentWillMount() {
        this.checkAuth();
      }
    }, {
      key: 'componentWillReceiveProps',
      value: function componentWillReceiveProps(nextProps) {
        this.checkAuth(nextProps);
      }
    }, {
      key: 'checkAuth',
      value: function checkAuth() {
        var _this2 = this;

        var props = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : this.props;

        if (props.isAuthenticated) {
          _reactRouter.browserHistory.push('/home');
        } else {
          (function () {
            var token = localStorage.getItem('token');
            if (token) {
              (0, _axios.post)('api/auth/is_token_valid', JSON.stringify({ token: token }), {
                withCredentials: true,
                headers: {
                  'Accept': 'application/json', // eslint-disable-line quote-props
                  'Content-Type': 'application/json'
                }
              }).then(function (res) {
                if (res.status === 200) {
                  _this2.props.loginUserSuccess(token);
                  _reactRouter.browserHistory.push('/home');
                } else {
                  _this2.setState({
                    loaded: true
                  });
                }
              });
            } else {
              _this2.setState({ loaded: true });
            }
          })();
        }
      }
    }, {
      key: 'render',
      value: function render() {
        var isAuthenticated = this.props.isAuthenticated;

        return _react2.default.createElement(
          'div',
          null,
          !isAuthenticated && this.state.loaded ? _react2.default.createElement(MyComponent, this.props) : null
        );
      }
    }]);

    return notAuthenticatedComponent;
  }(_react.Component);

  notAuthenticatedComponent.propTypes = {
    loginUserSuccess: _react2.default.PropTypes.func,
    isAuthenticated: _react2.default.PropTypes.bool
  };

  return (0, _reactRedux.connect)(mapStateToProps, mapDispatchToProps)(notAuthenticatedComponent);
};

exports.default = requireNoAuthentication;