'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  Download,
  Smartphone,
  CheckCircle2,
  Share2,
  Copy,
  ExternalLink,
  ShieldCheck,
  Cpu,
  Layers,
  Sparkles,
  ArrowLeft,
  ChevronRight,
  AlertCircle
} from 'lucide-react';

export default function AppDownloadPage() {
  const [copied, setCopied] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState('/downloads/onion-iq.apk');
  const [qrCodeUrl, setQrCodeUrl] = useState('');
  const [isDownloading, setIsDownloading] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const fullUrl = `${window.location.origin}/downloads/onion-iq.apk`;
      setDownloadUrl(fullUrl);
      const encoded = encodeURIComponent(fullUrl);
      setQrCodeUrl(`https://api.qrserver.com/v1/create-qr-code/?size=300x300&color=0-0-0&bgcolor=ffffff&data=${encoded}`);
    }
  }, []);

  const handleCopyLink = () => {
    navigator.clipboard.writeText(downloadUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  const handleDownloadClick = () => {
    setIsDownloading(true);
    setTimeout(() => setIsDownloading(false), 3000);
  };

  return (
    <div className="min-h-screen bg-[#090a0f] text-white flex flex-col justify-between selection:bg-emerald-500/30 selection:text-emerald-200 relative overflow-hidden">
      {/* Background Ambient Lighting */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[850px] h-[350px] bg-gradient-to-b from-emerald-600/15 via-teal-500/10 to-transparent rounded-full blur-[140px] pointer-events-none" />
      <div className="absolute bottom-0 right-10 w-[550px] h-[300px] bg-blue-600/10 rounded-full blur-[120px] pointer-events-none" />

      {/* Top Header */}
      <header className="relative z-20 max-w-6xl w-full mx-auto px-6 py-6 flex items-center justify-between">
        <Link
          href="/"
          className="flex items-center gap-2 text-neutral-400 hover:text-white transition text-sm font-medium group"
        >
          <div className="w-8 h-8 rounded-full bg-white/5 border border-white/10 flex items-center justify-center group-hover:bg-white/10 transition">
            <ArrowLeft className="w-4 h-4" />
          </div>
          <span>Back to Home</span>
        </Link>

        <div className="flex items-center gap-3">
          <Link
            href="/analyze"
            className="text-xs px-3.5 py-1.5 rounded-full bg-white/5 border border-white/10 hover:border-white/20 text-neutral-300 hover:text-white transition hidden sm:inline-flex items-center gap-1.5"
          >
            <span>Launch Web Assessor</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </header>

      {/* Main Content Hero */}
      <main className="relative z-10 max-w-5xl w-full mx-auto px-6 py-6 flex-1 flex flex-col justify-center">
        <div className="bg-[#12141c]/90 backdrop-blur-2xl border border-white/10 rounded-[32px] p-6 sm:p-10 shadow-[0_30px_70px_rgba(0,0,0,0.8)]">
          {/* Badge & Title */}
          <div className="text-center max-w-2xl mx-auto space-y-3 mb-10">
            <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/25 text-emerald-400 text-xs font-semibold shadow-sm">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
              <span>Official Android Release • Version 1.0.0</span>
            </div>

            <h1 className="text-3xl sm:text-5xl font-black tracking-tight bg-gradient-to-r from-white via-neutral-100 to-neutral-400 bg-clip-text text-transparent">
              Download OnionIQ App
            </h1>

            <p className="text-neutral-400 text-sm sm:text-base leading-relaxed">
              Install the mobile assessment tool for instant onion quality diagnostics, multimodal AI defect scanning, and procurement batch certification.
            </p>
          </div>

          {/* Download Center Grid */}
          <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-center mb-10">
            {/* Left Column: Direct Download CTA & Specs */}
            <div className="md:col-span-7 flex flex-col justify-between space-y-6">
              <div className="space-y-4">
                <a
                  href="/downloads/onion-iq.apk"
                  download="onion-iq.apk"
                  onClick={handleDownloadClick}
                  className="w-full flex items-center justify-center gap-3 bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-400 hover:to-emerald-500 text-black font-extrabold text-lg py-4 px-6 rounded-2xl shadow-[0_12px_30px_rgba(16,185,129,0.35)] transition-all transform hover:-translate-y-0.5 active:translate-y-0.5 select-none"
                >
                  <Download className="w-6 h-6 stroke-[2.5]" />
                  <span>{isDownloading ? 'Starting Download...' : 'Download for Android (.APK)'}</span>
                </a>

                <div className="flex items-center justify-between text-xs text-neutral-400 px-2">
                  <span className="flex items-center gap-1.5">
                    <ShieldCheck className="w-4 h-4 text-emerald-400" />
                    Verified Safe & Malware-Free
                  </span>
                  <span>Direct Download • No Registration</span>
                </div>
              </div>

              {/* Technical Specifications Grid */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-white/[0.03] border border-white/5 p-4 rounded-2xl">
                <div>
                  <p className="text-[11px] text-neutral-500 uppercase tracking-wider font-semibold">Format & Size</p>
                  <p className="text-sm font-bold text-white mt-0.5">APK • 142 MB</p>
                </div>
                <div>
                  <p className="text-[11px] text-neutral-500 uppercase tracking-wider font-semibold">OS Version</p>
                  <p className="text-sm font-bold text-white mt-0.5">Android 8.0+</p>
                </div>
                <div>
                  <p className="text-[11px] text-neutral-500 uppercase tracking-wider font-semibold">Architecture</p>
                  <p className="text-sm font-bold text-white mt-0.5">ARM64 / v7a</p>
                </div>
                <div>
                  <p className="text-[11px] text-neutral-500 uppercase tracking-wider font-semibold">AI Engine</p>
                  <p className="text-sm font-bold text-emerald-400 mt-0.5">TFLite + Cloud</p>
                </div>
              </div>

              {/* Share & Copy Link */}
              <div className="flex items-center gap-3">
                <button
                  onClick={handleCopyLink}
                  className="flex-1 flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl bg-white/5 border border-white/10 hover:border-white/20 text-xs font-medium text-neutral-300 hover:text-white transition"
                >
                  {copied ? <CheckCircle2 className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                  <span>{copied ? 'Link Copied to Clipboard!' : 'Copy Direct Download Link'}</span>
                </button>

                <a
                  href="/downloads/onion-iq.apk"
                  target="_blank"
                  rel="noreferrer"
                  className="p-2.5 rounded-xl bg-white/5 border border-white/10 hover:border-white/20 text-neutral-400 hover:text-white transition"
                  title="Open in New Tab"
                >
                  <ExternalLink className="w-4 h-4" />
                </a>
              </div>
            </div>

            {/* Right Column: Scan to Download via QR Code */}
            <div className="md:col-span-5 bg-white/[0.02] border border-white/5 rounded-2xl p-6 flex flex-col items-center text-center">
              <div className="bg-white p-3.5 rounded-2xl shadow-xl border border-white/20 mb-4 transition-transform hover:scale-105 duration-200">
                {qrCodeUrl ? (
                  /* eslint-disable-next-line @next/next/no-img-element */
                  <img
                    src={qrCodeUrl}
                    alt="Scan to Download APK"
                    className="w-36 h-36 rounded-lg block"
                  />
                ) : (
                  <div className="w-36 h-36 bg-neutral-200 animate-pulse rounded-lg" />
                )}
              </div>

              <div className="flex items-center gap-2 text-sm font-bold text-white mb-1">
                <Smartphone className="w-4 h-4 text-emerald-400" />
                <span>Scan to Download on Phone</span>
              </div>
              <p className="text-xs text-neutral-400 max-w-[220px] leading-relaxed">
                Point your smartphone camera at the QR code to begin direct download automatically.
              </p>
            </div>
          </div>

          {/* 3 Step Installation Guide */}
          <div className="border-t border-white/10 pt-8">
            <h2 className="text-sm font-bold uppercase tracking-wider text-neutral-400 mb-5 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-emerald-400" />
              <span>Easy 3-Step Installation Guide</span>
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="bg-white/[0.02] border border-white/5 rounded-2xl p-4 flex gap-3.5 items-start">
                <span className="w-7 h-7 rounded-xl bg-emerald-500/20 text-emerald-400 font-extrabold text-xs flex items-center justify-center shrink-0">
                  1
                </span>
                <div>
                  <h3 className="text-sm font-semibold text-white">Download APK</h3>
                  <p className="text-xs text-neutral-400 mt-1 leading-relaxed">
                    Click the download button or scan the QR code to save <code className="text-emerald-300">onion-iq.apk</code>.
                  </p>
                </div>
              </div>

              <div className="bg-white/[0.02] border border-white/5 rounded-2xl p-4 flex gap-3.5 items-start">
                <span className="w-7 h-7 rounded-xl bg-emerald-500/20 text-emerald-400 font-extrabold text-xs flex items-center justify-center shrink-0">
                  2
                </span>
                <div>
                  <h3 className="text-sm font-semibold text-white">Open the File</h3>
                  <p className="text-xs text-neutral-400 mt-1 leading-relaxed">
                    Tap the notification or find the file in your device&apos;s <strong>Downloads</strong> folder.
                  </p>
                </div>
              </div>

              <div className="bg-white/[0.02] border border-white/5 rounded-2xl p-4 flex gap-3.5 items-start">
                <span className="w-7 h-7 rounded-xl bg-emerald-500/20 text-emerald-400 font-extrabold text-xs flex items-center justify-center shrink-0">
                  3
                </span>
                <div>
                  <h3 className="text-sm font-semibold text-white">Allow & Install</h3>
                  <p className="text-xs text-neutral-400 mt-1 leading-relaxed">
                    If prompted, allow <em>&ldquo;Install unknown apps&rdquo;</em> in Android Settings, then confirm Install.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="relative z-20 max-w-6xl w-full mx-auto px-6 py-6 text-center text-xs text-neutral-500 border-t border-white/5">
        <p>© 2026 OnionIQ Automated Quality Assessor • All rights reserved.</p>
      </footer>
    </div>
  );
}
