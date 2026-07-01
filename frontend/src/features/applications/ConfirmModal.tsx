export const ConfirmModal = ({ 
  isOpen, onClose, onConfirm, message 
}: { 
  isOpen: boolean; onClose: () => void; onConfirm: () => void; message: string; 
}) => {
  if (!isOpen) return null;

  return (
    <div style={{ 
      position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.85)', 
      display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 4000 
    }}>
      <div className="form-container" style={{ width: '350px' }}>
        <p style={{ margin: '0 0 20px 0', textTransform: 'uppercase', textAlign: 'center' }}>
          {message}
        </p>
        <div style={{ display: 'flex', gap: '10px', justifyContent: 'center' }}>
          <button className="btn-red" onClick={onConfirm}>ДА, УДАЛИТЬ</button>
          <button className="btn-white" onClick={onClose}>ОТМЕНА</button>
        </div>
      </div>
    </div>
  );
};