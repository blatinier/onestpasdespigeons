import { connect } from 'react-redux';
import MenuContainer from '../components/menu-container';

const mapStateToProps = state => ({
  menu: state.get('menu').get('menu')
});

export default connect(mapStateToProps)(MenuContainer);
