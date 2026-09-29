'use client';

import React from 'react';
import { History, CheckCircle2, AlertTriangle, FileText, ChevronRight } from 'lucide-react';

interface HistoryItem {
  id: string;
  timestamp: string;
  totalOnions: number;
  gradeAPercent: number;
  ursPercent: number;
  status: 'ACCEPTED' | 'REJECTED';
}

export default function HistoryView() {
  const historyData: HistoryItem[] = [
    {
      id: 'BATCH-99421',
      timestamp: 'Today · 10:42 AM',
      totalOnions: 18,
      gradeAPercent: 83.3,
      ursPercent: 16.7,
      status: 'ACCEPTED',
    },
    {
      id: 'BATCH-99420',
      timestamp: 'Today · 09:15 AM',
      totalOnions: 15,
      gradeAPercent: 65.0,
      ursPercent: 35.0,
      status: 'REJECTED',
    },
    {
      id: 'BATCH-99419',
      timestamp: 'Yesterday · 04:30 PM',
      totalOnions: 22,
      gradeAPercent: 91.2,
      ursPercent: 8.8,
      status: 'ACCEPTED',
    },
    {
      id: 'BATCH-99418',
      timestamp: 'Yesterday · 02:10 PM',
      totalOnions: 20,
      gradeAPercent: 88.5,
      ursPercent: 11.5,
      status: 'ACCEPTED',
    },
  ];

  return (
    <div className="space-y-4 animate-fadeIn">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-black text-white tracking-tight">Inspection History</h2>
          <p className="text-xs text-[#A7A7B0]">Past procurement batch quality reports</p>
        </div>
        <span className="text-xs px-2.5 py-1 rounded-full bg-[#151518] text-[#7CFF6B] border border-[#7CFF6B]/30 font-bold">
          {historyData.length} Batches Logged
        </span>
      </div>

      <div className="space-y-2.5">
        {historyData.map((item) => (
          <div
            key={item.id}
            className="bg-[#1B1B20] border border-white/10 hover:border-white/20 rounded-2xl p-4 flex items-center justify-between shadow-xl transition cursor-pointer"
          >
            <div className="space-y-1">
              <div className="flex items-center space-x-2">
                <span className="font-extrabold text-sm text-white">{item.id}</span>
                <span
                  className={`text-[10px] font-black px-2 py-0.5 rounded-full border ${
                    item.status === 'ACCEPTED'
                      ? 'bg-[#7CFF6B]/15 text-[#7CFF6B] border-[#7CFF6B]/30'
                      : 'bg-[#FF5C5C]/15 text-[#FF5C5C] border-[#FF5C5C]/30'
                  }`}
                >
                  {item.status}
                </span>
              </div>
              <p className="text-[11px] text-[#A7A7B0]">{item.timestamp} • {item.totalOnions} Onions Sampled</p>
            </div>

            <div className="flex items-center space-x-3">
              <div className="text-right">
                <p className="text-sm font-black text-[#7CFF6B]">{item.gradeAPercent}%</p>
                <p className="text-[10px] text-[#A7A7B0]">Grade A</p>
              </div>
              <ChevronRight className="w-5 h-5 text-[#A7A7B0]" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
