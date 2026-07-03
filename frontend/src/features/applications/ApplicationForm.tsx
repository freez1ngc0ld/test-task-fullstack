import { useState } from 'react';
import { Application } from '../../types/application';

interface Props {
  initialData?: Application;
  onSubmit: (data: any) => void;
  onCancel: () => void;
  error?: string | null; 
}

export const ApplicationForm = ({ initialData, onSubmit, onCancel, error }: Props) => {
  const [form, setForm] = useState(initialData || {
    title: '',
    description: '',
    status: 'new',
    priority: 'normal'
  });

  const [localError, setLocalError] = useState<string | null>(null);

  const handleSubmit = () => {
    if (form.title.length < 3 || form.title.length > 120) {
      setLocalError("ДЛИНА ЗАГОЛОВКА ДОЛЖНА БЫТЬ ОТ 3 ДО 120 СИМВОЛОВ");
      return;
    }
    setLocalError(null);
    onSubmit(form);
  };

  return (
    <div style={{
      position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.85)', 
      display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000
    }}>
      <div className="form-container" style={{ width: '400px' }}>
        <h2 style={{ marginTop: 0, textTransform: 'uppercase' }}>
          {initialData ? 'РЕДАКТИРОВАНИЕ' : 'НОВАЯ ЗАЯВКА'}
        </h2>

        {(error || localError) && (
          <p style={{ color: 'var(--accent-red)', marginBottom: '15px', fontWeight: 'bold' }}>
            {error || localError}
          </p>
        )}

        <div className="form-group">
          <input 
            placeholder="ЗАГОЛОВОК" 
            value={form.title} 
            onChange={e => {
              setForm({...form, title: e.target.value});
              if (localError) setLocalError(null); 
            }} 
          />
          <textarea 
            placeholder="ОПИСАНИЕ" 
            value={form.description || ''} 
            onChange={e => setForm({...form, description: e.target.value})} 
            style={{ 
              background: 'transparent', border: '2px solid white', color: 'white', 
              padding: '10px', height: '100px', resize: 'none', fontFamily: 'inherit', width: '100%' 
            }}
          />

          {!initialData && (
            <select 
              value={form.status} 
              onChange={e => setForm({...form, status: e.target.value as any})}
              style={{ background: 'black', color: 'white', padding: '10px', border: '2px solid white', width: '100%' }}
            >
              <option value="new">NEW</option>
              <option value="in_progress">IN PROGRESS</option>
              <option value="done">DONE</option>
            </select>
          )}

          <select 
            value={form.priority} 
            onChange={e => setForm({...form, priority: e.target.value as any})}
            style={{ background: 'black', color: 'white', padding: '10px', border: '2px solid white', width: '100%' }}
          >
            <option value="low">LOW</option>
            <option value="normal">NORMAL</option>
            <option value="high">HIGH</option>
          </select>
        </div>

        <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
          <button className="btn-green" onClick={handleSubmit} style={{ flex: 1 }}>СОХРАНИТЬ</button>
          <button className="btn-white" onClick={onCancel} style={{ flex: 1 }}>ОТМЕНА</button>
        </div>
      </div>
    </div>
  );
};