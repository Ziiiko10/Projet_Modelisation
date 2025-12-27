import { useUIStore } from '../../stores';
import { X, AlertCircle, CheckCircle, Info, AlertTriangle } from 'lucide-react';
import { clsx } from 'clsx';

export const AlertContainer = () => {
  const { alerts, removeAlert } = useUIStore();

  if (alerts.length === 0) return null;

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2 w-80">
      {alerts.map((alert) => (
        <Alert
          key={alert.id}
          type={alert.type}
          message={alert.message}
          onClose={() => removeAlert(alert.id)}
        />
      ))}
    </div>
  );
};

interface AlertProps {
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  onClose: () => void;
}

const Alert = ({ type, message, onClose }: AlertProps) => {
  const icons = {
    success: CheckCircle,
    error: AlertCircle,
    warning: AlertTriangle,
    info: Info,
  };

  const styles = {
    success: 'bg-green-50 border-green-200 text-green-800',
    error: 'bg-red-50 border-red-200 text-red-800',
    warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
    info: 'bg-blue-50 border-blue-200 text-blue-800',
  };

  const iconStyles = {
    success: 'text-green-500',
    error: 'text-red-500',
    warning: 'text-yellow-500',
    info: 'text-blue-500',
  };

  const Icon = icons[type];

  return (
    <div
      className={clsx(
        'flex items-start p-4 rounded-lg border shadow-lg animate-in slide-in-from-right',
        styles[type]
      )}
    >
      <Icon className={clsx('w-5 h-5 mt-0.5 mr-3 flex-shrink-0', iconStyles[type])} />
      <div className="flex-1">
        <p className="text-sm font-medium">{message}</p>
      </div>
      <button
        onClick={onClose}
        className="ml-3 flex-shrink-0 hover:opacity-70 transition-opacity"
      >
        <X className="w-4 h-4" />
      </button>
    </div>
  );
};
