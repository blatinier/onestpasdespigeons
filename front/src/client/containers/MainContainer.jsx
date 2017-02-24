import React, { PropTypes } from 'react';

import Home from '../components/Home';
import Statistic from '../components/Statistic';
import Login from '../components/Login';

const MainContainer = ({ menu }) => {
  switch (menu) {
    case 'home':
      return <Home />;
    case 'statistic':
      return <Statistic />;
    case 'login':
      return <Login />;
    default:
      return <Home />;
  }
};

MainContainer.propTypes = {
  menu: PropTypes.string,
};


export default MainContainer;
