import { useState, useEffect } from 'react';
import { ListParams } from '../../types/application';

export const ApplicationSearchForm = ({ onSearch, initialParams }: { 
  onSearch: (params: ListParams) => void,
  initialParams: ListParams 
}) => {
  const [form, setForm] = useState<ListParams>(initialParams);

  useEffect(() => {
    const timer = setTimeout(() => onSearch(form), 300); 
    return () => clearTimeout(timer);
  }, [form]);

  const handleStatusChange = (status: string) => {
    setForm(prev => {
      const statuses = prev.statuses || [];
      const newStatuses = statuses.includes(status) ? statuses.filter(s => s !== status) : [...statuses, status];
      return { ...prev, statuses: newStatuses };
    });
  };

  return (
    <div className="form-container" style={{ 
      display: 'flex', gap: '20px', alignItems: 'center', flexWrap: 'wrap', marginBottom: '20px'
    }}>
      <input 
        value={form.query || ''} 
        onChange={(e) => setForm(p => ({ ...p, query: e.target.value }))} 
        placeholder="ПОИСК..."
        style={{ flex: 1, minWidth: '200px' }}
      />
      
      <div style={{ display: 'flex', gap: '15px' }}>
        {['new', 'in_progress', 'done'].map(s => (
          <label key={s} style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
            <input 
              type="checkbox" 
              checked={form.statuses?.includes(s)} 
              onChange={() => handleStatusChange(s)} 
              style={{ width: '18px', height: '18px' }}
            /> 
            {s.toUpperCase()}
          </label>
        ))}
      </div>

      <select 
        value={form.sort_by_priority ? 'priority' : 'date'} 
        onChange={(e) => setForm(p => ({ ...p, sort_by_priority: e.target.value === 'priority' }))}
        style={{ background: 'transparent', color: 'white', padding: '8px', border: '2px solid white' }}
      >
        <option value="date" style={{ background: 'black' }}>ДАТА</option>
        <option value="priority" style={{ background: 'black' }}>ПРИОРИТЕТ</option>
      </select>

      <select 
        value={form.sort_desc ? 'desc' : 'asc'} 
        onChange={(e) => setForm(p => ({ ...p, sort_desc: e.target.value === 'desc' }))}
        style={{ background: 'transparent', color: 'white', padding: '8px', border: '2px solid white' }}
      >
        <option value="desc" style={{ background: 'black' }}>↓ УБЫВАНИЕ</option>
        <option value="asc" style={{ background: 'black' }}>↑ ВОЗРАСТАНИЕ</option>
      </select>
    </div>
  );
};