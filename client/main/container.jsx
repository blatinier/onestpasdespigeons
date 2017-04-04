import React, { PropTypes } from 'react';
import { Link } from 'react-router';


const Main = ({ children }) => (
  <div>
    <header>
      <Link to="/home">Home</Link>
      <Link to="/statistic">Statistics</Link>
      <Link to="/login">LogIn</Link>
      <Link to="/register">SignIn</Link>
    </header>
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
