// @flow
/* eslint-disable import/no-extraneous-dependencies, no-unused-expressions */

import { createStore } from 'redux';
import { combineReducers } from 'redux-immutable';
import { should } from 'chai';
import { describe, it, beforeEach } from 'mocha';
import menuReducer from '../../client/reducers/menu-reducer';
import { goToWorkflowMenu } from '../../client/actions/menu-actions';

should();
let store;

describe('App State', () => {
  describe('Menu', () => {
    beforeEach(() => {
      store = createStore(combineReducers({
        menu: menuReducer
      }));
    });
    describe('goToWorkflow', () => {
      it('should change menu to workflow', () => {
        store.getState().getIn(['menu', 'section']).should.equal('home');
        store.dispatch(goToWorkflowMenu());
        store.getState().getIn(['menu', 'section']).should.equal('workflow');
      });
    });
  });
});
