import React from 'react';
import { Button, Col } from 'react-bootstrap';
import FieldGroup from '../common/fieldgroup';


const RegisterView = () => (
  <Col lgOffset={4} lg={4}>
    <h1>
      Register
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
      <FieldGroup
        id="formControlsPasswordConfirm"
        label="Password Confirmation"
        type="password"
      />
      <Button type="submit">Register!</Button>
    </form>
  </Col>
);

export default RegisterView;
