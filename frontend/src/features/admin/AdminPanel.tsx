import { useState } from 'react';
import { useAdmin } from '../../context/AdminContext';
import { adminApi } from '../../api/adminApi';
import { AdminManagementModal } from './AdminManagementModal';
import { PasswordModal } from './PasswordModal';
import { ChangePasswordModal } from './ChangePasswordModal';

export const AdminPanel = () => {
  const { admin, logout } = useAdmin();
  
  const [showManageModal, setShowManageModal] = useState(false);
  const [showPassModal, setShowPassModal] = useState(false);
  const [passError, setPassError] = useState<string | null>(null);
  const [showChangePass, setShowChangePass] = useState(false);

  const handleDeleteMe = async (password: string) => {
    try {
      await adminApi.deleteMyAccount(password);
      setShowPassModal(false);
      setPassError(null);
      logout(); 
    } catch (e: any) {
      setPassError(e.response?.data?.detail || "Ошибка удаления аккаунта");
    }
  };

  if (!admin) return null;

  return (
    <div style={{ 
      padding: '20px', 
      border: '2px solid var(--border-color)',
      marginBottom: '20px',
      display: 'flex',
      flexWrap: 'wrap',
      alignItems: 'center',
      gap: '15px'
    }}>
      <div style={{ marginRight: 'auto' }}>
        <strong style={{ textTransform: 'uppercase' }}>Админ: </strong> {admin.username} 
        <span style={{ marginLeft: '10px', opacity: 0.7 }}>
          [{admin.admin_type}]
        </span>
      </div>

      <div style={{ display: 'flex', gap: '10px' }}>
        <button className="btn-white" onClick={logout}>ВЫЙТИ</button>
        <button className="btn-white" onClick={() => setShowChangePass(true)}>СМЕНИТЬ ПАРОЛЬ</button>
        <button 
          className="btn-red" 
          onClick={() => setShowPassModal(true)}
        >
          УДАЛИТЬ АККАУНТ
        </button>

        {admin.admin_type === 'superadmin' && (
          <button 
            className="btn-green"
            onClick={() => setShowManageModal(true)}
          >
            ВСЕ АДМИНЫ
          </button>
        )}
      </div>

      {showManageModal && (
        <AdminManagementModal onClose={() => setShowManageModal(false)} />
      )}
      {showChangePass && <ChangePasswordModal onClose={() => setShowChangePass(false)} />}
      <PasswordModal 
        isOpen={showPassModal} 
        onClose={() => { setShowPassModal(false); setPassError(null); }}
        onConfirm={handleDeleteMe}
        title="ПОДТВЕРЖДЕНИЕ УДАЛЕНИЯ"
        error={passError}
      />
    </div>
  );
};