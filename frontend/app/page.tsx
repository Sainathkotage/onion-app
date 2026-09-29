'use client';

import React, { useState } from 'react';
import Navbar from '@/components/landing/Navbar';
import HeroSection from '@/components/landing/HeroSection';
import GameCardsDeck from '@/components/landing/GameCardsDeck';
import GameModal from '@/components/landing/GameModal';
import FilterModal from '@/components/landing/FilterModal';
import { GameItem, GAMES_DATA } from '@/components/landing/types';
import { playSwitchSound } from '@/components/landing/audio';

export default function NintendoSwitchPage() {
  const [activeTab, setActiveTab] = useState<'games' | 'store'>('games');
  const [searchQuery, setSearchQuery] = useState('');
  const [coins, setCoins] = useState<number>(12900000);
  const [coinBurst, setCoinBurst] = useState(false);
  const [cartCount, setCartCount] = useState(1);
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [selectedGame, setSelectedGame] = useState<GameItem | null>(null);
  const [filterModalOpen, setFilterModalOpen] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [isFramedMode, setIsFramedMode] = useState(true);

  const handleAddCoins = () => {
    playSwitchSound('coin', soundEnabled);
    setCoins((prev) => prev + 50000);
    setCoinBurst(true);
    setTimeout(() => setCoinBurst(false), 1200);
  };

  const handleAddToCart = () => {
    setCartCount((prev) => prev + 1);
  };

  const filteredGames = GAMES_DATA.filter((game) => {
    const matchesSearch =
      game.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      game.subtitle.toLowerCase().includes(searchQuery.toLowerCase()) ||
      game.category.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCat = selectedCategory === 'All' || game.category.includes(selectedCategory);
    return matchesSearch && matchesCat;
  });

  return (
    <div
      className={`min-h-screen transition-colors duration-500 font-sans flex items-center justify-center p-2 sm:p-4 md:p-8 ${
        isFramedMode ? 'bg-[#3b3d48]' : 'bg-[#0c0d12] p-0'
      }`}
    >
      {/* Tablet Device Frame Shell (Exact Mockup Container) */}
      <div
        className={`w-full max-w-[1240px] bg-[#0c0d12] text-white overflow-hidden relative shadow-[0_35px_80px_-15px_rgba(0,0,0,0.85)] border border-white/10 flex flex-col justify-between transition-all duration-300 ${
          isFramedMode
            ? 'rounded-[32px] sm:rounded-[44px] min-h-[720px]'
            : 'rounded-none min-h-screen border-none'
        }`}
      >
        {/* Subtle Dark Square Grid Pattern */}
        <div className="absolute inset-0 switch-bg-pattern opacity-90 pointer-events-none" />

        {/* Ambient Glows */}
        <div className="absolute -top-40 left-1/2 -translate-x-1/2 w-[700px] h-[300px] bg-sky-500/10 rounded-full blur-[120px] pointer-events-none" />
        <div className="absolute -bottom-32 left-1/2 -translate-x-1/2 w-[800px] h-[350px] bg-blue-600/15 rounded-full blur-[140px] pointer-events-none" />

        {/* 1. Top Navigation Bar */}
        <Navbar
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          coins={coins}
          onAddCoins={handleAddCoins}
          coinBurst={coinBurst}
          cartCount={cartCount}
          soundEnabled={soundEnabled}
          setSoundEnabled={setSoundEnabled}
          onOpenFilter={() => setFilterModalOpen(true)}
          isFramedMode={isFramedMode}
          setIsFramedMode={setIsFramedMode}
        />

        {/* 2. Hero Section & Fanned Cards Deck */}
        <main className="relative z-20 flex-1 flex flex-col items-center justify-between pt-6 pb-2 px-4 sm:px-8 overflow-hidden">
          <HeroSection />

          <GameCardsDeck
            onSelectGame={(game) => setSelectedGame(game)}
            onOpenAllGames={() => setFilterModalOpen(true)}
            soundEnabled={soundEnabled}
          />
        </main>
      </div>

      {/* 3. Interactive Modals */}
      <GameModal
        game={selectedGame}
        onClose={() => setSelectedGame(null)}
        onAddToCart={handleAddToCart}
        soundEnabled={soundEnabled}
      />

      <FilterModal
        isOpen={filterModalOpen}
        onClose={() => setFilterModalOpen(false)}
        selectedCategory={selectedCategory}
        setSelectedCategory={setSelectedCategory}
        filteredGames={filteredGames}
        onSelectGame={(game) => setSelectedGame(game)}
        soundEnabled={soundEnabled}
      />
    </div>
  );
}
