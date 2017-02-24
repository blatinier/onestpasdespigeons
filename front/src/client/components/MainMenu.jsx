//  import React, { PropTypes } from 'react';
import React from 'react';
import NavMenu from './NavMenu';

const MainMenu = () => (
  <p>
    <NavMenu menu="home">
      Home
    </NavMenu>
    -
    <NavMenu menu="statistic">
      Statistic
    </NavMenu>
    -
    <NavMenu menu="login">
      Login
    </NavMenu>
  </p>
);

export default MainMenu;
