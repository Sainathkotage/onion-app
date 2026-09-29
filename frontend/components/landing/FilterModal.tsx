'use client';

import React from 'react';
import { X, SlidersHorizontal } from 'lucide-react';
import { GameItem } from './types';
import { playSwitchSound } from './audio';

interface FilterModalProps {
  isOpen: boolean;
  onClose: () => void;
  selectedCategory: string;
  setSelectedCategory: (cat: string) => void;
  filteredGames: GameItem[];
  onSelectGame: (game: GameItem) => void;
  soundEnabled: boolean;
}

const CATEGORIES = ['All', 'Platformer', 'Action', 'Battle Royale', 'Multiplayer'];

export default function FilterModal({
  isOpen,
  onClose,
  selectedCategory,
  setSelectedCategory,
  filteredGames,
  onSelectGame,
  soundEnabled,
}: FilterModalProps) {
  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 animate-fadeIn select-none"
      onClick={onClose}
    >
      <div
        className="w-full max-w-md bg-[#16171e] border border-white/15 rounded-3xl p-6 shadow-2xl space-y-5"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-black text-white flex items-center gap-2">
            <SlidersHorizontal className="w-4 h-4 text-sky-400" />
            <span>Filter Nintendo Catalog</span>
          </h3>
          <button
            onClick={() => {
              playSwitchSound('click', soundEnabled);
              onClose();
            }}
            className="p-1.5 text-neutral-400 hover:text-white rounded-full bg-white/5"
            title="Close"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Category Pills */}
        <div className="space-y-2">
          <label className="text-xs font-bold uppercase tracking-wider text-neutral-400">
            Categories
          </label>
          <div className="flex flex-wrap gap-2">
            {CATEGORIES.map((cat) => (
              <button
                key={cat}
                onClick={() => {
                  setSelectedCategory(cat);
                  playSwitchSound('click', soundEnabled);
                }}
                className={`px-3 py-1.5 rounded-full text-xs font-bold transition ${
                  selectedCategory === cat
                    ? 'bg-sky-500 text-white shadow-md'
                    : 'bg-[#22242d] text-neutral-400 hover:text-white'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Matching Games */}
        <div className="space-y-2 pt-2 border-t border-white/10">
          <label className="text-xs font-bold uppercase tracking-wider text-neutral-400">
            Matches ({filteredGames.length})
          </label>
          <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
            {filteredGames.map((g) => (
              <div
                key={g.id}
                onClick={() => {
                  onSelectGame(g);
                  onClose();
                  playSwitchSound('select', soundEnabled);
                }}
                className="flex items-center justify-between p-2.5 rounded-xl bg-[#20222a] hover:bg-[#282a35] cursor-pointer transition border border-white/5"
              >
                <div className="flex items-center gap-3">
                  <div
                    className={`w-9 h-9 rounded-lg bg-gradient-to-br ${g.gradient} flex items-center justify-center text-xs font-black text-white shadow-sm`}
                  >
                    {g.title[0]}
                  </div>
                  <div>
                    <div className="text-xs font-black text-white">{g.title}</div>
                    <div className="text-[10px] text-neutral-400">{g.subtitle}</div>
                  </div>
                </div>
                <span className="text-xs font-bold text-sky-400">⭐ {g.rating}</span>
              </div>
            ))}
          </div>
        </div>

        <button
          onClick={() => {
            playSwitchSound('click', soundEnabled);
            onClose();
          }}
          className="w-full py-2.5 bg-white text-neutral-950 font-black text-xs rounded-xl shadow transition hover:bg-neutral-200"
        >
          Apply Filter
        </button>
      </div>
    </div>
  );
}
