'use client';

import React from 'react';
import Image from 'next/image';
import Link from 'next/link';
import {
  Search,
  SlidersHorizontal,
  ShoppingBag,
  Volume2,
  VolumeX,
  Plus,
  Maximize2,
  Minimize2,
  Smartphone,
  Download,
} from 'lucide-react';
import { playSwitchSound } from './audio';

interface NavbarProps {
  activeTab: 'games' | 'store';
  setActiveTab: (tab: 'games' | 'store') => void;
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  coins: number;
  onAddCoins: () => void;
  coinBurst: boolean;
  cartCount: number;
  soundEnabled: boolean;
  setSoundEnabled: (val: boolean) => void;
  onOpenFilter: () => void;
  isFramedMode: boolean;
  setIsFramedMode: (val: boolean) => void;
}

export default function Navbar({
  activeTab,
  setActiveTab,
  searchQuery,
  setSearchQuery,
  coins,
  onAddCoins,
  coinBurst,
  cartCount,
  soundEnabled,
  setSoundEnabled,
  onOpenFilter,
  isFramedMode,
  setIsFramedMode,
}: NavbarProps) {
  return (
    <header className="relative z-40 px-4 sm:px-8 pt-5 pb-4 flex items-center justify-between gap-3 border-b border-white/5 select-none">
      {/* Left: Navigation Tabs & Search Pill */}
      <div className="flex items-center gap-2.5 sm:gap-4 flex-wrap">
        {/* Mode Toggle Tabs */}
        <div className="flex items-center gap-1 bg-[#17181e] p-1 rounded-full border border-white/5 text-xs font-semibold">
          <button
            onClick={() => {
              setActiveTab('games');
              playSwitchSound('click', soundEnabled);
            }}
            className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-full transition ${
              activeTab === 'games'
                ? 'bg-[#23252e] text-white shadow-sm font-bold'
                : 'text-neutral-400 hover:text-white'
            }`}
          >
            <span className="w-1.5 h-1.5 rounded-full bg-white animate-pulse" />
            <span>Games</span>
          </button>
          <button
            onClick={() => {
              setActiveTab('store');
              playSwitchSound('click', soundEnabled);
            }}
            className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-full transition ${
              activeTab === 'store'
                ? 'bg-[#23252e] text-white shadow-sm font-bold'
                : 'text-neutral-400 hover:text-white'
            }`}
          >
            <ShoppingBag className="w-3.5 h-3.5" />
            <span>Store</span>
          </button>
        </div>

        {/* Search Games Pill */}
        <div className="relative flex items-center">
          <div className="flex items-center bg-[#17181e] border border-white/5 hover:border-white/20 transition rounded-full px-3.5 py-1.5 w-40 sm:w-56 focus-within:w-60 focus-within:border-white/30">
            <Search className="w-3.5 h-3.5 text-neutral-400 mr-2 shrink-0" />
            <input
              type="text"
              placeholder="Search Games..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="bg-transparent text-xs text-white placeholder:text-neutral-500 focus:outline-none w-full"
            />
            <button
              onClick={() => {
                onOpenFilter();
                playSwitchSound('click', soundEnabled);
              }}
              className="p-1 text-neutral-400 hover:text-white transition"
              title="Filter Catalog"
            >
              <SlidersHorizontal className="w-3 h-3" />
            </button>
          </div>
        </div>
      </div>

      {/* Center: Official Nintendo Switch Joy-Con Logo */}
      <div className="hidden md:flex items-center justify-center shrink-0">
        <div
          className="flex items-center gap-1 cursor-pointer group"
          title="Nintendo Switch"
          onClick={() => playSwitchSound('click', soundEnabled)}
        >
          <svg
            viewBox="0 0 100 90"
            className="w-11 h-10 fill-white group-hover:scale-105 transition transform drop-shadow-md"
          >
            {/* Left Joy-Con */}
            <path d="M12,0 C5.37,0 0,5.37 0,12 L0,78 C0,84.63 5.37,90 12,90 L38,90 L38,0 L12,0 Z M19,30 C15.13,30 12,26.87 12,23 C12,19.13 15.13,16 19,16 C22.87,16 26,19.13 26,23 C26,26.87 22.87,30 19,30 Z M27,62 C24.24,62 22,59.76 22,57 C22,54.24 24.24,52 27,52 C29.76,52 32,54.24 32,57 C32,59.76 29.76,62 27,62 Z" />
            {/* Right Joy-Con */}
            <path d="M62,0 L62,90 L88,90 C94.63,90 100,84.63 100,78 L100,12 C100,5.37 94.63,0 88,0 L62,0 Z M81,67 C77.13,67 74,63.87 74,60 C74,56.13 77.13,53 81,53 C84.87,53 88,56.13 88,60 C88,63.87 84.87,67 81,67 Z M73,35 C70.24,35 68,32.76 68,30 C68,27.24 70.24,25 73,25 C75.76,25 78,27.24 78,30 C78,32.76 75.76,35 73,35 Z" />
          </svg>
        </div>
      </div>

      {/* Right: Audio, Cart, Mode Toggle, Coin Counter, User Avatar */}
      <div className="flex items-center gap-2 sm:gap-3">
        {/* Audio Toggle */}
        <button
          onClick={() => {
            setSoundEnabled(!soundEnabled);
            playSwitchSound('click', true);
          }}
          className="p-2 rounded-full bg-[#17181e] border border-white/5 hover:border-white/20 text-neutral-400 hover:text-white transition"
          title={soundEnabled ? 'Mute Sounds' : 'Enable Nintendo Sounds'}
        >
          {soundEnabled ? <Volume2 className="w-4 h-4 text-sky-400" /> : <VolumeX className="w-4 h-4" />}
        </button>

        {/* Shopping Cart Pill */}
        <div className="relative">
          <button
            onClick={() => playSwitchSound('click', soundEnabled)}
            className="p-2 rounded-full bg-[#17181e] border border-white/5 hover:border-white/20 text-neutral-300 hover:text-white transition relative"
            title="Cart"
          >
            <ShoppingBag className="w-4 h-4" />
            {cartCount > 0 && (
              <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-red-500 text-[10px] font-bold text-white flex items-center justify-center">
                {cartCount}
              </span>
            )}
          </button>
        </div>

        {/* View Mode Toggle (Frame vs Full-width) */}
        <button
          onClick={() => setIsFramedMode(!isFramedMode)}
          className="hidden lg:flex p-2 rounded-full bg-[#17181e] border border-white/5 hover:border-white/20 text-neutral-400 hover:text-white transition"
          title={isFramedMode ? 'Expand to Full View' : 'Show Frame Border'}
        >
          {isFramedMode ? <Maximize2 className="w-4 h-4" /> : <Minimize2 className="w-4 h-4" />}
        </button>

        {/* Mobile App Download Button */}
        <Link
          href="/download"
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-emerald-500/15 border border-emerald-500/30 hover:border-emerald-500/60 hover:bg-emerald-500/25 text-emerald-300 hover:text-white transition text-xs font-semibold shadow-sm"
          title="Download Mobile Android App (.APK)"
        >
          <Smartphone className="w-3.5 h-3.5 text-emerald-400" />
          <span className="hidden sm:inline">Get App</span>
        </Link>

        {/* Coin Balance Pill (1 290 0000 +) */}
        <div className="flex items-center bg-[#17181e] border border-white/5 rounded-full pl-2 pr-1.5 py-1 text-xs gap-2 shadow-inner">
          <div
            className={`w-5 h-5 rounded-full bg-gradient-to-br from-amber-300 to-amber-600 border border-amber-200 flex items-center justify-center shadow-md ${
              coinBurst ? 'scale-125 rotate-180 transition-transform duration-300' : ''
            }`}
          >
            <span className="text-[11px] font-black text-amber-950 leading-none">★</span>
          </div>

          <span className="font-bold text-[12px] sm:text-[13px] text-white tracking-wide">
            {coins.toLocaleString().replace(/,/g, ' ')}
          </span>

          <button
            onClick={onAddCoins}
            className="w-5 h-5 rounded-full bg-[#2563eb] hover:bg-[#1d4ed8] text-white flex items-center justify-center transition transform active:scale-90"
            title="Claim +50 000 Coins"
          >
            <Plus className="w-3.5 h-3.5 stroke-[3]" />
          </button>
        </div>

        {/* User Profile Avatar Pill with Adventure Cowboy Hat */}
        <div className="relative cursor-pointer group" title="Logged in as Adventurer">
          <div className="w-9 h-9 rounded-full overflow-hidden border border-white/20 ring-2 ring-transparent group-hover:ring-sky-400 transition shadow-md">
            <Image
              src="/games/avatar.jpg"
              alt="Profile Avatar"
              width={36}
              height={36}
              className="w-full h-full object-cover"
            />
          </div>
          <span className="absolute bottom-0 right-0 w-2.5 h-2.5 bg-emerald-400 border-2 border-[#0c0d12] rounded-full" />
        </div>
      </div>
    </header>
  );
}
