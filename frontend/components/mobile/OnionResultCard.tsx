'use client';

import React from 'react';
import { OnionClassificationItem } from '@/lib/api';

interface OnionResultCardProps {
  item: OnionClassificationItem;
}

export default function OnionResultCard({ item }: OnionResultCardProps) {
  const getBadgeStyle = (label: string) => {
    switch (label) {
      case 'Healthy':
        return 'bg-[#7CFF6B]/15 text-[#7CFF6B] border-[#7CFF6B]/30';
      case 'Damaged':
        return 'bg-[#FFB547]/15 text-[#FFB547] border-[#FFB547]/30';
      case 'Rotten':
        return 'bg-[#FF5C5C]/15 text-[#FF5C5C] border-[#FF5C5C]/30';
      case 'Sprouted':
        return 'bg-purple-500/15 text-purple-300 border-purple-500/30';
      case 'Undersized':
        return 'bg-sky-500/15 text-sky-300 border-sky-500/30';
      default:
        return 'bg-slate-500/15 text-slate-300 border-slate-500/30';
    }
  };

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL?.replace('/api', '') || 'http://localhost:8000';
  const cropUrl = item.crop_path.startsWith('http')
    ? item.crop_path
    : `${API_BASE_URL}/${item.crop_path.replace(/^\//, '')}`;

  const confidencePercent = Math.round(item.confidence * 100);

  return (
    <div className="bg-[#1B1B20] border border-white/10 rounded-2xl p-3 flex flex-col justify-between space-y-2 shadow-xl hover:border-white/20 transition">
      {/* Onion Image Crop */}
      <div className="relative aspect-square w-full rounded-xl bg-[#0B0B0D] overflow-hidden border border-white/5 flex items-center justify-center">
        {item.crop_path ? (
          <img
            src={cropUrl}
            alt={`Onion #${item.onion_id}`}
            className="w-full h-full object-cover"
            onError={(e) => {
              // Fallback placeholder graphic if crop path fails
              (e.target as HTMLElement).style.display = 'none';
            }}
          />
        ) : (
          <span className="text-3xl">🧅</span>
        )}
        <span className="absolute bottom-1.5 left-1.5 text-[10px] font-bold bg-[#0B0B0D]/80 backdrop-blur-md px-1.5 py-0.5 rounded text-white border border-white/10">
          #{item.onion_id < 10 ? `0${item.onion_id}` : item.onion_id}
        </span>
      </div>

      {/* Label & Confidence */}
      <div className="space-y-1.5">
        <div className="flex items-center justify-between">
          <span className={`text-[10px] font-extrabold px-2 py-0.5 rounded-full border ${getBadgeStyle(item.class_label)}`}>
            {item.class_label}
          </span>
          <span className="text-[11px] font-bold text-white">{confidencePercent}%</span>
        </div>

        {/* Physical Size / Diameter Information */}
        <div className="pt-1 border-t border-white/5">
          {item.size?.measurement_status === 'calibrated' && item.size?.physical_diameter_mm != null ? (
            <div className="flex items-center justify-between text-[11px]">
              <span className="font-extrabold text-white flex items-center space-x-1">
                <span className="text-[#7CFF6B]">Ø</span>
                <span>{item.size.physical_diameter_mm} mm</span>
              </span>
              <span className="text-[10px] px-1.5 py-0.5 rounded-md bg-[#7CFF6B]/15 text-[#7CFF6B] font-bold border border-[#7CFF6B]/30">
                {item.size.size_category}
              </span>
            </div>
          ) : (
            <div className="flex items-center justify-between text-[10px] text-[#A7A7B0]">
              <span className="text-amber-400/80 font-medium">Physical: N/A</span>
              <span className="text-[9px] px-1.5 py-0.5 rounded bg-white/5 text-[#A7A7B0] border border-white/5 font-medium">
                {item.size?.size_category || 'Relative'}
              </span>
            </div>
          )}
        </div>

        {item.defect_reason && (
          <p className="text-[10px] text-[#A7A7B0] truncate leading-tight">{item.defect_reason}</p>
        )}
      </div>
    </div>
  );
}
