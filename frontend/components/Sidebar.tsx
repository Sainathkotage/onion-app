'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, Camera, BarChart3, ShieldCheck, Sparkles, HelpCircle, Settings, Smartphone } from 'lucide-react';

export default function Sidebar() {
  const pathname = usePathname();

  const navItems = [
    { name: 'Dashboard', href: '/', icon: Home },
    { name: 'Assess Batch', href: '/analyze', icon: Camera },
    { name: 'Mobile App', href: '/download', icon: Smartphone },
  ];

  return (
    <aside className="w-20 lg:w-64 bg-[#23151d] border-r border-white/5 flex flex-col justify-between p-4 flex-shrink-0 min-h-screen">
      <div className="space-y-8">
        {/* Brand Logo */}
        <Link href="/" className="flex items-center space-x-3 group px-2">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-amber-500 to-amber-400 text-slate-950 font-black text-2xl flex items-center justify-center shadow-lg shadow-amber-500/20 transform group-hover:scale-105 transition duration-200">
            🧅
          </div>
          <div className="hidden lg:block">
            <span className="text-xl font-black text-white tracking-tight block">OnionIQ</span>
            <span className="text-[10px] font-semibold text-amber-400/80 uppercase tracking-widest block">
              Procurement AI
            </span>
          </div>
        </Link>

        {/* Navigation Section */}
        <nav className="space-y-2">
          <div className="hidden lg:block px-3 text-[10px] font-bold uppercase tracking-wider text-white/30 mb-2">
            Main Menu
          </div>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center space-x-3 px-3.5 py-3 rounded-2xl transition font-bold text-sm ${
                  isActive
                    ? 'bg-amber-400 text-slate-950 shadow-lg shadow-amber-400/20'
                    : 'text-slate-400 hover:text-white hover:bg-white/5'
                }`}
              >
                <Icon className="w-5 h-5 flex-shrink-0" />
                <span className="hidden lg:inline">{item.name}</span>
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Footer / Demo Mode Badge */}
      <div className="space-y-4 pt-6 border-t border-white/5">
        <div className="hidden lg:block bg-[#2d1b25] p-3.5 rounded-2xl border border-white/5 text-xs space-y-2">
          <div className="flex items-center justify-between">
            <span className="font-extrabold text-amber-300 flex items-center space-x-1">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Prototype Mode</span>
            </span>
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
          </div>
          <p className="text-[11px] text-slate-400 leading-tight">
            CV & ML pipeline executing with deterministic fallback classifier.
          </p>
        </div>

        <div className="text-center text-[10px] text-slate-500 font-mono hidden lg:block">
          v1.0.0 • Problem 26031
        </div>
      </div>
    </aside>
  );
}
