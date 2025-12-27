import { ReactNode } from 'react';
import { clsx } from 'clsx';

interface CardProps {
  children: ReactNode;
  title?: string;
  subtitle?: string;
  action?: ReactNode;
  className?: string;
  padding?: 'none' | 'sm' | 'md' | 'lg';
}

export const Card = ({
  children,
  title,
  subtitle,
  action,
  className,
  padding = 'md',
}: CardProps) => {
  const paddings = {
    none: '',
    sm: 'p-3',
    md: 'p-4',
    lg: 'p-6',
  };

  return (
    <div className={clsx('bg-white rounded-lg shadow-sm border border-gray-200', className)}>
      {(title || subtitle || action) && (
        <div className={clsx('border-b border-gray-200', paddings[padding])}>
          <div className="flex items-center justify-between">
            <div>
              {title && <h3 className="text-lg font-semibold text-gray-900">{title}</h3>}
              {subtitle && <p className="mt-1 text-sm text-gray-500">{subtitle}</p>}
            </div>
            {action && <div>{action}</div>}
          </div>
        </div>
      )}
      <div className={clsx(title || subtitle || action ? '' : paddings[padding])}>
        {children}
      </div>
    </div>
  );
};
