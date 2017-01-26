import React, { PropTypes } from 'react';

const MainMenu = ({ homeAction, wfAction, currentMenu }) => {
  switch (currentMenu) {
    case 'workflow':
      return (<ul>
        <li><button type="button" onClick={homeAction}> Home </button></li>
        <li> Workflow </li>
      </ul>);
    default:
      return (<ul>
        <li> Home </li>
        <li><button type="button" onClick={wfAction}> Workflow </button></li>
      </ul>);
  }
};

MainMenu.propTypes = {
  homeAction: PropTypes.func.isRequired,
  wfAction: PropTypes.func.isRequired,
  currentMenu: PropTypes.string.isRequired,
};

export default MainMenu;
