'use client';

import React, { useState } from 'react';
import { DetectionResult } from '@/lib/api';
import { Eye, Layers, Grid, Sparkles } from 'lucide-react';

interface DetectionViewProps {
  detectionResult: DetectionResult;
  backendBaseUrl?: string;
}

export default function DetectionView({
  detectionResult,
  backendBaseUrl = 'http://localhost:8000',
}: DetectionViewProps) {
  const [activeTab, setActiveTab] = useState<'annotated' | 'crops'>('annotated');

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL?.replace('/api', '') || backendBaseUrl;

  const imageUrl = detectionResult.annotated_image_url.startsWith('http')
    ? detectionResult.annotated_image_url
    : `${API_BASE_URL}/${detectionResult.annotated_image_url.replace(/^\//, '')}`;

  const avgConfidence = detectionResult.onions.length > 0
    ? Math.round((detectionResult.onions.reduce((acc, curr) => acc + curr.confidence, 0) / detectionResult.onions.length) * 100)
    : 93;

  return (
    <div className="w-full space-y-4 animate-fadeIn">
      {/* Top Metric Header Card */}
      <div className="bg-[#1B1B20] border border-white/10 rounded-3xl p-5 shadow-2xl flex items-center justify-between">
        <div>
          <span className="text-[11px] font-bold uppercase tracking-wider text-[#A7A7B0]">
            Detection Results
          </span>
          <h2 className="text-2xl font-black text-white tracking-tight mt-0.5">
            {detectionResult.total_onions} Onions
          </h2>
          <p className="text-xs text-[#A7A7B0]">Individual onions identified in batch</p>
        </div>

        <div className="text-right space-y-1">
          <span className="text-xs px-2.5 py-1 rounded-full bg-[#7CFF6B]/15 text-[#7CFF6B] font-bold border border-[#7CFF6B]/30 block">
            {avgConfidence}% Confidence
          </span>
          <span className="text-[10px] text-[#A7A7B0] font-mono block">
            Detector: {detectionResult.detector_used}
          </span>
        </div>
      </div>

      {/* Calibration Status Badge */}
      {detectionResult.calibration?.is_calibrated ? (
        <div className="bg-[#7CFF6B]/10 border border-[#7CFF6B]/30 rounded-2xl p-3.5 flex items-start space-x-3 text-xs animate-fadeIn">
          <span className="text-lg leading-none">✓</span>
          <div className="flex-1 space-y-0.5">
            <div className="flex items-center justify-between">
              <span className="font-extrabold text-[#7CFF6B]">
                Physical Scale Calibrated ({detectionResult.calibration.pixels_per_mm?.toFixed(2)} px/mm)
              </span>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-[#7CFF6B]/20 text-[#7CFF6B] font-bold">
                ArUco #{detectionResult.calibration.marker_id} ({detectionResult.calibration.reference_width_mm}mm)
              </span>
            </div>
            <p className="text-[#A7A7B0] text-[11px]">
              Physical millimeter diameters are computed from the verified reference fiducial marker.
            </p>
            {detectionResult.calibration.perspective_warning && (
              <p className="text-amber-400 text-[10px] font-medium mt-1">
                ⚠ {detectionResult.calibration.perspective_warning}
              </p>
            )}
          </div>
        </div>
      ) : (
        <div className="bg-amber-500/10 border border-amber-500/30 rounded-2xl p-3.5 flex items-start space-x-3 text-xs animate-fadeIn">
          <span className="text-lg leading-none">⚠</span>
          <div className="flex-1 space-y-0.5">
            <div className="flex items-center justify-between">
              <span className="font-extrabold text-amber-400">
                Reference Marker Not Detected — Relative Sizing Active
              </span>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 font-bold">
                Uncalibrated
              </span>
            </div>
            <p className="text-[#A7A7B0] text-[11px]">
              Physical diameter (mm) is unavailable. Sizing is estimated relatively against batch median.
            </p>
          </div>
        </div>
      )}

      {/* Tab Switcher */}
      <div className="flex items-center bg-[#151518] p-1 rounded-2xl border border-white/10">
        <button
          onClick={() => setActiveTab('annotated')}
          className={`flex-1 py-2 text-xs font-bold rounded-xl transition flex items-center justify-center space-x-1.5 ${
            activeTab === 'annotated'
              ? 'bg-[#7CFF6B] text-[#0B0B0D] shadow-md font-extrabold'
              : 'text-[#A7A7B0] hover:text-white'
          }`}
        >
          <Eye className="w-3.5 h-3.5" />
          <span>Annotated Image</span>
        </button>

        <button
          onClick={() => setActiveTab('crops')}
          className={`flex-1 py-2 text-xs font-bold rounded-xl transition flex items-center justify-center space-x-1.5 ${
            activeTab === 'crops'
              ? 'bg-[#7CFF6B] text-[#0B0B0D] shadow-md font-extrabold'
              : 'text-[#A7A7B0] hover:text-white'
          }`}
        >
          <Grid className="w-3.5 h-3.5" />
          <span>Individual Crops ({detectionResult.total_onions})</span>
        </button>
      </div>

      {/* Main Content View */}
      {activeTab === 'annotated' ? (
        <div className="bg-[#1B1B20] border border-white/10 rounded-3xl p-3 shadow-2xl space-y-3">
          <div className="relative bg-[#0B0B0D] rounded-2xl overflow-hidden p-1 flex items-center justify-center">
            <img
              src={imageUrl}
              alt="Annotated Onion Batch"
              className="max-h-[420px] w-auto max-w-full rounded-xl object-contain shadow-xl"
            />
          </div>
          <div className="flex items-center justify-between text-[11px] text-[#A7A7B0] px-2">
            <span>{detectionResult.total_onions} onions detected</span>
            <span>Avg Confidence: {avgConfidence}%</span>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          {detectionResult.onions.map((onion) => {
            const cropUrl = onion.crop_path.startsWith('http')
              ? onion.crop_path
              : `${API_BASE_URL}/${onion.crop_path.replace(/^\//, '')}`;

            return (
              <div
                key={onion.id}
                className="bg-[#1B1B20] border border-white/10 rounded-2xl p-2.5 space-y-2 text-center shadow-xl hover:border-white/20 transition"
              >
                <div className="aspect-square bg-[#0B0B0D] rounded-xl overflow-hidden flex items-center justify-center p-1 border border-white/5">
                  <img
                    src={cropUrl}
                    alt={onion.label}
                    className="w-full h-full object-cover rounded-lg"
                    onError={(e) => {
                      (e.target as HTMLElement).style.display = 'none';
                    }}
                  />
                </div>
                <div>
                  <span className="font-extrabold text-xs text-white block">{onion.label}</span>
                  <span className="text-[10px] font-bold text-[#7CFF6B]">
                    {Math.round(onion.confidence * 100)}% Conf
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
