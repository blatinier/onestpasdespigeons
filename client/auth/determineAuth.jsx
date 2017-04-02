import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import * as actionCreators from '../auth/actions';


const mapStateToProps = state => ({
  token: state.auth.token,
  userName: state.auth.userName,
  isAuthenticated: state.auth.isAuthenticated,
});

const mapDispatchToProps = dispatch => bindActionCreators(actionCreators, dispatch);

const determineAuth = (MyComponent) => {
  class AuthenticatedComponent extends Component {
    componentWillMount() {
      this.checkAuth();
      this.state = {
        loaded_if_needed: false,
      };
    }

    componentWillReceiveProps(nextProps) {
      this.checkAuth(nextProps);
    }

    checkAuth(props = this.props) {
      if (!props.isAuthenticated) {
        const token = localStorage.getItem('token');
        if (token) {
          fetch('api/is_token_valid', {
            method: 'post',
            credentials: 'include',
            headers: {
              'Accept': 'application/json', // eslint-disable-line quote-props
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ token }),
          })
          .then((res) => {
            if (res.status === 200) {
              this.props.loginUserSuccess(token);
              this.setState({
                loaded_if_needed: true,
              });
            }
          });
        }
      } else {
        this.setState({
          loaded_if_needed: true,
        });
      }
    }

    render() {
      return (
        <div>
          {this.state.loaded_if_needed
            ? <MyComponent {...this.props} />
            : null
          }
        </div>
      );
    }
  }

  AuthenticatedComponent.propTypes = {
    loginUserSuccess: React.PropTypes.func,
  };

  return connect(mapStateToProps, mapDispatchToProps)(AuthenticatedComponent);
};


export default determineAuth;
