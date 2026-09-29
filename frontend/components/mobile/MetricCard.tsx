'use client';

import React from 'react';
import { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  label: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  variant?: 'default' | 'accent' | 'warning' | 'danger';
}

export default function MetricCard({
  label,
  value,
  subtitle,
  icon: Icon,
  variant = 'default',
}: MetricCardProps) {
  const getVariantStyles = () => {
    switch (variant) {
      case 'accent':
        return {
          iconBg: 'bg-[#7CFF6B]/15 border-[#7CFF6B]/30 text-[#7CFF6B]',
          valueColor: 'text-[#7CFF6B]',
        };
      case 'warning':
        return {
          iconBg: 'bg-[#FFB547]/15 border-[#FFB547]/30 text-[#FFB547]',
          valueColor: 'text-[#FFB547]',
        };
      case 'danger':
        return {
          iconBg: 'bg-[#FF5C5C]/15 border-[#FF5C5C]/30 text-[#FF5C5C]',
          valueColor: 'text-[#FF5C5C]',
        };
      default:
        return {
          iconBg: 'bg-white/10 border-white/10 text-white',
          valueColor: 'text-white',
        };
    }
  };

  const styles = getVariantStyles();

  return (
    <div className="bg-[#1B1B20] border border-white/10 rounded-2xl p-4 flex flex-col justify-between shadow-xl relative overflow-hidden group hover:border-white/20 transition">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs text-[#A7A7B0] font-medium tracking-tight">{label}</span>
        <div className={`w-8 h-8 rounded-xl border flex items-center justify-center ${styles.iconBg}`}>
          <Icon className="w-4 h-4" />
        </div>
      </div>
      <div>
        <h3 className={`text-2xl font-black tracking-tight ${styles.valueColor}`}>{value}</h3>
        {subtitle && <p className="text-[11px] text-[#A7A7B0] mt-0.5 tracking-tight">{subtitle}</p>}
      </div>
    </div>
  );
}
