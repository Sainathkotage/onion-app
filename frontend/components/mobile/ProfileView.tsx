'use client';

import React from 'react';
import { User, Cpu, ShieldCheck, Settings, Info, Bell, Moon } from 'lucide-react';

export default function ProfileView() {
  return (
    <div className="space-y-5 animate-fadeIn">
      {/* Profile Header */}
      <div className="bg-[#1B1B20] border border-white/10 rounded-3xl p-5 shadow-2xl flex items-center space-x-4">
        <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-[#7CFF6B] to-emerald-400 p-0.5 flex items-center justify-center shadow-lg shadow-[#7CFF6B]/20">
          <div className="w-full h-full rounded-[14px] bg-[#0B0B0D] flex items-center justify-center text-[#7CFF6B] font-black text-xl">
            PC
          </div>
        </div>
        <div>
          <h2 className="text-lg font-black text-white">Procurement Officer</h2>
          <p className="text-xs text-[#A7A7B0]">Procurement Station #4 • Center ID #26031</p>
          <div className="mt-1.5 inline-flex items-center space-x-1.5 px-2.5 py-0.5 rounded-full bg-[#7CFF6B]/15 text-[#7CFF6B] text-[10px] font-bold border border-[#7CFF6B]/30">
            <ShieldCheck className="w-3 h-3" />
            <span>Authorized Quality Assessor</span>
          </div>
        </div>
      </div>

      {/* AI Model Status Card */}
      <div className="bg-[#1B1B20] border border-white/10 rounded-3xl p-5 space-y-3 shadow-xl">
        <div className="flex items-center space-x-2">
          <Cpu className="w-5 h-5 text-[#7CFF6B]" />
          <h3 className="text-sm font-black text-white">AI Engine & Model Pipeline</h3>
        </div>
        
        <div className="space-y-2 text-xs divide-y divide-white/5">
          <div className="pt-1 flex justify-between">
            <span className="text-[#A7A7B0]">Detector Algorithm:</span>
            <span className="font-bold text-white">OpenCV Watershed / Roboflow</span>
          </div>
          <div className="pt-2 flex justify-between">
            <span className="text-[#A7A7B0]">Classifier Architecture:</span>
            <span className="font-bold text-white">DenseNet121 / AIDE ML Fine-Tuned</span>
          </div>
          <div className="pt-2 flex justify-between">
            <span className="text-[#A7A7B0]">Defect Classes:</span>
            <span className="font-bold text-[#7CFF6B]">5 Standardized Classes</span>
          </div>
          <div className="pt-2 flex justify-between">
            <span className="text-[#A7A7B0]">System Build:</span>
            <span className="font-bold text-white">v3.2.0 (SIH 2026 Prototype)</span>
          </div>
        </div>
      </div>

      {/* Settings List */}
      <div className="bg-[#1B1B20] border border-white/10 rounded-3xl p-3 shadow-xl divide-y divide-white/5 text-sm">
        <div className="p-3 flex items-center justify-between hover:bg-white/5 rounded-2xl transition cursor-pointer">
          <div className="flex items-center space-x-3">
            <Bell className="w-4 h-4 text-[#A7A7B0]" />
            <span className="text-white font-medium">Notification Preferences</span>
          </div>
          <span className="text-xs text-[#7CFF6B] font-bold">Enabled</span>
        </div>

        <div className="p-3 flex items-center justify-between hover:bg-white/5 rounded-2xl transition cursor-pointer">
          <div className="flex items-center space-x-3">
            <Moon className="w-4 h-4 text-[#A7A7B0]" />
            <span className="text-white font-medium">Dark Mode Interface</span>
          </div>
          <span className="text-xs text-[#7CFF6B] font-bold">OLED Dark</span>
        </div>

        <div className="p-3 flex items-center justify-between hover:bg-white/5 rounded-2xl transition cursor-pointer">
          <div className="flex items-center space-x-3">
            <Info className="w-4 h-4 text-[#A7A7B0]" />
            <span className="text-white font-medium">About OnionIQ</span>
          </div>
          <span className="text-xs text-[#A7A7B0]">v3.2</span>
        </div>
      </div>
    </div>
  );
}
