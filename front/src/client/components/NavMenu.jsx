import React, { PropTypes } from 'react';
import { Link } from 'react-router';


const NavMenu = ({ menu, children }) => (
  <Link
    to={menu}
    activeStyle={{
      color: 'red',
    }}
  >
    {children}
  </Link>
);

NavMenu.propTypes = {
  menu: PropTypes.string.isRequired,
  children: PropTypes.string.isRequired,
};

export default NavMenu;
