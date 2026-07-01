import { useState } from 'react';
import { adminApi } from '../../api/adminApi';

export const ChangePasswordModal = ({ onClose }: { onClose: () => void }) => {
  const [passwords, setPasswords] = useState({ old: '', new: '', confirm: '' });
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (passwords.new !== passwords.confirm) {
      setError("НОВЫЕ ПАРОЛИ НЕ СОВПАДАЮТ");
      return;
    }

    try {
      await adminApi.changePassword(passwords.old, passwords.new);
      setSuccess(true);
      setTimeout(onClose, 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || "ОШИБКА ПРИ СМЕНЕ ПАРОЛЯ");
    }
  };

  return (
    <div style={{ 
      position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.85)', 
      display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 6000 
    }}>
      <div className="form-container" style={{ width: '350px' }}>
        <h3 style={{ marginTop: 0, textTransform: 'uppercase' }}>СМЕНА ПАРОЛЯ</h3>
        
        {success ? (
          <p style={{ color: 'var(--accent-green)', fontWeight: 'bold' }}>ПАРОЛЬ УСПЕШНО ИЗМЕНЕН!</p>
        ) : (
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {error && <p style={{ color: 'var(--accent-red)', fontWeight: 'bold' }}>{error}</p>}
            
            <input 
              type="password" 
              placeholder="СТАРЫЙ ПАРОЛЬ" 
              onChange={e => setPasswords({...passwords, old: e.target.value})} 
              required 
            />
            <input 
              type="password" 
              placeholder="НОВЫЙ ПАРОЛЬ" 
              onChange={e => setPasswords({...passwords, new: e.target.value})} 
              required 
            />
            <input 
              type="password" 
              placeholder="ПОВТОРИТЕ НОВЫЙ ПАРОЛЬ" 
              onChange={e => setPasswords({...passwords, confirm: e.target.value})} 
              required 
            />
            
            <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
              <button type="submit" className="btn-green" style={{ flex: 1 }}>ИЗМЕНИТЬ</button>
              <button type="button" className="btn-white" onClick={onClose} style={{ flex: 1 }}>ОТМЕНА</button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};