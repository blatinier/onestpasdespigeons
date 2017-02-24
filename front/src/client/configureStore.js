import { combineReducers } from 'redux-immutable';
import { createStore } from 'redux';


const configureStore = () => {
  const store = createStore(combineReducers({
  }));

  return store;
};

export default configureStore;
