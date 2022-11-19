import axios from 'axios';
import { Navigate } from 'react-router-dom';
import { ErrorHandler } from '../utils';


const Logout = ({ username, setUsername, setMessage }) => {

  const errorHandler = new ErrorHandler(setMessage);

  const logout = async () => {
    try {
      const response = await axios.get(`user/logout/${username}`);
      localStorage.removeItem('username');
      localStorage.removeItem('token');
      setUsername('');
      setMessage({ text: `Logged out ${response.data}.`, variant: 'secondary' });
    } catch (error) {
      errorHandler.log(error);
    }
  }

  if (username) logout();

  return (
    <Navigate to="/" />
  );
}

export default Logout;