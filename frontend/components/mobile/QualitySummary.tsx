'use client';

import React from 'react';
import { BatchGradingResult } from '@/lib/api';
import { Award, AlertTriangle, CheckCircle2, FileText, Sparkles } from 'lucide-react';

interface QualitySummaryProps {
  gradingResult: BatchGradingResult;
  onExportPdf?: () => void;
  isGeneratingPdf?: boolean;
}

export default function QualitySummary({
  gradingResult,
  onExportPdf,
  isGeneratingPdf = false,
}: QualitySummaryProps) {
  const isApproved = gradingResult.grade_a.percentage >= 80.0;
  const gradeAPercent = gradingResult.grade_a.percentage.toFixed(1);
  const ursPercent = gradingResult.urs.percentage.toFixed(1);

  const breakdown = gradingResult.breakdown;

  return (
    <div className="bg-[#1B1B20] border border-white/10 rounded-3xl p-5 space-y-5 shadow-2xl">
      {/* Header & Status Badge */}
      <div className="flex items-center justify-between">
        <div>
          <span className="text-[11px] font-bold uppercase tracking-wider text-[#A7A7B0]">
            Batch Quality Decision
          </span>
          <h3 className="text-lg font-black text-white tracking-tight mt-0.5">
            Quality Assessment
          </h3>
        </div>

        <div
          className={`px-3 py-1 rounded-full border text-xs font-extrabold flex items-center space-x-1.5 ${
            isApproved
              ? 'bg-[#7CFF6B]/15 text-[#7CFF6B] border-[#7CFF6B]/30'
              : 'bg-[#FF5C5C]/15 text-[#FF5C5C] border-[#FF5C5C]/30'
          }`}
        >
          {isApproved ? (
            <>
              <CheckCircle2 className="w-3.5 h-3.5 text-[#7CFF6B]" />
              <span>GRADE A ACCEPTED</span>
            </>
          ) : (
            <>
              <AlertTriangle className="w-3.5 h-3.5 text-[#FF5C5C]" />
              <span>HIGH URS REJECTED</span>
            </>
          )}
        </div>
      </div>

      {/* Metric Cards (Grade A vs URS) */}
      <div className="grid grid-cols-2 gap-3">
        <div className="bg-[#151518] p-3.5 rounded-2xl border border-white/5 space-y-1">
          <span className="text-[11px] text-[#A7A7B0] font-medium">Grade A (Procurement)</span>
          <div className="flex items-baseline space-x-1">
            <span className="text-2xl font-black text-[#7CFF6B]">{gradeAPercent}%</span>
            <span className="text-[10px] text-[#A7A7B0]">({gradingResult.grade_a.count})</span>
          </div>
        </div>

        <div className="bg-[#151518] p-3.5 rounded-2xl border border-white/5 space-y-1">
          <span className="text-[11px] text-[#A7A7B0] font-medium">URS (Rejected Supply)</span>
          <div className="flex items-baseline space-x-1">
            <span className="text-2xl font-black text-[#FF5C5C]">{ursPercent}%</span>
            <span className="text-[10px] text-[#A7A7B0]">({gradingResult.urs.count})</span>
          </div>
        </div>
      </div>

      {/* Progress Distribution Bar */}
      <div className="space-y-1.5">
        <div className="flex justify-between text-[11px] font-semibold text-[#A7A7B0]">
          <span>Defect Distribution</span>
          <span>Total: {gradingResult.total_onions} Onions</span>
        </div>
        <div className="h-3 w-full bg-[#151518] rounded-full overflow-hidden flex p-0.5 border border-white/5">
          {breakdown.healthy.percentage > 0 && (
            <div
              className="bg-[#7CFF6B] h-full rounded-l-full transition-all"
              style={{ width: `${breakdown.healthy.percentage}%` }}
              title={`Healthy: ${breakdown.healthy.count} (${breakdown.healthy.percentage.toFixed(1)}%)`}
            />
          )}
          {breakdown.damaged.percentage > 0 && (
            <div
              className="bg-[#FFB547] h-full transition-all"
              style={{ width: `${breakdown.damaged.percentage}%` }}
              title={`Damaged: ${breakdown.damaged.count} (${breakdown.damaged.percentage.toFixed(1)}%)`}
            />
          )}
          {breakdown.rotten.percentage > 0 && (
            <div
              className="bg-[#FF5C5C] h-full transition-all"
              style={{ width: `${breakdown.rotten.percentage}%` }}
              title={`Rotten: ${breakdown.rotten.count} (${breakdown.rotten.percentage.toFixed(1)}%)`}
            />
          )}
          {breakdown.sprouted.percentage > 0 && (
            <div
              className="bg-purple-500 h-full transition-all"
              style={{ width: `${breakdown.sprouted.percentage}%` }}
              title={`Sprouted: ${breakdown.sprouted.count} (${breakdown.sprouted.percentage.toFixed(1)}%)`}
            />
          )}
          {breakdown.undersized.percentage > 0 && (
            <div
              className="bg-sky-400 h-full rounded-r-full transition-all"
              style={{ width: `${breakdown.undersized.percentage}%` }}
              title={`Undersized: ${breakdown.undersized.count} (${breakdown.undersized.percentage.toFixed(1)}%)`}
            />
          )}
        </div>
      </div>

      {/* Breakdown Details List */}
      <div className="grid grid-cols-2 gap-2 text-xs">
        <div className="flex items-center space-x-2">
          <span className="w-2.5 h-2.5 rounded-full bg-[#7CFF6B]" />
          <span className="text-[#A7A7B0]">Healthy:</span>
          <span className="font-bold text-white">{breakdown.healthy.count}</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-2.5 h-2.5 rounded-full bg-[#FFB547]" />
          <span className="text-[#A7A7B0]">Damaged:</span>
          <span className="font-bold text-white">{breakdown.damaged.count}</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-2.5 h-2.5 rounded-full bg-[#FF5C5C]" />
          <span className="text-[#A7A7B0]">Rotten:</span>
          <span className="font-bold text-white">{breakdown.rotten.count}</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-2.5 h-2.5 rounded-full bg-purple-500" />
          <span className="text-[#A7A7B0]">Sprouted:</span>
          <span className="font-bold text-white">{breakdown.sprouted.count}</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-2.5 h-2.5 rounded-full bg-sky-400" />
          <span className="text-[#A7A7B0]">Undersized:</span>
          <span className="font-bold text-white">{breakdown.undersized.count}</span>
        </div>
      </div>

      {/* Recommendation text */}
      <p className="text-xs text-[#A7A7B0] bg-[#151518] p-3 rounded-xl border border-white/5 leading-relaxed">
        <strong className="text-white font-bold">Officer Action: </strong>
        {gradingResult.recommendation}
      </p>

      {/* Gemini AI Quality Assessment */}
      {gradingResult.quality_summary && (
        <div className="bg-[#151518] p-4 rounded-2xl border border-amber-500/20 text-xs text-slate-300 leading-relaxed space-y-2">
          <div className="flex items-center space-x-1.5 text-amber-400 font-bold">
            <Sparkles className="w-4 h-4 text-amber-400" />
            <span className="text-[11px] uppercase tracking-wider font-extrabold">
              {gradingResult.ai_engine || 'Google Gemini Vision'} Quality Diagnosis
            </span>
          </div>
          <p className="text-slate-300 text-xs leading-relaxed">{gradingResult.quality_summary}</p>
        </div>
      )}

      {/* PDF Export Action */}
      {onExportPdf && (
        <button
          onClick={onExportPdf}
          disabled={isGeneratingPdf}
          className="w-full py-3 bg-[#7CFF6B] hover:bg-[#6be65b] text-[#0B0B0D] font-extrabold rounded-2xl shadow-lg glow-accent transition flex items-center justify-center space-x-2 text-sm disabled:opacity-50"
        >
          <FileText className="w-4 h-4" />
          <span>{isGeneratingPdf ? 'Generating PDF...' : 'Download Digital PDF Report'}</span>
        </button>
      )}
    </div>
  );
}
