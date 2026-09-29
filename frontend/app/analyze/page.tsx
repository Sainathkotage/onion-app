'use client';

import React, { useState } from 'react';
import ImageUploader from '@/components/ImageUploader';
import ImagePreview from '@/components/ImagePreview';
import AnalysisStepper from '@/components/AnalysisStepper';
import DetectionView from '@/components/DetectionView';
import ClassificationGrid from '@/components/ClassificationGrid';
import GradingDashboard from '@/components/GradingDashboard';
import {
  uploadImage,
  detectOnions,
  classifyOnions,
  gradeBatch,
  UploadResponse,
  DetectionResult,
  BatchClassificationResult,
  BatchGradingResult,
} from '@/lib/api';
import { RefreshCw, ShieldCheck, Eye, Grid, Award, AlertTriangle, Sparkles } from 'lucide-react';

export default function AnalyzePage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [currentStepIndex, setCurrentStepIndex] = useState<number>(0);
  
  const [uploadResult, setUploadResult] = useState<UploadResponse | null>(null);
  const [detectionResult, setDetectionResult] = useState<DetectionResult | null>(null);
  const [classificationResult, setClassificationResult] = useState<BatchClassificationResult | null>(null);
  const [gradingResult, setGradingResult] = useState<BatchGradingResult | null>(null);
  
  const [viewTab, setViewTab] = useState<'dashboard' | 'classification' | 'detection'>('dashboard');
  const [error, setError] = useState<string | null>(null);

  const stepMessages = [
    'Stage 1: Uploading batch image to backend API...',
    'Stage 2: Segmenting & counting onions with Google Gemini Vision...',
    'Stage 3: Diagnosing quality & defect categories with Gemini Multimodal AI...',
    'Stage 4: Calculating Grade A %, URS %, defect breakdown & report...',
    'Stage 5: Finalizing assessment dashboard and quality certificate!'
  ];

  const handleImageSelected = (file: File) => {
    setSelectedFile(file);
    setUploadResult(null);
    setDetectionResult(null);
    setClassificationResult(null);
    setGradingResult(null);
    setError(null);
  };

  const handleReset = () => {
    setSelectedFile(null);
    setUploadResult(null);
    setDetectionResult(null);
    setClassificationResult(null);
    setGradingResult(null);
    setError(null);
    setCurrentStepIndex(0);
  };

  const handleAnalyze = async () => {
    if (!selectedFile || isProcessing) return;

    setIsProcessing(true);
    setError(null);
    setCurrentStepIndex(0);

    try {
      // Step 1: Upload Image
      setCurrentStepIndex(0);
      const uploadRes = await uploadImage(selectedFile);
      setUploadResult(uploadRes);

      // Step 2: Detect Onions
      setCurrentStepIndex(1);
      const detectRes = await detectOnions(uploadRes.upload_id, uploadRes.filename);
      setDetectionResult(detectRes);

      // Step 3: Classify Defect Classes
      setCurrentStepIndex(2);
      const classifyRes = await classifyOnions(uploadRes.upload_id, detectRes.onions, detectRes.calibration);
      setClassificationResult(classifyRes);

      // Step 4: Calculate Grading & Report Data
      setCurrentStepIndex(3);
      const gradeRes = await gradeBatch(uploadRes.upload_id, classifyRes.classifications, detectRes.calibration);
      setGradingResult(gradeRes);

      // Step 5: Complete
      setCurrentStepIndex(4);
      setViewTab('dashboard');

    } catch (err: any) {
      console.error('Analysis Pipeline Error:', err);
      setError(err.message || 'An unexpected error occurred during analysis.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="space-y-8 py-2 animate-fadeIn">
      {/* Top Workflow Header */}
      <div className="bg-[#24161f] p-6 rounded-3xl border border-white/10 shadow-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">
            Batch Quality Assessment
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            End-to-End Workflow: Capture Photo → Detect → Classify Defects → Grade A / URS → PDF Certificate
          </p>
        </div>

        <div className="flex items-center space-x-3 self-start md:self-auto">
          {gradingResult && (
            <>
              {/* Navigation View Tabs */}
              <div className="flex items-center bg-[#191016] p-1 rounded-2xl border border-white/10">
                <button
                  onClick={() => setViewTab('dashboard')}
                  className={`px-3 py-2 text-xs font-bold rounded-xl transition flex items-center space-x-1.5 ${
                    viewTab === 'dashboard'
                      ? 'bg-amber-400 text-slate-950 shadow-md'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  <Award className="w-3.5 h-3.5" />
                  <span>Quality Report</span>
                </button>
                <button
                  onClick={() => setViewTab('classification')}
                  className={`px-3 py-2 text-xs font-bold rounded-xl transition flex items-center space-x-1.5 ${
                    viewTab === 'classification'
                      ? 'bg-amber-400 text-slate-950 shadow-md'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  <Grid className="w-3.5 h-3.5" />
                  <span>Defect Grid</span>
                </button>
                <button
                  onClick={() => setViewTab('detection')}
                  className={`px-3 py-2 text-xs font-bold rounded-xl transition flex items-center space-x-1.5 ${
                    viewTab === 'detection'
                      ? 'bg-amber-400 text-slate-950 shadow-md'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  <Eye className="w-3.5 h-3.5" />
                  <span>Detection View</span>
                </button>
              </div>

              <button
                onClick={handleReset}
                className="px-4 py-2.5 bg-white/5 hover:bg-white/10 text-white font-bold text-xs rounded-xl transition flex items-center space-x-1.5 border border-white/10"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>Assess Another Batch</span>
              </button>
            </>
          )}

          <div className="flex items-center space-x-2 text-xs font-bold px-3.5 py-2 bg-emerald-500/10 text-emerald-300 rounded-2xl border border-emerald-500/20">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>Prototype Ready</span>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      {isProcessing ? (
        <AnalysisStepper
          currentStepIndex={currentStepIndex}
          stepMessages={stepMessages}
        />
      ) : gradingResult && uploadResult && classificationResult && detectionResult ? (
        viewTab === 'dashboard' ? (
          <GradingDashboard
            uploadId={uploadResult.upload_id}
            gradingResult={gradingResult}
            classifications={classificationResult.classifications}
            annotatedImageUrl={detectionResult.annotated_image_url}
            onReset={handleReset}
          />
        ) : viewTab === 'classification' ? (
          <ClassificationGrid classificationResult={classificationResult} />
        ) : (
          <DetectionView detectionResult={detectionResult} />
        )
      ) : !selectedFile ? (
        <ImageUploader onImageSelected={handleImageSelected} />
      ) : (
        <div className="space-y-6">
          <ImagePreview
            file={selectedFile}
            onReset={handleReset}
            onAnalyze={handleAnalyze}
            isAnalyzing={isProcessing}
          />

          {error && (
            <div className="max-w-3xl mx-auto p-5 bg-rose-950/40 border border-rose-500/30 rounded-2xl flex items-start space-x-3 text-rose-300 text-sm">
              <AlertTriangle className="w-5 h-5 flex-shrink-0 text-rose-400 mt-0.5" />
              <div>
                <h4 className="font-bold text-white">Pipeline Execution Error</h4>
                <p className="mt-0.5 text-rose-300">{error}</p>
                <button
                  onClick={handleAnalyze}
                  className="mt-3 px-4 py-1.5 bg-rose-500 hover:bg-rose-400 text-white font-bold text-xs rounded-xl transition"
                >
                  Retry Analysis
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
