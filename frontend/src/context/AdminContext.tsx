import { createContext, useState, useContext } from 'react';
import { useEffect } from 'react';
import { adminApi } from '../api/adminApi';

export const AdminContext = createContext<any>(null);

export const AdminProvider = ({ children }: any) => {
  const [admin, setAdmin] = useState(() => {
    try {
      const saved = localStorage.getItem('admin_data');
      return (saved && saved !== 'undefined') ? JSON.parse(saved) : null;
    } catch { return null; }
  });

  const login = (adminData: any, token: string) => {
    localStorage.setItem('admin_token', token);
    localStorage.setItem('admin_data', JSON.stringify(adminData));
    setAdmin(adminData);
  };

  const logout = () => {
    localStorage.removeItem('admin_token');
    localStorage.removeItem('admin_data');
    setAdmin(null);
  };

  useEffect(() => {
  const token = localStorage.getItem('admin_token');
  if (token) {
    adminApi.getMe()
      .then(res => login(res.data, token))
      .catch(() => {
        localStorage.removeItem('admin_token');
        logout(); 
      });
  }
}, []);

  return <AdminContext.Provider value={{ admin, login, logout }}>{children}</AdminContext.Provider>;
};

export const useAdmin = () => useContext(AdminContext);