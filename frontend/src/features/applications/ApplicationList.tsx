import { useState, useContext } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { applicationApi } from '../../api/applicationApi';
import { AdminContext } from '../../context/AdminContext';
import { AdminPanel } from '../admin/AdminPanel';
import { LoginModal } from '../admin/LoginModal';
import { ConfirmModal } from './ConfirmModal';
import { ApplicationItem } from './ApplicationItem';
import { ApplicationSearchForm } from './ApplicationSearchForm';
import { ApplicationForm } from './ApplicationForm';
import { useSelection } from '../../hooks/useSelection';
import { ListParams, Application } from '../../types/application';

export const ApplicationList = () => {
  const queryClient = useQueryClient();
  const { admin } = useContext(AdminContext);
  const { selectedIds, toggleSelect, clearSelection } = useSelection();
  
  const limit = 10;
  const [params, setParams] = useState<ListParams>({ 
    offset: 0, 
    limit: limit, 
    sort_desc: true, 
    sort_by_priority: false 
  });
  
  const [editingApp, setEditingApp] = useState<Application | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [showLogin, setShowLogin] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);

  const { data, isLoading } = useQuery({
    queryKey: ['applications', params],
    queryFn: () => applicationApi.getAll({ ...params, limit: limit + 1 }).then(res => res.data),
  });

  const applications = data || [];
  const displayApps = applications.slice(0, limit);
  const hasNextPage = applications.length > limit;

  const handleSave = async (data: any) => {
    try {
      if (editingApp) await applicationApi.update(editingApp.id, data);
      else await applicationApi.create(data);
      setEditingApp(null);
      setIsCreating(false);
      setFormError(null);
      queryClient.invalidateQueries({ queryKey: ['applications'] });
    } catch (err: any) {
      setFormError(err.response?.data?.detail || "Ошибка сохранения");
    }
  };

  const handleDeleteMany = async () => {
    try {
      await applicationApi.deleteMany(Array.from(selectedIds));
      clearSelection();
      setShowConfirm(false);
      queryClient.invalidateQueries({ queryKey: ['applications'] });
      setFormError(null);
    } catch (err: any) {
      setFormError(err.response?.data?.detail || "Ошибка удаления");
      setShowConfirm(false);
    }
  };

  const handleStatusChange = async (appId: string, newStatus: string) => {
    try {
      await applicationApi.update(appId, { status: newStatus });
      queryClient.invalidateQueries({ queryKey: ['applications'] });
      setFormError(null);
    } catch (err: any) {
      setFormError(err.response?.data?.detail || "Ошибка смены статуса");
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      {admin ? <AdminPanel /> : <button className="btn-white" onClick={() => setShowLogin(true)}>ВХОД ДЛЯ АДМИНИСТРАТОРА</button>}
      
      {showLogin && <LoginModal onClose={() => setShowLogin(false)} />}
      <ConfirmModal 
        isOpen={showConfirm} 
        onClose={() => setShowConfirm(false)}
        onConfirm={handleDeleteMany}
        message={`УДАЛИТЬ ВЫБРАННЫЕ (${selectedIds.size}) ЗАЯВКИ?`}
      />

      <hr style={{ margin: '20px 0', borderColor: 'white' }} />

      {formError && (
        <p style={{ color: 'var(--accent-red)', marginBottom: '20px', padding: '10px', border: '1px solid var(--accent-red)', fontWeight: 'bold' }}>
          {formError}
        </p>
      )}

      {(isCreating || editingApp) && (
        <ApplicationForm 
          initialData={editingApp || undefined} 
          onSubmit={handleSave} 
          onCancel={() => {setEditingApp(null); setIsCreating(false); setFormError(null)}} 
          error={formError} 
        />
      )}

      <div style={{ marginBottom: '20px', display: 'flex', gap: '10px' }}>
        <button className="btn-white" onClick={() => setIsCreating(true)}>+ СОЗДАТЬ ЗАЯВКУ</button>
        {admin && selectedIds.size > 0 && (
          <button className="btn-red" onClick={() => setShowConfirm(true)}>
            УДАЛИТЬ ВЫБРАННЫЕ ({selectedIds.size})
          </button>
        )}
      </div>
      
      <ApplicationSearchForm initialParams={params} onSearch={(p) => setParams({...p, offset: 0})} />

      {isLoading ? (
        <div>ЗАГРУЗКА...</div>
      ) : (
        <div>
          {displayApps.map((app: Application) => {
            const isDone = app.status === 'done';
            const isSelected = selectedIds.has(app.id);

            return (
              <div key={app.id} className={`app-card ${isSelected ? 'selected' : ''} ${isDone ? 'done' : ''}`}>
                <ApplicationItem app={app} />
                
                <div style={{ marginTop: '10px', display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                  {admin && !isDone && (
                    <button className={isSelected ? 'btn-green' : 'btn-white'} onClick={() => toggleSelect(app.id)}>
                      {isSelected ? 'ВЫБРАНО ✅' : 'ВЫБРАТЬ'}
                    </button>
                  )}
                  
                  {!isDone ? (
                    <>
                      <button className="btn-white" onClick={() => setEditingApp(app)}>ИЗМЕНИТЬ</button>
                      {app.status === 'new' && (
                        <button className="btn-white" onClick={() => handleStatusChange(app.id, 'in_progress')}>В РАБОТУ 🚀</button>
                      )}
                      {app.status === 'in_progress' && (
                        <button className="btn-green" onClick={() => handleStatusChange(app.id, 'done')}>ЗАВЕРШИТЬ ✅</button>
                      )}
                    </>
                  ) : (
                    <span style={{ fontSize: '0.8em', opacity: 0.6, marginTop: '10px' }}>(ЗАВЕРШЕНО)</span>
                  )}
                </div>
              </div>
            );
          })}
          
          <div style={{ marginTop: '20px', display: 'flex', gap: '10px' }}>
            <button className="btn-white" disabled={params.offset === 0} onClick={() => setParams(p => ({...p, offset: Math.max(0, p.offset - limit)}))}>PREV</button>
            <span style={{ alignSelf: 'center' }}>СТРАНИЦА: {params.offset / limit + 1}</span>
            <button className="btn-white" disabled={!hasNextPage} onClick={() => setParams(p => ({...p, offset: p.offset + limit}))}>NEXT</button>
          </div>
        </div>
      )}
    </div>
  );
};