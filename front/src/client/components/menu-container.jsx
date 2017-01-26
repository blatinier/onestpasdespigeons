import React, { PropTypes } from 'react';

const MenuContainer = ({ menu }) => <div>{menu}</div>;

MenuContainer.propTypes = {
  menu: PropTypes.string.isRequired,
};

export default MenuContainer;
