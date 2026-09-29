'use client';

import React, { useState, useEffect } from 'react';
import { RefreshCw, Sparkles, FileText, ArrowRight, AlertTriangle } from 'lucide-react';

interface ImagePreviewProps {
  file: File;
  onReset: () => void;
  onAnalyze: () => void;
  isAnalyzing?: boolean;
}

export default function ImagePreview({ file, onReset, onAnalyze, isAnalyzing = false }: ImagePreviewProps) {
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [dimensions, setDimensions] = useState<{ width: number; height: number } | null>(null);
  const [isCorrupted, setIsCorrupted] = useState<boolean>(false);

  useEffect(() => {
    setIsCorrupted(false);
    setDimensions(null);

    const url = URL.createObjectURL(file);
    setPreviewUrl(url);

    const img = new Image();
    img.onload = () => {
      setDimensions({ width: img.width, height: img.height });
      setIsCorrupted(false);
    };
    img.onerror = () => {
      setIsCorrupted(true);
    };
    img.src = url;

    return () => {
      URL.revokeObjectURL(url);
    };
  }, [file]);

  const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);

  return (
    <div className="w-full bg-[#1B1B20] border border-white/10 rounded-3xl overflow-hidden shadow-2xl space-y-0">
      {/* Header Bar */}
      <div className="bg-[#151518] px-5 py-3.5 border-b border-white/5 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <FileText className="w-4 h-4 text-[#7CFF6B]" />
          <span className="text-xs font-bold text-white truncate max-w-xs">{file.name}</span>
          <span className="text-[10px] px-2 py-0.5 bg-[#0B0B0D] text-[#A7A7B0] rounded-md font-mono border border-white/5">
            {fileSizeMB} MB
          </span>
        </div>
        <button
          onClick={onReset}
          disabled={isAnalyzing}
          className="text-xs font-bold text-[#A7A7B0] hover:text-white flex items-center space-x-1 transition disabled:opacity-50"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Retake</span>
        </button>
      </div>

      {/* Main Image Frame */}
      <div className="relative bg-[#0B0B0D] p-3 flex items-center justify-center min-h-[260px] max-h-[420px]">
        {isCorrupted ? (
          <div className="p-6 text-center space-y-2 text-rose-400">
            <AlertTriangle className="w-8 h-8 mx-auto" />
            <p className="text-sm font-bold text-white">Corrupted Image File</p>
            <p className="text-xs text-rose-300 max-w-sm">
              The browser could not decode this file. It may be damaged, truncated, or not a valid image.
            </p>
          </div>
        ) : previewUrl ? (
          <img
            src={previewUrl}
            alt="Batch Preview"
            className="max-h-[380px] w-auto max-w-full object-contain rounded-2xl shadow-xl border border-white/5"
          />
        ) : (
          <div className="text-[#A7A7B0] text-xs">Loading image preview...</div>
        )}

        {dimensions && !isCorrupted && (
          <div className="absolute bottom-4 right-4 bg-[#0B0B0D]/80 backdrop-blur-md text-white px-2.5 py-0.5 rounded-full text-[10px] font-mono border border-white/10">
            {dimensions.width} × {dimensions.height} px
          </div>
        )}
      </div>

      {/* Action Footer */}
      <div className="p-5 bg-[#151518] border-t border-white/5 space-y-3">
        <div className="flex items-center justify-between text-xs text-[#A7A7B0]">
          <span className="font-semibold text-white">
            {isCorrupted ? 'Image Error' : 'Batch Preview Ready'}
          </span>
          <span>
            {isCorrupted ? 'Please retake or upload another image' : 'Click Analyze to run AI pipeline'}
          </span>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={onReset}
            disabled={isAnalyzing}
            className="px-4 py-3 bg-[#1B1B20] hover:bg-white/10 text-white font-bold rounded-2xl border border-white/10 transition text-xs"
          >
            Retake
          </button>

          <button
            onClick={onAnalyze}
            disabled={isAnalyzing || isCorrupted}
            className="flex-1 py-3 bg-[#7CFF6B] hover:bg-[#6be65b] text-[#0B0B0D] font-extrabold rounded-2xl shadow-xl glow-accent transition flex items-center justify-center space-x-2 text-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Sparkles className="w-4 h-4 text-[#0B0B0D] animate-pulse" />
            <span>{isAnalyzing ? 'Analyzing Batch...' : 'Analyze Batch'}</span>
            <ArrowRight className="w-4 h-4 text-[#0B0B0D]" />
          </button>
        </div>
      </div>
    </div>
  );
}
