import React, { PropTypes } from 'react';
import { FormGroup, ControlLabel, FormControl,
         HelpBlock, Button } from 'react-bootstrap';

const FieldGroup = ({ id, label, help, ...props }) => (
  <FormGroup controlId={id}>
    <ControlLabel>{label}</ControlLabel>
    <FormControl {...props} />
    {help && <HelpBlock>{help}</HelpBlock>}
  </FormGroup>
);

FieldGroup.propTypes = {
  id: PropTypes.string,
  label: PropTypes.string,
  help: PropTypes.string
};

const LoginView = () => (
  <div>
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
      <Button type="submit">Submit</Button>
    </form>
  </div>
);

export default LoginView;
