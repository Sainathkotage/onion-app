'use client';

import React, { useState } from 'react';
import Image from 'next/image';
import { User, Play, Gamepad2, SlidersHorizontal } from 'lucide-react';
import { GameItem, GAMES_DATA } from './types';
import { playSwitchSound } from './audio';

interface GameCardsDeckProps {
  onSelectGame: (game: GameItem) => void;
  onOpenAllGames: () => void;
  soundEnabled: boolean;
}

export default function GameCardsDeck({
  onSelectGame,
  onOpenAllGames,
  soundEnabled,
}: GameCardsDeckProps) {
  const [activeCardIndex, setActiveCardIndex] = useState<number>(2); // Kirby starts centered
  const [hoveredCardIndex, setHoveredCardIndex] = useState<number | null>(null);

  const handleCardClick = (index: number) => {
    setActiveCardIndex(index);
    playSwitchSound('select', soundEnabled);
    onSelectGame(GAMES_DATA[index]);
  };

  const getCardTransform = (index: number) => {
    const isHovered = hoveredCardIndex === index;
    const isCenter = index === 2;

    const angles: Record<number, number> = {
      0: -15,
      1: -7,
      2: 0,
      3: 7,
      4: 15,
    };

    const translateY: Record<number, number> = {
      0: 24,
      1: 10,
      2: -14,
      3: 10,
      4: 24,
    };

    const translateX: Record<number, number> = {
      0: -24,
      1: -12,
      2: 0,
      3: 12,
      4: 24,
    };

    const zIndices: Record<number, number> = {
      0: 10,
      1: 20,
      2: 30,
      3: 20,
      4: 10,
    };

    if (isHovered) {
      return {
        transform: 'translateY(-36px) scale(1.08) rotate(0deg)',
        zIndex: 50,
      };
    }

    return {
      transform: `translateX(${translateX[index]}px) translateY(${translateY[index]}px) rotate(${angles[index]}deg) scale(${
        isCenter ? 1.05 : 0.98
      })`,
      zIndex: zIndices[index],
    };
  };

  return (
    <div className="w-full max-w-5xl mx-auto mt-8 md:mt-10 mb-4 select-none relative z-20 flex flex-col items-center">
      {/* 5-Card Fanned Container */}
      <div className="w-full flex items-end justify-center gap-2 sm:gap-3 md:gap-4 relative pt-16 pb-6 overflow-x-auto sm:overflow-visible no-scrollbar px-2">
        {GAMES_DATA.map((game, index) => {
          const isCenter = index === 2;
          const isHovered = hoveredCardIndex === index;
          const fanStyle = getCardTransform(index);

          return (
            <div
              key={game.id}
              style={{
                transform: fanStyle.transform,
                zIndex: fanStyle.zIndex,
              }}
              onMouseEnter={() => {
                setHoveredCardIndex(index);
                playSwitchSound('woosh', soundEnabled);
              }}
              onMouseLeave={() => setHoveredCardIndex(null)}
              onClick={() => handleCardClick(index)}
              className={`card-3d-wrapper shrink-0 relative w-[135px] sm:w-[170px] md:w-[195px] h-[215px] sm:h-[260px] md:h-[290px] rounded-[24px] sm:rounded-[30px] cursor-pointer bg-gradient-to-b ${
                game.gradient
              } p-4 flex flex-col justify-between shadow-2xl select-none group ${
                isCenter && hoveredCardIndex === null ? game.glowClass : ''
              }`}
            >
              {/* Character Pop-out 3D Figure */}
              <div
                className={`absolute pointer-events-none transition-transform duration-300 ${
                  game.characterOffset
                } ${
                  isHovered || (isCenter && hoveredCardIndex === null)
                    ? 'scale-110 -translate-y-2'
                    : 'scale-100'
                }`}
              >
                <Image
                  src={game.characterImg}
                  alt={game.characterAlt}
                  fill
                  className="object-contain filter drop-shadow-[0_14px_20px_rgba(0,0,0,0.6)]"
                  priority
                />
              </div>

              {/* Card Top: Title & Rating Badge */}
              <div className="relative z-10 flex items-start justify-between">
                <div>
                  <h3 className="font-black text-sm sm:text-base md:text-lg text-white leading-tight drop-shadow-sm">
                    {game.title}
                  </h3>
                  <p className="text-[10px] sm:text-xs text-white/80 font-medium tracking-tight">
                    {game.subtitle}
                  </p>
                </div>

                {/* Rating badge */}
                <div className="flex items-center gap-1 bg-black/25 backdrop-blur-md px-2 py-0.5 rounded-full border border-white/20 text-[10px] sm:text-xs font-bold text-white shadow-sm">
                  <User className="w-2.5 h-2.5 sm:w-3 sm:h-3 fill-white/80 text-white/80" />
                  <span>{game.rating}</span>
                </div>
              </div>

              {/* Card Bottom: Genre & Action Icon */}
              <div className="relative z-10 pt-2 flex items-center justify-between">
                <span className="text-[10px] font-bold uppercase tracking-wider text-white/80 bg-black/20 px-2 py-0.5 rounded-md backdrop-blur-xs">
                  {game.category.split(' ')[0]}
                </span>

                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleCardClick(index);
                  }}
                  className="opacity-0 group-hover:opacity-100 transition-opacity bg-white text-neutral-900 rounded-full p-1.5 shadow-lg hover:scale-110 active:scale-95"
                  title="View Game Details"
                >
                  <Play className="w-3 h-3 fill-neutral-900 ml-0.5" />
                </button>
              </div>

              {/* Card Outer Bezel Highlight */}
              <div className="absolute inset-0 rounded-[24px] sm:rounded-[30px] border border-white/25 pointer-events-none" />
            </div>
          );
        })}
      </div>

      {/* Action Footer Buttons */}
      <div className="w-full flex items-center justify-center gap-3 pt-2 pb-3 relative z-30">
        <button
          onClick={() => {
            onSelectGame(GAMES_DATA[activeCardIndex]);
            playSwitchSound('select', soundEnabled);
          }}
          className="px-6 py-2.5 bg-white text-neutral-950 font-black text-xs sm:text-sm rounded-full shadow-lg hover:bg-neutral-200 transition transform active:scale-95 flex items-center gap-2"
        >
          <Gamepad2 className="w-4 h-4 text-neutral-900" />
          <span>Explore {GAMES_DATA[activeCardIndex].title}</span>
        </button>

        <button
          onClick={() => {
            onOpenAllGames();
            playSwitchSound('click', soundEnabled);
          }}
          className="px-4 py-2.5 bg-[#17181e] text-white font-bold text-xs sm:text-sm rounded-full border border-white/10 hover:border-white/25 transition flex items-center gap-2"
        >
          <SlidersHorizontal className="w-3.5 h-3.5 text-neutral-400" />
          <span>All Games ({GAMES_DATA.length})</span>
        </button>
      </div>
    </div>
  );
}
