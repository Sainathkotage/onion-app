'use client';

import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Camera, Image as ImageIcon, AlertCircle, X, RefreshCw, Sparkles } from 'lucide-react';

interface ImageUploaderProps {
  onImageSelected: (file: File) => void;
}

export default function ImageUploader({ onImageSelected }: ImageUploaderProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Live Camera state
  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [cameraFacingMode, setCameraFacingMode] = useState<'environment' | 'user'>('environment');
  const [cameraLoading, setCameraLoading] = useState(false);
  const [cameraError, setCameraError] = useState<string | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const cameraInputRef = useRef<HTMLInputElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const mediaStreamRef = useRef<MediaStream | null>(null);

  const stopCameraStream = useCallback(() => {
    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach((track) => track.stop());
      mediaStreamRef.current = null;
    }
  }, []);

  const openCamera = async () => {
    setErrorMessage(null);
    setCameraError(null);

    // Check if mediaDevices and getUserMedia are supported
    if (!navigator?.mediaDevices?.getUserMedia) {
      // Fallback directly to native capture input
      cameraInputRef.current?.click();
      return;
    }

    setIsCameraOpen(true);
    setCameraLoading(true);

    try {
      stopCameraStream();
      const constraints: MediaStreamConstraints = {
        video: {
          facingMode: cameraFacingMode,
          width: { ideal: 1920 },
          height: { ideal: 1080 },
        },
        audio: false,
      };

      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      mediaStreamRef.current = stream;

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }
    } catch (err: any) {
      console.warn('Live camera access error:', err);
      // Try fallback to user facing mode if environment mode failed
      if (cameraFacingMode === 'environment') {
        try {
          const fallbackStream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false,
          });
          mediaStreamRef.current = fallbackStream;
          if (videoRef.current) {
            videoRef.current.srcObject = fallbackStream;
            await videoRef.current.play();
          }
          setCameraLoading(false);
          return;
        } catch {
          // Both failed
        }
      }

      setCameraError(
        err.name === 'NotAllowedError'
          ? 'Camera permission denied. Please allow camera access in browser settings or use file upload.'
          : 'Unable to start camera stream. You can capture using the device file picker instead.'
      );
    } finally {
      setCameraLoading(false);
    }
  };

  const closeCamera = () => {
    stopCameraStream();
    setIsCameraOpen(false);
    setCameraError(null);
  };

  const switchCamera = () => {
    const nextMode = cameraFacingMode === 'environment' ? 'user' : 'environment';
    setCameraFacingMode(nextMode);
  };

  // Re-run camera when facing mode toggles
  useEffect(() => {
    if (isCameraOpen) {
      openCamera();
    }
    return () => {
      stopCameraStream();
    };
  }, [cameraFacingMode]);

  // Clean up stream on unmount
  useEffect(() => {
    return () => {
      stopCameraStream();
    };
  }, [stopCameraStream]);

  const capturePhoto = () => {
    if (!videoRef.current) return;
    const video = videoRef.current;

    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || 1280;
    canvas.height = video.videoHeight || 720;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(
      (blob) => {
        if (!blob) {
          setErrorMessage('Failed to capture photo frame from camera.');
          return;
        }
        const capturedFile = new File([blob], `camera_capture_${Date.now()}.jpg`, {
          type: 'image/jpeg',
          lastModified: Date.now(),
        });
        closeCamera();
        validateAndSelect(capturedFile);
      },
      'image/jpeg',
      0.95
    );
  };

  const validateAndSelect = (file: File) => {
    setErrorMessage(null);

    // Check empty file
    if (!file || file.size === 0) {
      setErrorMessage('The selected file is empty (0 bytes). Please choose a valid image.');
      return;
    }

    // Format validation
    const validMimeTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/bmp'];
    const validExtensions = ['.jpg', '.jpeg', '.png', '.webp', '.bmp'];
    const fileExt = file.name ? '.' + file.name.split('.').pop()?.toLowerCase() : '';

    const isValidFormat =
      validMimeTypes.includes(file.type.toLowerCase()) || validExtensions.includes(fileExt);

    if (!isValidFormat) {
      setErrorMessage('Unsupported format. Please upload JPG, PNG, WEBP, or BMP images.');
      return;
    }

    // File size validation (20MB)
    const maxSizeMB = 20;
    if (file.size > maxSizeMB * 1024 * 1024) {
      setErrorMessage(`Image size (${(file.size / (1024 * 1024)).toFixed(1)}MB) exceeds maximum limit of ${maxSizeMB}MB.`);
      return;
    }

    onImageSelected(file);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSelect(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSelect(e.target.files[0]);
    }
  };

  return (
    <div className="w-full space-y-4">
      {/* Live Camera Viewfinder Modal */}
      {isCameraOpen && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-[#1B1B20] border border-white/10 rounded-3xl max-w-2xl w-full overflow-hidden shadow-2xl flex flex-col animate-fadeIn">
            {/* Camera Header */}
            <div className="bg-[#151518] px-5 py-3.5 border-b border-white/10 flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Camera className="w-4 h-4 text-[#7CFF6B]" />
                <span className="text-sm font-bold text-white">Live Camera Viewfinder</span>
              </div>
              <button
                onClick={closeCamera}
                className="p-1 rounded-xl text-[#A7A7B0] hover:text-white hover:bg-white/10 transition"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Viewfinder Frame */}
            <div className="relative bg-[#0B0B0D] flex items-center justify-center min-h-[320px] max-h-[500px] overflow-hidden">
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className="w-full h-full max-h-[460px] object-cover"
              />

              {/* Viewfinder Target Framing Guide */}
              <div className="absolute inset-8 border-2 border-dashed border-[#7CFF6B]/40 rounded-2xl pointer-events-none flex items-center justify-center">
                <div className="text-center bg-black/50 backdrop-blur-sm px-3 py-1 rounded-xl border border-white/10 text-[11px] text-[#A7A7B0]">
                  Frame onions/tray inside guideline
                </div>
              </div>

              {cameraLoading && (
                <div className="absolute inset-0 bg-[#0B0B0D]/90 flex items-center justify-center text-white text-xs space-x-2">
                  <RefreshCw className="w-4 h-4 animate-spin text-[#7CFF6B]" />
                  <span>Connecting to camera...</span>
                </div>
              )}

              {cameraError && (
                <div className="absolute inset-0 bg-[#0B0B0D]/95 p-6 flex flex-col items-center justify-center text-center space-y-3">
                  <AlertCircle className="w-8 h-8 text-[#FF5C5C]" />
                  <p className="text-xs text-[#FF5C5C] max-w-sm">{cameraError}</p>
                  <button
                    onClick={() => {
                      closeCamera();
                      cameraInputRef.current?.click();
                    }}
                    className="px-4 py-2 bg-white/10 hover:bg-white/20 text-white font-bold rounded-xl text-xs transition"
                  >
                    Use Device File Picker
                  </button>
                </div>
              )}
            </div>

            {/* Camera Controls Footer */}
            <div className="p-4 bg-[#151518] border-t border-white/10 flex items-center justify-between">
              <button
                type="button"
                onClick={switchCamera}
                disabled={cameraLoading}
                className="px-3 py-2 bg-white/5 hover:bg-white/10 text-white rounded-xl text-xs font-bold transition flex items-center space-x-1.5"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>Flip Camera</span>
              </button>

              <button
                type="button"
                onClick={capturePhoto}
                disabled={cameraLoading || Boolean(cameraError)}
                className="px-6 py-3 bg-[#7CFF6B] hover:bg-[#6be65b] text-[#0B0B0D] font-extrabold rounded-2xl shadow-xl glow-accent transition flex items-center space-x-2 text-xs disabled:opacity-50"
              >
                <Camera className="w-4 h-4 text-[#0B0B0D]" />
                <span>Capture Photo</span>
              </button>

              <button
                type="button"
                onClick={closeCamera}
                className="px-3 py-2 text-[#A7A7B0] hover:text-white text-xs font-bold transition"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Main Drag-and-Drop Area */}
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`relative border-2 border-dashed rounded-3xl p-6 sm:p-8 text-center transition-all duration-200 cursor-pointer ${
          isDragging
            ? 'border-[#7CFF6B] bg-[#7CFF6B]/10 scale-[1.01]'
            : 'border-white/15 hover:border-[#7CFF6B]/50 bg-[#1B1B20] hover:bg-[#151518] shadow-2xl'
        }`}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept="image/jpeg,image/png,image/webp,image/bmp"
          className="hidden"
        />

        {/* Native mobile camera capture fallback input */}
        <input
          type="file"
          ref={cameraInputRef}
          onChange={handleFileChange}
          accept="image/*"
          capture="environment"
          className="hidden"
        />

        <div className="flex flex-col items-center justify-center space-y-4">
          <div className="w-16 h-16 rounded-2xl bg-[#7CFF6B]/15 text-[#7CFF6B] flex items-center justify-center border border-[#7CFF6B]/30 shadow-lg glow-accent">
            <Camera className="w-8 h-8" />
          </div>

          <div>
            <h3 className="text-xl font-black text-white tracking-tight">
              Capture Batch Image
            </h3>
            <p className="text-xs text-[#A7A7B0] mt-1 max-w-sm mx-auto leading-relaxed">
              Place onions in a well-lit area and keep the tray visible. Snap via camera or select an image file.
            </p>
          </div>

          {/* Action Buttons */}
          <div
            className="flex flex-col sm:flex-row items-center gap-3 pt-2 w-full max-w-xs"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              type="button"
              onClick={openCamera}
              className="w-full py-3 bg-[#7CFF6B] hover:bg-[#6be65b] text-[#0B0B0D] font-extrabold rounded-2xl shadow-xl glow-accent transition flex items-center justify-center space-x-2 text-xs"
            >
              <Camera className="w-4 h-4 text-[#0B0B0D]" />
              <span>Take Photo</span>
            </button>

            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="w-full py-3 bg-[#151518] hover:bg-white/10 text-white font-bold rounded-2xl border border-white/10 transition flex items-center justify-center space-x-2 text-xs"
            >
              <ImageIcon className="w-4 h-4 text-[#A7A7B0]" />
              <span>Upload Image</span>
            </button>
          </div>

          {/* Reference Marker Calibration Notice */}
          <div className="bg-[#151518] border border-white/10 rounded-xl px-4 py-2.5 max-w-sm text-left flex items-start space-x-2.5 text-[11px] text-[#A7A7B0]">
            <span className="text-[#7CFF6B] text-base leading-none">📐</span>
            <div>
              <p className="font-bold text-white">Scale Calibration Notice</p>
              <p className="text-[10px] text-[#A7A7B0] mt-0.5">
                Place a <strong>50mm ArUco marker</strong> inside the frame for calibrated physical diameter (mm). Without a marker, relative size estimation will be used.
              </p>
            </div>
          </div>

          <p className="text-[11px] text-[#A7A7B0] font-medium">
            Supported formats: JPG, PNG, WEBP, BMP (Max 20MB)
          </p>
        </div>
      </div>

      {errorMessage && (
        <div className="p-4 bg-[#FF5C5C]/15 border border-[#FF5C5C]/30 rounded-2xl flex items-start space-x-3 text-[#FF5C5C] text-xs animate-fadeIn">
          <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <p className="font-bold">Upload Error</p>
            <p className="text-[#FF5C5C]/90 mt-0.5">{errorMessage}</p>
          </div>
          <button
            onClick={() => setErrorMessage(null)}
            className="text-[#FF5C5C] hover:text-white transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      )}
    </div>
  );
}

