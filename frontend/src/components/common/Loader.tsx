import { useUIStore } from '../../stores';
import { clsx } from 'clsx';

export const Loader = () => {
  const { isLoading, loadingMessage } = useUIStore();

  if (!isLoading) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 shadow-xl max-w-sm w-full mx-4">
        <div className="flex flex-col items-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600" />
          {loadingMessage && (
            <p className="mt-4 text-gray-700 text-center font-medium">{loadingMessage}</p>
          )}
        </div>
      </div>
    </div>
  );
};

interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const Spinner = ({ size = 'md', className }: SpinnerProps) => {
  const sizes = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
  };

  return (
    <div
      className={clsx(
        'animate-spin rounded-full border-b-2 border-primary-600',
        sizes[size],
        className
      )}
    />
  );
};
