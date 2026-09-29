'use client';

import React from 'react';
import Image from 'next/image';
import { X, Star, Check, Download } from 'lucide-react';
import { GameItem } from './types';
import { playSwitchSound } from './audio';

interface GameModalProps {
  game: GameItem | null;
  onClose: () => void;
  onAddToCart: () => void;
  soundEnabled: boolean;
}

export default function GameModal({
  game,
  onClose,
  onAddToCart,
  soundEnabled,
}: GameModalProps) {
  if (!game) return null;

  return (
    <div
      className="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-4 animate-fadeIn select-none"
      onClick={onClose}
    >
      <div
        className="w-full max-w-lg bg-[#14151b] border border-white/15 rounded-3xl overflow-hidden shadow-2xl relative"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Header Banner with Theme Gradient */}
        <div
          className={`h-44 bg-gradient-to-r ${game.gradient} relative p-6 flex items-end justify-between overflow-hidden`}
        >
          <button
            onClick={() => {
              playSwitchSound('click', soundEnabled);
              onClose();
            }}
            className="absolute top-4 right-4 p-2 rounded-full bg-black/40 hover:bg-black/70 text-white transition z-20"
            title="Close"
          >
            <X className="w-4 h-4" />
          </button>

          <div className="relative z-10">
            <span className="text-xs font-bold uppercase tracking-wider text-white/80 bg-black/30 px-2.5 py-0.5 rounded-full">
              {game.category}
            </span>
            <h2 className="text-3xl font-black text-white mt-1 drop-shadow-md">
              {game.title}
            </h2>
            <p className="text-sm font-semibold text-white/95">{game.subtitle}</p>
          </div>

          {/* Large Character render */}
          <div className="w-32 h-32 relative -mb-4 shrink-0 pointer-events-none">
            <Image
              src={game.characterImg}
              alt={game.characterAlt}
              fill
              className="object-contain filter drop-shadow-[0_12px_24px_rgba(0,0,0,0.65)]"
            />
          </div>
        </div>

        {/* Modal Body */}
        <div className="p-6 space-y-5">
          {/* Key Specs Row */}
          <div className="grid grid-cols-3 gap-2 bg-[#1b1c24] p-3 rounded-2xl border border-white/5 text-center">
            <div>
              <div className="flex items-center justify-center gap-1 text-amber-400 text-sm font-black">
                <Star className="w-3.5 h-3.5 fill-amber-400" />
                <span>{game.rating}</span>
              </div>
              <span className="text-[10px] text-neutral-400 font-medium">
                ({game.reviewsCount})
              </span>
            </div>
            <div className="border-x border-white/10">
              <span className="text-sm font-black text-white">{game.storageSize}</span>
              <p className="text-[10px] text-neutral-400 font-medium">Download Size</p>
            </div>
            <div>
              <span className="text-sm font-black text-white">{game.players}</span>
              <p className="text-[10px] text-neutral-400 font-medium">Player Support</p>
            </div>
          </div>

          {/* Description */}
          <div className="space-y-1.5">
            <h4 className="text-xs font-bold uppercase tracking-wider text-neutral-400">
              Game Overview
            </h4>
            <p className="text-xs sm:text-sm text-neutral-300 leading-relaxed">
              {game.description}
            </p>
          </div>

          {/* Features Highlights */}
          <div className="space-y-1.5">
            <h4 className="text-xs font-bold uppercase tracking-wider text-neutral-400">
              Hardware Highlights
            </h4>
            <div className="flex flex-wrap gap-2">
              {game.features.map((feat, idx) => (
                <span
                  key={idx}
                  className="text-[11px] font-semibold bg-[#22232c] border border-white/5 text-neutral-300 px-2.5 py-1 rounded-lg flex items-center gap-1.5"
                >
                  <Check className="w-3 h-3 text-sky-400" />
                  {feat}
                </span>
              ))}
            </div>
          </div>

          {/* Pricing & Checkout Action Buttons */}
          <div className="pt-3 border-t border-white/10 flex items-center justify-between gap-3">
            <div>
              <span className="text-xs text-neutral-400 line-through mr-1.5">
                {game.price}
              </span>
              <span className="text-base sm:text-lg font-black text-emerald-400">
                {game.discountPrice || game.price}
              </span>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => {
                  playSwitchSound('coin', soundEnabled);
                  onAddToCart();
                  onClose();
                }}
                className="px-4 py-2.5 bg-[#2563eb] hover:bg-[#1d4ed8] text-white font-bold text-xs rounded-xl shadow-lg transition flex items-center gap-1.5 transform active:scale-95"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Get Free with Pass</span>
              </button>
              <button
                onClick={() => {
                  playSwitchSound('click', soundEnabled);
                  onClose();
                }}
                className="px-3 py-2.5 bg-neutral-800 hover:bg-neutral-700 text-neutral-300 text-xs font-bold rounded-xl transition"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
