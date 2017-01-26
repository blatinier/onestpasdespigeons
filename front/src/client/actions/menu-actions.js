import { createAction } from 'redux-actions';

export const SWITCH_MENU = 'SWITCH_MENU';
export const goToHomeMenu = createAction(SWITCH_MENU, () => 'home');
export const goToWorkflowMenu = createAction(SWITCH_MENU, () => 'workflow');
