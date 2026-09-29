'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { checkHealth } from '@/lib/api';
import { CheckCircle2, AlertCircle, Bell, Search, Sparkles, User, Smartphone, Download } from 'lucide-react';

export default function Header() {
  const [backendStatus, setBackendStatus] = useState<'online' | 'offline' | 'checking'>('checking');

  useEffect(() => {
    const verifyBackend = async () => {
      try {
        await checkHealth();
        setBackendStatus('online');
      } catch (err) {
        setBackendStatus('offline');
      }
    };
    verifyBackend();
    const interval = setInterval(verifyBackend, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="bg-[#1f131a] border-b border-white/5 px-6 py-4 flex items-center justify-between sticky top-0 z-40 backdrop-blur-md bg-opacity-90">
      {/* Greeting & Search */}
      <div className="flex items-center space-x-6">
        <div>
          <h2 className="text-sm font-medium text-slate-400">Welcome back,</h2>
          <h1 className="text-lg font-extrabold text-white tracking-tight flex items-center space-x-2">
            <span>Procurement Center Officer</span>
            <span className="text-xs px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 font-bold border border-amber-500/30">
              Station #4
            </span>
          </h1>
        </div>
      </div>

      {/* Right Controls */}
      <div className="flex items-center space-x-3">
        {/* Mobile App Download Button */}
        <Link
          href="/download"
          className="flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-emerald-500/15 border border-emerald-500/30 hover:border-emerald-500/60 hover:bg-emerald-500/25 text-emerald-300 hover:text-white text-xs font-bold transition shadow-sm"
          title="Download Android APK"
        >
          <Smartphone className="w-3.5 h-3.5" />
          <span>Download App (.APK)</span>
        </Link>

        {/* Backend API Status Pill */}
        <div className="flex items-center space-x-2 px-3 py-1.5 rounded-full bg-[#2d1b25] border border-white/10 text-xs">
          {backendStatus === 'online' ? (
            <>
              <div className="w-2.5 h-2.5 bg-emerald-400 rounded-full animate-pulse" />
              <span className="text-emerald-300 font-extrabold">API Online</span>
            </>
          ) : backendStatus === 'offline' ? (
            <>
              <div className="w-2.5 h-2.5 bg-rose-500 rounded-full" />
              <span className="text-rose-400 font-extrabold">API Offline</span>
            </>
          ) : (
            <>
              <div className="w-2.5 h-2.5 bg-amber-400 rounded-full animate-ping" />
              <span className="text-amber-300 font-bold">Connecting...</span>
            </>
          )}
        </div>

        {/* User Profile Avatar */}
        <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-amber-500 to-rose-500 p-0.5 flex items-center justify-center shadow-md">
          <div className="w-full h-full rounded-full bg-[#24171d] flex items-center justify-center text-amber-300 font-bold text-sm">
            AP
          </div>
        </div>
      </div>
    </header>
  );
}
