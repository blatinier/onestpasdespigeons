import axios from 'axios';


export const parseJSON = response => response.data;

export const createUser = (email, password) => axios.post('api/auth/create_user', { email, password });

export const getToken = (email, password) => axios.post('api/auth/get_token', { email, password });

