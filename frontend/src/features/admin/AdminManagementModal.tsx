import { useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { adminApi } from '../../api/adminApi';
import { ConfirmModal } from './ConfirmModal';

export const AdminManagementModal = ({ onClose }: { onClose: () => void }) => {
  const queryClient = useQueryClient();
  const [offset, setOffset] = useState(0);
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState<string | null>(null);
  
  const [confirmAction, setConfirmAction] = useState<{ isOpen: boolean; id: string | null }>({ 
    isOpen: false, 
    id: null 
  });

  const limit = 10;
  const { data: response, isLoading } = useQuery({
    queryKey: ['admins', offset],
    queryFn: () => adminApi.listAdmins(offset, limit + 1),
  });

  const admins = response?.data || [];
  const displayAdmins = admins.slice(0, limit);
  const hasNextPage = admins.length > limit;

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      await adminApi.signup(form.username, form.password);
      queryClient.invalidateQueries({ queryKey: ['admins'] });
      setForm({ username: '', password: '' });
    } catch (err: any) { 
      setError(err.response?.data?.detail || "Ошибка создания администратора"); 
    }
  };

  const handleDelete = async () => {
    if (!confirmAction.id) return;
    setError(null);
    try {
      await adminApi.deleteAccount(confirmAction.id);
      queryClient.invalidateQueries({ queryKey: ['admins'] });
      setConfirmAction({ isOpen: false, id: null });
    } catch (err: any) { 
      setError(err.response?.data?.detail || "Ошибка удаления администратора"); 
    }
  };

  return (
    <div style={{ 
      position: 'fixed', inset: 0, background: 'var(--bg-color)', zIndex: 5000, 
      display: 'flex', flexDirection: 'column', padding: '40px', overflowY: 'auto' 
    }}>
      <div style={{ maxWidth: '800px', margin: '0 auto', width: '100%' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
          <h2>УПРАВЛЕНИЕ АДМИНАМИ</h2>
          <button className="btn-white" onClick={onClose}>ЗАКРЫТЬ</button>
        </div>

        {error && (
          <div style={{ color: 'var(--accent-red)', padding: '15px', border: '2px solid var(--accent-red)', marginBottom: '20px', fontWeight: 'bold' }}>
            {error}
          </div>
        )}

        <div className="form-container" style={{ marginBottom: '30px' }}>
          <h4 style={{ marginTop: 0 }}>ДОБАВИТЬ АДМИНИСТРАТОРА</h4>
          <form onSubmit={handleSignup} style={{ display: 'flex', gap: '10px' }}>
            <input placeholder="USERNAME" value={form.username} onChange={e => setForm({...form, username: e.target.value})} style={{ flex: 1 }} />
            <input type="password" placeholder="PASSWORD" value={form.password} onChange={e => setForm({...form, password: e.target.value})} style={{ flex: 1 }} />
            <button className="btn-green" type="submit">СОЗДАТЬ</button>
          </form>
        </div>

        {isLoading ? <div>ЗАГРУЗКА...</div> : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {displayAdmins.map((a: any) => (
              <div key={a.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '15px', border: '2px solid var(--border-color)' }}>
                <div>
                  <strong>{a.username.toUpperCase()}</strong>
                  <div style={{ fontSize: '0.8em', opacity: 0.7 }}>{a.admin_type}</div>
                </div>
                {a.admin_type !== 'superadmin' && (
                  <button className="btn-red" onClick={() => setConfirmAction({ isOpen: true, id: a.id })}>УДАЛИТЬ</button>
                )}
              </div>
            ))}
          </div>
        )}

        <div style={{ marginTop: '30px', display: 'flex', gap: '10px' }}>
          <button className="btn-white" disabled={offset === 0} onClick={() => setOffset(o => Math.max(0, o - 10))}>PREV</button>
          <span style={{ alignSelf: 'center', padding: '0 10px' }}>СТРАНИЦА: {offset / 10 + 1}</span>
          <button className="btn-white" disabled={!hasNextPage} onClick={() => setOffset(o => o + 10)}>NEXT</button>
        </div>
      </div>

      <ConfirmModal 
        isOpen={confirmAction.isOpen}
        onClose={() => setConfirmAction({ isOpen: false, id: null })}
        onConfirm={handleDelete}
        message="ВЫ ДЕЙСТВИТЕЛЬНО ХОТИТЕ УДАЛИТЬ ЭТОГО АДМИНИСТРАТОРА?"
        confirmText="УДАЛИТЬ"
      />
    </div>
  );
};