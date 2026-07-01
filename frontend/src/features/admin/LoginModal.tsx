import { useState, useContext } from 'react';
import { adminApi } from '../../api/adminApi';
import { AdminContext } from '../../context/AdminContext';

export const LoginModal = ({ onClose }: { onClose: () => void }) => {
  const { login } = useContext(AdminContext);
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async () => {
    try {
      const res = await adminApi.signin(form.username, form.password);
      localStorage.setItem('admin_token', res.data.access_token);

      const me = await adminApi.getMe();
      login(me.data, res.data.access_token);
      onClose();
    } catch (err: any) {
      setError(err.response?.data?.detail || "Ошибка входа");
    }
  };

  return (
    <div style={{
      position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.8)', 
      display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 2000
    }}>
      <div className="form-container" style={{ width: '300px' }}>
        <h2 style={{ marginTop: 0 }}>ВХОД</h2>
        
        {error && (
          <div style={{ color: 'var(--accent-red)', marginBottom: '10px', fontWeight: 'bold' }}>
            {error}
          </div>
        )}
        
        <div className="form-group">
          <input 
            placeholder="ЛОГИН" 
            value={form.username} 
            onChange={e => setForm({...form, username: e.target.value})} 
          />
          <input 
            type="password" 
            placeholder="ПАРОЛЬ" 
            value={form.password} 
            onChange={e => setForm({...form, password: e.target.value})} 
          />
        </div>
        
        <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
          <button className="btn-green" onClick={handleLogin} style={{ flex: 1 }}>ВОЙТИ</button>
          <button className="btn-white" onClick={onClose} style={{ flex: 1 }}>ОТМЕНА</button>
        </div>
      </div>
    </div>
  );
};