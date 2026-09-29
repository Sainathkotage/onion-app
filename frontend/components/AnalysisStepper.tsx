'use client';

import React from 'react';
import { CheckCircle2, Loader2, Cpu, Scan, Layers, Award, Sparkles } from 'lucide-react';

interface AnalysisStepperProps {
  currentStepIndex: number; // 0 to 4
  stepMessages: string[];
}

export default function AnalysisStepper({ currentStepIndex, stepMessages }: AnalysisStepperProps) {
  const steps = [
    { title: 'Image Uploaded', icon: Scan },
    { title: 'Detecting Onions', icon: Layers },
    { title: 'Classifying Quality', icon: Cpu },
    { title: 'Calculating Grade & URS', icon: Award },
    { title: 'Generating Quality Report', icon: Sparkles },
  ];

  return (
    <div className="w-full bg-[#1B1B20] border border-white/10 rounded-3xl p-6 shadow-2xl space-y-5 animate-fadeIn">
      <div className="text-center space-y-1.5">
        <div className="inline-flex items-center space-x-1.5 px-3 py-1 bg-[#7CFF6B]/15 text-[#7CFF6B] rounded-full text-xs font-bold border border-[#7CFF6B]/30">
          <Sparkles className="w-3.5 h-3.5 animate-pulse" />
          <span>Computer Vision Pipeline</span>
        </div>
        <h3 className="text-xl font-black text-white tracking-tight">Analyzing Batch</h3>
        <p className="text-xs text-[#A7A7B0] max-w-xs mx-auto">
          {stepMessages[currentStepIndex] || 'Executing quality analysis pipeline...'}
        </p>
      </div>

      {/* Stepper Steps List */}
      <div className="space-y-2.5 pt-2">
        {steps.map((step, idx) => {
          const StepIcon = step.icon;
          const isDone = idx < currentStepIndex;
          const isCurrent = idx === currentStepIndex;

          return (
            <div
              key={step.title}
              className={`flex items-center space-x-3.5 p-3 rounded-2xl border transition-all duration-300 ${
                isDone
                  ? 'bg-[#7CFF6B]/10 border-[#7CFF6B]/30 text-[#7CFF6B]'
                  : isCurrent
                  ? 'bg-[#FFB547]/10 border-[#FFB547]/40 text-[#FFB547] shadow-lg glow-warning'
                  : 'bg-[#151518] border-white/5 text-[#A7A7B0]'
              }`}
            >
              <div
                className={`w-9 h-9 rounded-xl flex items-center justify-center font-bold text-xs flex-shrink-0 ${
                  isDone
                    ? 'bg-[#7CFF6B] text-[#0B0B0D]'
                    : isCurrent
                    ? 'bg-[#FFB547] text-[#0B0B0D] shadow-md'
                    : 'bg-white/5 text-[#A7A7B0]'
                }`}
              >
                {isDone ? (
                  <CheckCircle2 className="w-5 h-5" />
                ) : isCurrent ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <StepIcon className="w-4 h-4" />
                )}
              </div>

              <div className="flex-1">
                <span className="font-extrabold text-xs block text-white">{step.title}</span>
                <span className="text-[10px] opacity-75">
                  {isDone ? '✓ Completed' : isCurrent ? '◉ In Progress...' : '○ Pending'}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
