'use client';

import React from 'react';
import { BatchClassificationResult } from '@/lib/api';
import OnionResultCard from '@/components/mobile/OnionResultCard';
import { Grid, Cpu, Info } from 'lucide-react';

interface ClassificationGridProps {
  classificationResult: BatchClassificationResult;
}

export default function ClassificationGrid({ classificationResult }: ClassificationGridProps) {
  return (
    <div className="w-full space-y-4 animate-fadeIn">
      {/* Classification Header */}
      <div className="bg-[#1B1B20] border border-white/10 rounded-3xl p-5 shadow-2xl space-y-2">
        <div className="flex items-center justify-between">
          <div>
            <span className="text-[11px] font-bold uppercase tracking-wider text-[#A7A7B0]">
              Classification Grid
            </span>
            <h2 className="text-2xl font-black text-white tracking-tight mt-0.5">
              Defect Category Analysis
            </h2>
          </div>
          <span className="text-xs px-2.5 py-1 rounded-full bg-[#7CFF6B]/15 text-[#7CFF6B] font-bold border border-[#7CFF6B]/30">
            {classificationResult.total_onions} Items
          </span>
        </div>

        <div className="flex flex-wrap items-center gap-2 text-xs text-[#A7A7B0]">
          <div className="flex items-center space-x-1.5">
            <Cpu className="w-3.5 h-3.5 text-[#7CFF6B]" />
            <span>Model: {classificationResult.classifier_used}</span>
          </div>
          {classificationResult.calibration?.is_calibrated ? (
            <span className="text-[10px] px-2 py-0.5 rounded-full bg-[#7CFF6B]/15 text-[#7CFF6B] border border-[#7CFF6B]/30 font-bold">
              ✓ Metric Calibrated ({classificationResult.calibration.pixels_per_mm?.toFixed(1)} px/mm)
            </span>
          ) : (
            <span className="text-[10px] px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-300 border border-amber-500/30 font-medium">
              ⚠ Uncalibrated (Relative Size)
            </span>
          )}
        </div>
      </div>

      {/* Grid of Onion Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
        {classificationResult.classifications.map((item) => (
          <OnionResultCard key={item.onion_id} item={item} />
        ))}
      </div>
    </div>
  );
}
