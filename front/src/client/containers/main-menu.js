import { connect } from 'react-redux';
import MainMenu from '../components/main-menu';
import { goToHomeMenu, goToWorkflowMenu } from '../actions/menu-actions';

const mapStateToProps = state => ({
  currentMenu: state.get('menu').get('section')
});

const mapDispatchToProps = dispatch => ({
  homeAction: () => { dispatch(goToHomeMenu()); },
  wfAction: () => { dispatch(goToWorkflowMenu()); },
});

export default connect(mapStateToProps, mapDispatchToProps)(MainMenu);
