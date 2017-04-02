import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { browserHistory } from 'react-router';
import { post } from 'axios';

import * as actionCreators from '../auth/actions';


const mapStateToProps = state => ({
  token: state.auth.token,
  isAuthenticated: state.auth.isAuthenticated,
});

const mapDispatchToProps = dispatch => (
  bindActionCreators(actionCreators, dispatch)
);

const requireNoAuthentication = (MyComponent) => {
  class notAuthenticatedComponent extends Component {
    constructor(props) {
      super(props);
      this.state = {
        loaded: false,
      };
    }

    componentWillMount() {
      this.checkAuth();
    }

    componentWillReceiveProps(nextProps) {
      this.checkAuth(nextProps);
    }

    checkAuth(props = this.props) {
      if (props.isAuthenticated) {
        browserHistory.push('/home');
      } else {
        const token = localStorage.getItem('token');
        if (token) {
          post(
            'api/auth/is_token_valid',
            JSON.stringify({ token }),
            {
              withCredentials: true,
              headers: {
                'Accept': 'application/json', // eslint-disable-line quote-props
                'Content-Type': 'application/json',
              }
            },
          )
            .then((res) => {
              if (res.status === 200) {
                this.props.loginUserSuccess(token);
                browserHistory.push('/home');
              } else {
                this.setState({
                  loaded: true,
                });
              }
            });
        } else {
          this.setState({ loaded: true, });
        }
      }
    }

    render() {
      const { isAuthenticated } = this.props;
      return (
        <div>
          {!isAuthenticated && this.state.loaded
          ? <MyComponent {...this.props} />
          : null
          }
        </div>
      );
    }
  }

  notAuthenticatedComponent.propTypes = {
    loginUserSuccess: React.PropTypes.func,
    isAuthenticated: React.PropTypes.bool,
  };

  return connect(mapStateToProps, mapDispatchToProps)(notAuthenticatedComponent);
};


export default requireNoAuthentication;
