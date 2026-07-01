export const ConfirmModal = ({ 
  isOpen, 
  onClose, 
  onConfirm, 
  message = "ВЫ УВЕРЕНЫ?", 
  confirmText = "УДАЛИТЬ" 
}: { 
  isOpen: boolean; 
  onClose: () => void; 
  onConfirm: () => void; 
  message?: string;
  confirmText?: string;
}) => {
  if (!isOpen) return null;

  return (
    <div style={{ 
      position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.85)', 
      display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 6000 
    }}>
      <div className="form-container" style={{ width: '350px', textAlign: 'center' }}>
        <h3 style={{ marginTop: 0, textTransform: 'uppercase' }}>ПОДТВЕРЖДЕНИЕ</h3>
        <p style={{ margin: '20px 0', fontSize: '16px', textTransform: 'uppercase' }}>
          {message}
        </p>
        <div style={{ display: 'flex', gap: '10px', justifyContent: 'center' }}>
          <button 
            className="btn-red"
            onClick={() => { onConfirm(); onClose(); }} 
          >
            {confirmText}
          </button>
          <button 
            className="btn-white"
            onClick={onClose} 
          >
            ОТМЕНА
          </button>
        </div>
      </div>
    </div>
  );
};