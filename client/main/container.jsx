import React, { PropTypes } from 'react';
import { Link } from 'react-router';
import { Nav, Navbar, NavItem } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';


const Main = ({ children }) => (
  <div>
    <Navbar>
      <Navbar.Header>
        <Navbar.Brand>
          <Link to="/home">OnEstPasDesPigeons</Link>
        </Navbar.Brand>
      </Navbar.Header>
      <Nav className="pull-right">
        <LinkContainer to="/statistic">
          <NavItem eventKey={2}>Statistics</NavItem>
        </LinkContainer>
        <LinkContainer to="/login">
          <NavItem eventKey={3}>LogIn</NavItem>
        </LinkContainer>
        <LinkContainer to="/register">
          <NavItem eventKey={4}>SignIn</NavItem>
        </LinkContainer>
      </Nav>
    </Navbar>
    {children}
  </div>
);

Main.propTypes = {
  children: PropTypes.node,
};

export default Main;
