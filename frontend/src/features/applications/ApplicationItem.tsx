import { Application } from '../../types/application';

interface Props {
  app: Application;
}

export const ApplicationItem = ({ app }: Props) => {
  const priorityClass = app.priority === 'high' ? 'priority-high' : 
                        app.priority === 'low' ? 'priority-low' : '';
  
  const formatDate = (dateString: string) => new Date(dateString).toLocaleString();

  return (
    <div className={`app-item ${priorityClass}`}>
      <strong>{app.title.toUpperCase()}</strong>
      
      <div style={{ marginBottom: '10px' }}>
        <span className="app-tag">{app.priority.toUpperCase()}</span>
        <span className="app-tag">{app.status.toUpperCase()}</span>
      </div>
      
      <p style={{ margin: '0 0 10px 0', fontSize: '0.9em', opacity: 0.8 }}>
        {app.description}
      </p>

      <div style={{ fontSize: '0.7em', opacity: 0.8, marginTop: '10px' }}>
        <div>СОЗДАНО: {formatDate(app.created_at)}</div>
        <div>ОБНОВЛЕНО: {formatDate(app.updated_at)}</div>
      </div>
    </div>
  );
};