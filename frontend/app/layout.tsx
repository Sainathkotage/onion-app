import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Fun Games — Nintendo Switch™',
  description: 'Explore the curated selection of Nintendo Switch games, exclusive access, ratings, and digital store downloads.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#2c2d35] text-white min-h-screen font-sans antialiased selection:bg-[#ff3b3b]/30 selection:text-white">
        {children}
      </body>
    </html>
  );
}
