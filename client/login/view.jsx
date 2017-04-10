import React from 'react';
import { Button, Col } from 'react-bootstrap';
import FieldGroup from '../common/fieldgroup';

const LoginView = () => (
  <Col lgOffset={4} lg={4}>
    <h1>
      Login
    </h1>
    <form>
      <FieldGroup
        id="formControlsEmail"
        type="email"
        label="Email address"
        placeholder="Enter email"
      />
      <FieldGroup
        id="formControlsPassword"
        label="Password"
        type="password"
      />
      <Button type="submit">Login!</Button>
    </form>
  </Col>
);

export default LoginView;
