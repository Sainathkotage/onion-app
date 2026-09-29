const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export interface UploadResponse {
  upload_id: string;
  filename: string;
  original_filename: string;
  width: number;
  height: number;
  format: string;
  status: string;
  access_url: string;
}

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
}

export interface CalibrationInfo {
  status: 'calibrated' | 'not_calibrated';
  is_calibrated: boolean;
  pixels_per_mm: number | null;
  reference_width_mm: number;
  marker_id?: number | null;
  marker_side_pixels?: number | null;
  marker_center?: [number, number] | null;
  marker_corners?: [number, number][] | null;
  distortion_ratio?: number | null;
  perspective_warning?: string | null;
  message: string;
}

export interface SizeInfo {
  physical_diameter_mm: number | null;
  diameter_pixels: number;
  size_category: string; // e.g. "Small", "Medium", "Large" or "Small (Relative)"
  relative_size: 'small' | 'medium' | 'large';
  is_undersized: boolean;
  measurement_status: 'calibrated' | 'unavailable';
  size_reason: string;
  scale_pixels_per_mm?: number | null;
}

export interface OnionDetectionItem {
  id: number;
  label: string;
  bbox: [number, number, number, number];
  confidence: number;
  crop_path: string;
  area: number;
  center: [number, number];
  size?: SizeInfo;
}

export interface DetectionResult {
  upload_id: string;
  total_onions: number;
  annotated_image_url: string;
  onions: OnionDetectionItem[];
  detector_used: string;
  calibration?: CalibrationInfo;
  status: string;
}

export interface OnionClassificationItem {
  onion_id: number;
  label: string;
  class_label: 'Healthy' | 'Damaged' | 'Rotten' | 'Sprouted' | 'Undersized';
  confidence: number;
  probabilities: Record<string, number>;
  crop_path: string;
  is_defective: boolean;
  defect_reason?: string;
  size?: SizeInfo;
}

export interface BatchClassificationResult {
  upload_id: string;
  total_onions: number;
  classifications: OnionClassificationItem[];
  classifier_used: string;
  is_demo_mode: boolean;
  calibration?: CalibrationInfo;
  status: string;
}

export interface CountPercentage {
  count: number;
  percentage: number;
}

export interface BreakdownDetail {
  healthy: CountPercentage;
  damaged: CountPercentage;
  rotten: CountPercentage;
  sprouted: CountPercentage;
  undersized: CountPercentage;
}

export interface SizeCategoryBreakdown {
  small: CountPercentage;
  medium: CountPercentage;
  large: CountPercentage;
  mean_diameter_mm?: number | null;
}

export interface BatchGradingResult {
  batch_id: string;
  timestamp: string;
  total_onions: number;
  grade_a: CountPercentage;
  urs: CountPercentage;
  breakdown: BreakdownDetail;
  size_breakdown?: SizeCategoryBreakdown;
  grading_status?: 'calibrated' | 'uncalibrated_relative';
  calibration?: CalibrationInfo;
  recommendation: string;
  quality_summary?: string;
  ai_engine?: string;
  status: string;
}

export interface PdfReportResponse {
  batch_id: string;
  upload_id: string;
  timestamp: string;
  pdf_report_url: string;
  status: string;
}

export async function checkHealth(): Promise<HealthResponse> {
  const res = await fetch(`${API_BASE_URL}/health`);
  if (!res.ok) {
    throw new Error(`Health check failed: ${res.statusText}`);
  }
  return res.json();
}

export async function uploadImage(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE_URL}/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: 'Upload failed' }));
    throw new Error(errorData.detail || 'Failed to upload image');
  }

  return res.json();
}

export async function detectOnions(upload_id: string, filename: string): Promise<DetectionResult> {
  const res = await fetch(`${API_BASE_URL}/analyze/detect`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ upload_id, filename }),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: 'Detection failed' }));
    throw new Error(errorData.detail || 'Failed to perform onion detection');
  }

  return res.json();
}

export async function classifyOnions(
  upload_id: string,
  onions: OnionDetectionItem[],
  calibration?: CalibrationInfo
): Promise<BatchClassificationResult> {
  const res = await fetch(`${API_BASE_URL}/analyze/classify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ upload_id, onions, calibration }),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: 'Classification failed' }));
    throw new Error(errorData.detail || 'Failed to perform defect classification');
  }

  return res.json();
}

export async function gradeBatch(
  upload_id: string,
  classifications: OnionClassificationItem[],
  calibration?: CalibrationInfo
): Promise<BatchGradingResult> {
  const res = await fetch(`${API_BASE_URL}/analyze/grade`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ upload_id, classifications, calibration }),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: 'Grading calculation failed' }));
    throw new Error(errorData.detail || 'Failed to calculate batch grading');
  }

  return res.json();
}

export async function generatePdfReport(
  upload_id: string,
  grading: BatchGradingResult,
  classifications: OnionClassificationItem[],
  annotated_image_url: string
): Promise<PdfReportResponse> {
  const res = await fetch(`${API_BASE_URL}/reports/pdf`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      upload_id,
      grading,
      classifications,
      annotated_image_url,
    }),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: 'PDF generation failed' }));
    throw new Error(errorData.detail || 'Failed to generate PDF quality report');
  }

  return res.json();
}
