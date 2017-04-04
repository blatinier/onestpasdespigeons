import React, { PropTypes } from 'react';
import { Link } from 'react-router';
import { Nav, Navbar, NavItem } from 'react-bootstrap';


// http://stackoverflow.com/a/36933127/1450754

const Main = ({ children }) => (
  <div className="container-fluid">
    <Navbar>
      <Navbar.Header>
        <Navbar.Brand>
          <Link to="/home">OnEstPasDesPigeons</Link>
        </Navbar.Brand>
      </Navbar.Header>
      <Nav>
        <NavItem eventKey={2}>
          <Link to="/statistic">Statistics</Link>
        </NavItem>
        <NavItem eventKey={3}>
          <Link to="/login">LogIn</Link>
        </NavItem>
        <NavItem eventKey={4}>
          <Link to="/register">SignIn</Link>
        </NavItem>
      </Nav>
    </Navbar>
    <section>
      <div>
        {children}
      </div>
    </section>
  </div>
);

Main.propTypes = {
  children: PropTypes.node,
};

export default Main;
