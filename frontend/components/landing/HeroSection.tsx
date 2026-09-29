'use client';

import React from 'react';
import Image from 'next/image';

export default function HeroSection() {
  return (
    <div className="relative w-full text-center max-w-2xl mx-auto space-y-3 pt-2 select-none">
      {/* Floating 3D Golden Blaster / Cannon (Left) */}
      <div className="absolute -top-4 -left-6 sm:-left-16 md:-left-28 lg:-left-36 hidden sm:block pointer-events-none z-10 animate-float">
        <div className="relative w-28 h-28 sm:w-36 sm:h-36 md:w-44 md:h-44 filter drop-shadow-[0_15px_30px_rgba(234,179,8,0.3)]">
          <Image
            src="/games/golden_blaster.png"
            alt="Golden Blaster Cannon"
            fill
            className="object-contain"
            priority
          />
        </div>
      </div>

      {/* Floating Flying Charizard (Right) */}
      <div className="absolute -top-2 -right-6 sm:-right-16 md:-right-24 lg:-right-32 hidden sm:block pointer-events-none z-10 animate-float-delayed">
        <div className="relative w-24 h-24 sm:w-32 sm:h-32 md:w-40 md:h-40 filter drop-shadow-[0_15px_30px_rgba(249,115,22,0.35)]">
          <Image
            src="/games/charizard.png"
            alt="Flying Charizard"
            fill
            className="object-contain"
            priority
          />
        </div>
      </div>

      {/* Center Background Nintendo Switch Console Silhouette */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[460px] h-[220px] pointer-events-none opacity-15 -rotate-6 z-0">
        <div className="w-full h-full rounded-[30px] border-4 border-white/20 bg-gradient-to-br from-neutral-800 to-black p-4 flex items-center justify-between shadow-2xl">
          <div className="w-11 h-24 rounded-l-2xl bg-sky-500/30 border border-sky-400/40" />
          <div className="flex-1 h-32 mx-4 rounded-xl bg-neutral-900 border border-white/10" />
          <div className="w-11 h-24 rounded-r-2xl bg-red-500/30 border border-red-400/40" />
        </div>
      </div>

      {/* 5 Months — Free Access Badge */}
      <div className="inline-flex items-center gap-1.5 px-3.5 py-1 rounded-full bg-[#1c1d25] border border-amber-400/30 shadow-sm text-xs font-semibold text-amber-300 relative z-10 hover:border-amber-400/50 transition">
        <span className="text-sm">🎁</span>
        <span>5 Months — Free Access</span>
      </div>

      {/* Main Bold Headline */}
      <h1 className="text-3xl sm:text-5xl md:text-6xl font-black tracking-tight text-white leading-[1.08] relative z-10">
        Fun Games
        <br />
        <span className="bg-gradient-to-r from-white via-neutral-100 to-neutral-300 bg-clip-text text-transparent">
          Nintendo Switch
        </span>
      </h1>

      {/* Curated Selection Subtitle */}
      <p className="text-neutral-400 text-xs sm:text-sm max-w-md sm:max-w-lg mx-auto leading-relaxed relative z-10 px-4">
        Be sure to try our selection of games, we have carefully chosen them. There are games for all tastes.
      </p>
    </div>
  );
}
