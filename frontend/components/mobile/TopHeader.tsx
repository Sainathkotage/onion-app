'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { checkHealth } from '@/lib/api';
import { Cpu, ShieldCheck, User } from 'lucide-react';

export default function TopHeader() {
  const [backendStatus, setBackendStatus] = useState<'online' | 'offline' | 'checking'>('checking');
  const [greeting, setGreeting] = useState<string>('Good day');

  useEffect(() => {
    const hour = new Date().getHours();
    if (hour < 12) setGreeting('Good morning');
    else if (hour < 18) setGreeting('Good afternoon');
    else setGreeting('Good evening');

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
    <header className="sticky top-0 z-40 bg-[#0B0B0D]/90 backdrop-blur-xl border-b border-white/5 px-4 py-3 sm:px-6">
      <div className="max-w-md mx-auto flex items-center justify-between">
        {/* Top Left: Logo & Branding */}
        <Link href="/" className="flex items-center space-x-2 group">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-[#7CFF6B] to-emerald-400 p-0.5 flex items-center justify-center shadow-lg shadow-[#7CFF6B]/20">
            <div className="w-full h-full rounded-[10px] bg-[#0B0B0D] flex items-center justify-center">
              <Cpu className="w-5 h-5 text-[#7CFF6B]" />
            </div>
          </div>
          <div>
            <div className="flex items-center space-x-1">
              <span className="text-base font-black tracking-tight text-white">OnionIQ</span>
              <span className="text-[10px] px-1.5 py-0.2 rounded bg-[#7CFF6B]/15 text-[#7CFF6B] font-bold border border-[#7CFF6B]/30">
                PRO
              </span>
            </div>
            <p className="text-[10px] text-[#A7A7B0] font-medium tracking-tight">AI Quality Assessment</p>
          </div>
        </Link>

        {/* Top Right: Status Pill & Avatar */}
        <div className="flex items-center space-x-2.5">
          {/* API Health Pill */}
          <div className="px-2.5 py-1 rounded-full bg-[#151518] border border-white/10 flex items-center space-x-1.5 text-[11px]">
            {backendStatus === 'online' ? (
              <>
                <span className="w-2 h-2 rounded-full bg-[#7CFF6B] animate-pulse" />
                <span className="text-[#7CFF6B] font-bold">AI Online</span>
              </>
            ) : backendStatus === 'offline' ? (
              <>
                <span className="w-2 h-2 rounded-full bg-[#FF5C5C]" />
                <span className="text-[#FF5C5C] font-bold">Prototype</span>
              </>
            ) : (
              <>
                <span className="w-2 h-2 rounded-full bg-[#FFB547] animate-ping" />
                <span className="text-[#FFB547] font-bold">Connecting</span>
              </>
            )}
          </div>

          {/* Profile Avatar */}
          <Link
            href="/profile"
            className="w-8 h-8 rounded-full bg-[#1B1B20] border border-white/10 flex items-center justify-center text-white text-xs font-bold hover:border-[#7CFF6B]/50 transition"
          >
            <User className="w-4 h-4 text-[#A7A7B0]" />
          </Link>
        </div>
      </div>
    </header>
  );
}
