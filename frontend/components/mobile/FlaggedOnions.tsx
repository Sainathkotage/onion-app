'use client';

import React from 'react';
import { OnionClassificationItem } from '@/lib/api';
import { AlertCircle, AlertTriangle } from 'lucide-react';

interface FlaggedOnionsProps {
  items: OnionClassificationItem[];
}

export default function FlaggedOnions({ items }: FlaggedOnionsProps) {
  const defectiveItems = items.filter((item) => item.is_defective || item.class_label !== 'Healthy');

  if (defectiveItems.length === 0) {
    return (
      <div className="bg-[#1B1B20] border border-white/10 rounded-2xl p-4 text-center space-y-1">
        <span className="text-xl">🎉</span>
        <h4 className="text-xs font-bold text-white">No Flagged Defects</h4>
        <p className="text-[11px] text-[#A7A7B0]">All onions in this batch meet Grade A procurement quality standards.</p>
      </div>
    );
  }

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL?.replace('/api', '') || 'http://localhost:8000';

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div>
          <h4 className="text-sm font-black text-white tracking-tight flex items-center space-x-1.5">
            <AlertTriangle className="w-4 h-4 text-[#FFB547]" />
            <span>Needs Attention ({defectiveItems.length})</span>
          </h4>
          <p className="text-[11px] text-[#A7A7B0]">Defective onions requiring quality inspector review</p>
        </div>
      </div>

      {/* Horizontal Scrollable Container */}
      <div className="flex space-x-3 overflow-x-auto pb-2 scrollbar-none snap-x">
        {defectiveItems.map((item) => {
          const cropUrl = item.crop_path.startsWith('http')
            ? item.crop_path
            : `${API_BASE_URL}/${item.crop_path.replace(/^\//, '')}`;

          return (
            <div
              key={item.onion_id}
              className="flex-shrink-0 w-44 bg-[#1B1B20] border border-white/10 rounded-2xl p-3 space-y-2 snap-start shadow-xl hover:border-white/20 transition"
            >
              <div className="relative aspect-square w-full rounded-xl bg-[#0B0B0D] overflow-hidden border border-white/5 flex items-center justify-center">
                {item.crop_path ? (
                  <img
                    src={cropUrl}
                    alt={`Defective Onion #${item.onion_id}`}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      (e.target as HTMLElement).style.display = 'none';
                    }}
                  />
                ) : (
                  <span className="text-2xl">🧅</span>
                )}
                <span className="absolute top-1.5 right-1.5 px-2 py-0.5 rounded-full text-[9px] font-black uppercase tracking-wider bg-[#FF5C5C]/20 text-[#FF5C5C] border border-[#FF5C5C]/40">
                  {item.class_label}
                </span>
              </div>

              <div>
                <div className="flex items-center justify-between text-xs">
                  <span className="font-extrabold text-white">Onion #{item.onion_id}</span>
                  <span className="font-bold text-[#FFB547]">{Math.round(item.confidence * 100)}%</span>
                </div>
                {item.defect_reason && (
                  <p className="text-[10px] text-[#A7A7B0] truncate mt-0.5">{item.defect_reason}</p>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
