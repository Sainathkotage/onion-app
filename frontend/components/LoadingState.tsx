'use client';

import React from 'react';
import { Loader2, Cpu, Scan, CheckCircle2 } from 'lucide-react';

interface LoadingStateProps {
  message?: string;
  stage?: string;
}

export default function LoadingState({
  message = 'Uploading and processing onion batch image...',
  stage = 'Stage 1: Image Transfer',
}: LoadingStateProps) {
  return (
    <div className="w-full max-w-xl mx-auto bg-white rounded-2xl p-8 border border-slate-200 shadow-xl text-center">
      <div className="relative w-20 h-20 mx-auto mb-6 flex items-center justify-center">
        <div className="absolute inset-0 rounded-full border-4 border-emerald-100 border-t-emerald-600 animate-spin" />
        <div className="w-12 h-12 rounded-full bg-emerald-50 text-emerald-700 flex items-center justify-center">
          <Scan className="w-6 h-6 animate-pulse" />
        </div>
      </div>

      <h3 className="text-xl font-bold text-slate-800">{stage}</h3>
      <p className="text-sm text-slate-600 mt-2">{message}</p>

      <div className="mt-6 pt-4 border-t border-slate-100 flex justify-center items-center space-x-2 text-xs text-emerald-700 font-medium">
        <Cpu className="w-4 h-4 text-emerald-600" />
        <span>OnionIQ Computer Vision Engine Active</span>
      </div>
    </div>
  );
}
