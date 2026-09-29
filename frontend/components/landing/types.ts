export interface GameItem {
  id: string;
  title: string;
  subtitle: string;
  rating: string;
  reviewsCount: string;
  gradient: string;
  glowClass: string;
  accentColor: string;
  characterImg: string;
  characterAlt: string;
  characterOffset: string;
  category: string;
  price: string;
  discountPrice?: string;
  storageSize: string;
  players: string;
  description: string;
  features: string[];
}

export const GAMES_DATA: GameItem[] = [
  {
    id: 'fortnite',
    title: 'Fortnite',
    subtitle: 'Battle Royale',
    rating: '4,8',
    reviewsCount: '2.4M',
    gradient: 'from-[#8b5cf6] via-[#7c3aed] to-[#5b21b6]',
    glowClass: 'glow-card-fortnite',
    accentColor: '#8b5cf6',
    characterImg: '/games/fortnite.png',
    characterAlt: 'Fortnite Raven Character',
    characterOffset: '-top-14 left-1/2 -translate-x-1/2 w-44 h-48',
    category: 'Battle Royale',
    price: 'Free to Play',
    storageSize: '18.4 GB',
    players: '1 - 100 Players',
    description:
      'Jump from the Battle Bus, scavenge for weapons, build tactical shelters, and outlast 99 opponents to achieve Victory Royale in this ever-evolving world.',
    features: ['Cross-Platform Play', 'Zero Build Mode', 'HD Rumble', 'Weekly Live Events'],
  },
  {
    id: 'mario',
    title: 'Mario',
    subtitle: 'Kingdom Battle',
    rating: '4,9',
    reviewsCount: '940K',
    gradient: 'from-[#ff4d4d] via-[#ef4444] to-[#b91c1c]',
    glowClass: 'glow-card-mario',
    accentColor: '#ef4444',
    characterImg: '/games/mario.png',
    characterAlt: 'Super Mario',
    characterOffset: '-top-16 left-1/2 -translate-x-1/2 w-44 h-48',
    category: 'Action Adventure',
    price: '$59.99',
    discountPrice: 'Free with Access',
    storageSize: '6.2 GB',
    players: '1 - 2 Players',
    description:
      'Mario teams up with heroic Rabbids to restore peace to the Mushroom Kingdom in a hilarious, dynamic turn-based tactical adventure packed with wacky blasters.',
    features: ['Turn-based Combat', 'Co-op Challenges', 'Joy-Con Motion Support', 'Amiibo Compatible'],
  },
  {
    id: 'kirby',
    title: 'Kirby',
    subtitle: 'Star Allies',
    rating: '4,7',
    reviewsCount: '1.2M',
    gradient: 'from-[#38bdf8] via-[#0284c7] to-[#0369a1]',
    glowClass: 'glow-card-kirby',
    accentColor: '#38bdf8',
    characterImg: '/games/kirby.png',
    characterAlt: 'Kirby Character',
    characterOffset: '-top-14 left-1/2 -translate-x-1/2 w-48 h-52',
    category: 'Platformer',
    price: '$59.99',
    discountPrice: 'Free with Access',
    storageSize: '4.0 GB',
    players: '1 - 4 Players',
    description:
      'Kirby is back and bringing friends along! Throw Friend Hearts to charm enemies into loyal allies, combine elemental copy abilities, and save Planet Popstar.',
    features: ['4-Player Drop-in Co-op', 'Friend Combos', 'Full Joy-Con Sharing', 'Guest Star Mode'],
  },
  {
    id: 'pokemon',
    title: 'Pokemon',
    subtitle: 'Legends Arceus',
    rating: '4,2',
    reviewsCount: '3.1M',
    gradient: 'from-[#2dd4bf] via-[#0d9488] to-[#115e59]',
    glowClass: 'glow-card-pokemon',
    accentColor: '#2dd4bf',
    characterImg: '/games/bulbasaur.png',
    characterAlt: 'Bulbasaur',
    characterOffset: '-top-12 left-1/2 -translate-x-1/2 w-40 h-44',
    category: 'Action RPG',
    price: '$59.99',
    discountPrice: 'Included in Pass',
    storageSize: '6.1 GB',
    players: '1 Player',
    description:
      'Explore the ancient, untamed Hisui region. Sneak up on wild Pokémon, study their behavioral patterns, aim your Poké Balls, and create the region’s first Pokédex.',
    features: ['Action RPG Mechanics', 'Semi-Open World', 'Agile & Strong Styles', 'Cloud Saves'],
  },
  {
    id: 'splatoon',
    title: 'Splatoon 3',
    subtitle: 'Multiplayer',
    rating: '3,9',
    reviewsCount: '870K',
    gradient: 'from-[#3b82f6] via-[#2563eb] to-[#1e40af]',
    glowClass: 'glow-card-splatoon',
    accentColor: '#3b82f6',
    characterImg: '/games/inkling.png',
    characterAlt: 'Splatoon Inkling Girl',
    characterOffset: '-top-14 left-1/2 -translate-x-1/2 w-44 h-48',
    category: 'Multiplayer Shooter',
    price: '$59.99',
    discountPrice: 'Season Pass Included',
    storageSize: '5.5 GB',
    players: '1 - 8 Players Online',
    description:
      'Claim your turf in dynamic 4-on-4 ink-splatting battles! Equip fresh weapons, customize your locker, dance through 3-team Splatfests, and conquer Salmon Run Next Wave.',
    features: ['4v4 Turf War', 'Salmon Run Next Wave', 'Gyro Aiming Support', 'Tableturf Battle'],
  },
];
