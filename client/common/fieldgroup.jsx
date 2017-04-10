import React, { PropTypes } from 'react';
import { FormGroup, ControlLabel, FormControl,
         HelpBlock } from 'react-bootstrap';


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

export default FieldGroup;
