'use client';

import React from 'react';
import { FileText, Download, CheckCircle2, ArrowRight } from 'lucide-react';
import Link from 'next/link';

export default function ReportsPage() {
  return (
    <div className="space-y-4 animate-fadeIn">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-black text-white tracking-tight">Quality Reports</h2>
          <p className="text-xs text-[#A7A7B0]">Exported digital PDF procurement certificates</p>
        </div>
      </div>

      <div className="bg-[#1B1B20] border border-white/10 rounded-3xl p-5 shadow-2xl space-y-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-2xl bg-[#7CFF6B]/15 text-[#7CFF6B] border border-[#7CFF6B]/30 flex items-center justify-center font-bold">
            <FileText className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white">Latest PDF Certificate</h3>
            <p className="text-xs text-[#A7A7B0]">BATCH-99421 • Today, 10:42 AM</p>
          </div>
        </div>

        <div className="bg-[#151518] p-3.5 rounded-2xl border border-white/5 space-y-1 text-xs text-[#A7A7B0]">
          <div className="flex justify-between">
            <span>Grade A Rate:</span>
            <span className="font-bold text-[#7CFF6B]">83.3%</span>
          </div>
          <div className="flex justify-between">
            <span>URS Ratio:</span>
            <span className="font-bold text-[#FF5C5C]">16.7%</span>
          </div>
          <div className="flex justify-between">
            <span>Official Decision:</span>
            <span className="font-bold text-white">ACCEPTED (GRADE A)</span>
          </div>
        </div>

        <Link
          href="/analyze"
          className="w-full py-3 bg-[#7CFF6B] hover:bg-[#6be65b] text-[#0B0B0D] font-extrabold rounded-2xl shadow-lg glow-accent transition flex items-center justify-center space-x-2 text-xs"
        >
          <Download className="w-4 h-4 text-[#0B0B0D]" />
          <span>Generate / Download PDF</span>
        </Link>
      </div>
    </div>
  );
}
