// @flow

import React from 'react';
import ReactDOM from 'react-dom';
import { combineReducers } from 'redux-immutable';
import { createStore } from 'redux';
import { Provider } from 'react-redux';
import menuReducer from './reducers/menu-reducer';
import MainMenu from './containers/main-menu';
import MenuContainer from './containers/menu-container';

const store = createStore(combineReducers({
  menu: menuReducer,
}));

ReactDOM.render(
  <Provider store={store}>
    <div>
      <MainMenu />
      <MenuContainer />
    </div>
  </Provider>
  , document.querySelector('.app')
);
