import React, { PropTypes } from 'react';

import MainMenu from './MainMenu';
import MainContainer from '../containers/MainContainer';


const App = ({ params }) => (
  <div>
    <MainMenu />
    <MainContainer menu={params.menu || 'home'} />
  </div>
);

App.propTypes = {
  params: PropTypes.object,
};

export default App;
