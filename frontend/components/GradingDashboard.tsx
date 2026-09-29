'use client';

import React, { useState } from 'react';
import { BatchGradingResult, OnionClassificationItem, generatePdfReport } from '@/lib/api';
import QualitySummary from '@/components/mobile/QualitySummary';
import FlaggedOnions from '@/components/mobile/FlaggedOnions';
import { Download, RefreshCw, FileText, Loader2 } from 'lucide-react';

interface GradingDashboardProps {
  uploadId: string;
  gradingResult: BatchGradingResult;
  classifications: OnionClassificationItem[];
  annotatedImageUrl: string;
  backendBaseUrl?: string;
  onReset?: () => void;
}

export default function GradingDashboard({
  uploadId,
  gradingResult,
  classifications,
  annotatedImageUrl,
  backendBaseUrl = 'http://localhost:8000',
  onReset,
}: GradingDashboardProps) {
  const [isGeneratingPdf, setIsGeneratingPdf] = useState(false);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL?.replace('/api', '') || backendBaseUrl;

  const handleDownloadPdf = async () => {
    setIsGeneratingPdf(true);
    try {
      if (pdfUrl) {
        window.open(`${API_BASE_URL}${pdfUrl}`, '_blank');
        return;
      }

      const res = await generatePdfReport(uploadId, gradingResult, classifications, annotatedImageUrl);
      setPdfUrl(res.pdf_report_url);
      window.open(`${API_BASE_URL}${res.pdf_report_url}`, '_blank');
    } catch (err) {
      console.error('PDF Generation Error:', err);
      alert('Failed to generate PDF report. Check backend API logs.');
    } finally {
      setIsGeneratingPdf(false);
    }
  };

  return (
    <div className="w-full space-y-5 animate-fadeIn">
      {/* Top Batch Info Card */}
      <div className="bg-[#1B1B20] border border-white/10 rounded-3xl p-5 shadow-2xl flex items-center justify-between">
        <div>
          <span className="text-[10px] font-bold font-mono px-2 py-0.5 rounded-full bg-[#7CFF6B]/15 text-[#7CFF6B] border border-[#7CFF6B]/30">
            {gradingResult.batch_id}
          </span>
          <h2 className="text-xl font-black text-white tracking-tight mt-1">
            Batch Quality Report
          </h2>
          <p className="text-[11px] text-[#A7A7B0]">{gradingResult.timestamp}</p>
        </div>

        {onReset && (
          <button
            onClick={onReset}
            className="px-3 py-2 bg-[#151518] hover:bg-white/10 text-white font-bold text-xs rounded-2xl border border-white/10 transition flex items-center space-x-1"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>New Batch</span>
          </button>
        )}
      </div>

      {/* Main Quality Assessment Summary Card */}
      <QualitySummary
        gradingResult={gradingResult}
        onExportPdf={handleDownloadPdf}
        isGeneratingPdf={isGeneratingPdf}
      />

      {/* Flagged Defective Onions Carousel */}
      <FlaggedOnions items={classifications} />
    </div>
  );
}
