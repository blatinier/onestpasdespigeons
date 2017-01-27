import { connect } from 'react-redux';
import MenuContainer from '../components/menu-container';

const mapStateToProps = state => ({
  menu: state.get('menu').get('section')
});

export default connect(mapStateToProps)(MenuContainer);
