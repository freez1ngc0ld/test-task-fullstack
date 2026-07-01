import { useState } from 'react';

export const PasswordModal = ({ 
  isOpen, 
  onClose, 
  onConfirm, 
  title = "ПОДТВЕРЖДЕНИЕ",
  error = null 
}: { 
  isOpen: boolean; 
  onClose: () => void; 
  onConfirm: (password: string) => void;
  title?: string;
  error?: string | null;
}) => {
  const [password, setPassword] = useState('');

  if (!isOpen) return null;

  return (
    <div style={{ 
      position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.85)', 
      display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 3000 
    }}>
      <div className="form-container" style={{ width: '300px' }}>
        <h3 style={{ marginTop: 0, textTransform: 'uppercase' }}>{title}</h3>

        {error && (
          <p style={{ color: 'var(--accent-red)', fontSize: '0.9em', marginBottom: '15px', fontWeight: 'bold' }}>
            {error}
          </p>
        )}
        
        <input 
          type="password" 
          autoFocus
          placeholder="ВВЕДИТЕ ПАРОЛЬ" 
          style={{ width: '100%', marginBottom: '15px', boxSizing: 'border-box' }}
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
        />
        
        <div style={{ display: 'flex', gap: '10px' }}>
          <button 
            className="btn-green" 
            style={{ flex: 1 }} 
            onClick={() => onConfirm(password)}
          >
            ПОДТВЕРДИТЬ
          </button>
          <button 
            className="btn-white" 
            style={{ flex: 1 }} 
            onClick={onClose}
          >
            ОТМЕНА
          </button>
        </div>
      </div>
    </div>
  );
};