import React from 'react';
import { clsx } from 'clsx';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'hover' | 'quest' | 'guild';
  children: React.ReactNode;
}

export function Card({ variant = 'default', className, children, ...props }: CardProps) {
  const baseClasses = 'bg-white rounded-xl shadow-sm border border-gray-200 p-6';
  
  const variantClasses = {
    default: '',
    hover: 'hover:shadow-md transition-shadow duration-200',
    quest: 'hover:shadow-lg transform hover:-translate-y-1 transition-all duration-200 cursor-pointer',
    guild: 'hover:border-primary-200 hover:shadow-md transition-all duration-200',
  };

  return (
    <div
      className={clsx(baseClasses, variantClasses[variant], className)}
      {...props}
    >
      {children}
    </div>
  );
}