import React, { PropTypes } from 'react';


const Main = ({ children }) => (
  <section>
    <div>
      {children}
    </div>
  </section>
);

Main.propTypes = {
  children: PropTypes.node,
};

export default Main;
