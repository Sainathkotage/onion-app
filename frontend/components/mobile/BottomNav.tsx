'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, Camera, History, FileText, User, Plus } from 'lucide-react';

export default function BottomNav() {
  const pathname = usePathname();

  const navItems = [
    { name: 'Home', href: '/', icon: Home },
    { name: 'History', href: '/history', icon: History },
    { name: 'Inspect', href: '/analyze', isPrimary: true, icon: Plus },
    { name: 'Reports', href: '/reports', icon: FileText },
    { name: 'Profile', href: '/profile', icon: User },
  ];

  return (
    <nav className="fixed bottom-4 left-1/2 -translate-x-1/2 z-50 w-[92%] max-w-md">
      <div className="glass-nav rounded-full px-4 py-2.5 flex items-center justify-between shadow-2xl border border-white/10">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;

          if (item.isPrimary) {
            return (
              <Link
                key={item.href}
                href={item.href}
                className="flex items-center space-x-1.5 px-4 py-2 bg-[#7CFF6B] hover:bg-[#6be65b] text-[#0B0B0D] font-extrabold rounded-full shadow-lg glow-accent transition transform active:scale-95"
              >
                <Camera className="w-4 h-4 text-[#0B0B0D]" />
                <span className="text-xs tracking-tight">Inspect</span>
              </Link>
            );
          }

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex flex-col items-center justify-center space-y-0.5 px-2.5 py-1 rounded-xl transition ${
                isActive
                  ? 'text-[#7CFF6B] font-bold'
                  : 'text-[#A7A7B0] hover:text-white'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span className="text-[10px] tracking-tight">{item.name}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
