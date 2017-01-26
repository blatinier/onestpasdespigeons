import Immutable from 'immutable';
import { SWITCH_MENU } from '../actions/menu-actions';

const initialState = Immutable.Map({
  menu: 'home',
});

const menuReducer = (state = initialState, action) => {
  switch (action.type) {
    case SWITCH_MENU:
      return state.set('menu', action.payload);
    default:
      return state;
  }
};

export default menuReducer;
