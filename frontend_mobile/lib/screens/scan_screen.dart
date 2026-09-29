import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../data/history_repository.dart';
import '../services/api_service.dart';
import '../theme/app_colors.dart';
import '../theme/app_icons.dart';
import '../theme/app_spacing.dart';
import '../theme/app_typography.dart';
import '../widgets/app_button.dart';
import '../widgets/scanning_radar.dart';
import '../widgets/tray_overlay.dart';
import 'analysis_screen.dart';

class ScanScreen extends StatefulWidget {
  const ScanScreen({super.key});

  @override
  State<ScanScreen> createState() => _ScanScreenState();
}

class _ScanScreenState extends State<ScanScreen> {
  File? _image;
  bool _isAnalyzing = false;
  String _analysisStatus = '1/2: Detecting onions with AI & NMS...';
  String _subStatus = 'Local neural model executing bounding segmentation';
  double _analysisProgress = 0.35;
  final ImagePicker _picker = ImagePicker();

  Future<void> _pickImage(ImageSource source) async {
    try {
      final XFile? pickedFile = await _picker.pickImage(
        source: source,
        imageQuality: 92,
        maxWidth: 1600,
      );
      if (pickedFile != null) {
        setState(() {
          _image = File(pickedFile.path);
        });
        _startAnalysis();
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Could not access image: $e')),
      );
    }
  }

  Future<void> _startAnalysis() async {
    if (_image == null) return;

    setState(() {
      _isAnalyzing = true;
      _analysisStatus = '1/2: Detecting onions with AI & NMS...';
      _subStatus = 'Applying Non-Maximum Suppression to deduplicate contours';
      _analysisProgress = 0.45;
    });

    await Future.delayed(const Duration(milliseconds: 600));

    if (mounted) {
      setState(() {
        _analysisStatus = '2/2: Querying Roboflow Disease Model...';
        _subStatus = 'Evaluating bulb pathology & foliar disease presence';
        _analysisProgress = 0.85;
      });
    }

    // Call preserved business logic
    final report = await ApiService.uploadAndAnalyze(_image!);

    // Also record into History repository
    HistoryRepository.instance.addReport(
      report,
      imagePath: _image!.path,
      farmName: 'Procurement Lot #${report.uploadId.split('-').last}',
    );

    if (!mounted) return;

    setState(() {
      _analysisProgress = 1.0;
      _isAnalyzing = false;
    });

    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => AnalysisScreen(report: report, imageFile: _image),
      ),
    );
  }

  void _showLightingTipsModal() {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => Padding(
        padding: AppSpacing.screenPadding.copyWith(top: 20, bottom: 28),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    const Icon(AppIcons.lightbulb, color: AppColors.secondary, size: 20),
                    const SizedBox(width: AppSpacing.xs),
                    Text('Tray Scanning Best Practices', style: AppTypography.headingSmall(isDark)),
                  ],
                ),
                IconButton(
                  icon: const Icon(AppIcons.close, size: 20),
                  onPressed: () => Navigator.pop(context),
                ),
              ],
            ),
            const SizedBox(height: AppSpacing.md),
            _buildTipRow(AppIcons.layers, 'Single Layer Spread',
                'Ensure onions do not overlap or stack on top of each other.', isDark),
            _buildTipRow(AppIcons.sun, 'Diffused Overhead Lighting',
                'Avoid strong single-directional flash that creates harsh dark shadows.', isDark),
            _buildTipRow(AppIcons.phone, 'Keep Phone Flat & Parallel',
                'Hold the phone directly above the center of the tray at 90 degrees.', isDark),
            _buildTipRow(AppIcons.crop, 'Include Complete Tray Boundary',
                'Fit the entire outer rim of the tray within the corner guide markers.', isDark),
          ],
        ),
      ),
    );
  }

  Widget _buildTipRow(IconData icon, String title, String desc, bool isDark) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: isDark ? AppColors.surfaceVariantDark : AppColors.surfaceVariantLight,
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(icon, size: 16, color: AppColors.primary),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: AppTypography.titleMedium(isDark).copyWith(fontSize: 13)),
                const SizedBox(height: 2),
                Text(desc, style: AppTypography.bodySmall(isDark)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Scan Onion Tray'),
        actions: [
          IconButton(
            tooltip: 'Scanning Guidelines',
            icon: const Icon(AppIcons.help, size: 22),
            onPressed: _showLightingTipsModal,
          ),
        ],
      ),
      body: _isAnalyzing
          ? ScanningRadarView(
              imageFile: _image,
              statusText: _analysisStatus,
              subStatusText: _subStatus,
              progress: _analysisProgress,
            )
          : SafeArea(
              child: Padding(
                padding: AppSpacing.screenPadding,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    // Main Camera Framing Area with Tray Overlay
                    Expanded(
                      child: Container(
                        decoration: BoxDecoration(
                          color: isDark ? AppColors.surfaceDark : Colors.grey.shade100,
                          borderRadius: AppSpacing.roundedCard,
                          border: Border.all(
                            color: isDark ? AppColors.borderDark : AppColors.borderLight,
                            width: 1.5,
                          ),
                          boxShadow: AppSpacing.cardShadowLight,
                        ),
                        clipBehavior: Clip.antiAlias,
                        child: Stack(
                          fit: StackFit.expand,
                          children: [
                            if (_image != null)
                              Image.file(_image!, fit: BoxFit.cover)
                            else
                              Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Container(
                                    width: 80,
                                    height: 80,
                                    decoration: BoxDecoration(
                                      color: (isDark ? AppColors.primaryLight : AppColors.primary).withAlpha(20),
                                      shape: BoxShape.circle,
                                    ),
                                    child: Icon(
                                      AppIcons.camera,
                                      size: 38,
                                      color: isDark ? AppColors.primaryLight : AppColors.primary,
                                    ),
                                  ),
                                  const SizedBox(height: AppSpacing.md),
                                  Text(
                                    'Position Tray in Frame',
                                    style: AppTypography.headingSmall(isDark),
                                  ),
                                  const SizedBox(height: AppSpacing.xs),
                                  Text(
                                    'Capture a top-down photo under good lighting',
                                    style: AppTypography.bodySmall(isDark),
                                  ),
                                ],
                              ),

                            // Tray Alignment Overlay with Corner Markers
                            const TrayAlignmentOverlay(),
                          ],
                        ),
                      ),
                    ),

                    const SizedBox(height: AppSpacing.md),

                    // Quick Tips Banner
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                      decoration: BoxDecoration(
                        color: isDark ? AppColors.surfaceVariantDark : AppColors.primaryContainer.withAlpha(120),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(
                          color: (isDark ? AppColors.primaryLight : AppColors.primary).withAlpha(40),
                        ),
                      ),
                      child: Row(
                        children: [
                          const Icon(AppIcons.sparkles, size: 18, color: AppColors.secondary),
                          const SizedBox(width: AppSpacing.xs),
                          Expanded(
                            child: Text(
                              'AI models count up to 40 onions per tray with NMS contour filtering.',
                              style: TextStyle(
                                fontSize: 12,
                                fontWeight: FontWeight.w500,
                                color: isDark ? AppColors.textSecondaryDark : AppColors.textPrimaryLight,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),

                    const SizedBox(height: AppSpacing.md),

                    // Action Buttons Row (Camera + Gallery)
                    Row(
                      children: [
                        Expanded(
                          flex: 3,
                          child: AppButton(
                            label: 'Capture Camera',
                            icon: AppIcons.camera,
                            variant: AppButtonVariant.primary,
                            onPressed: () => _pickImage(ImageSource.camera),
                          ),
                        ),
                        const SizedBox(width: AppSpacing.sm),
                        Expanded(
                          flex: 2,
                          child: AppButton(
                            label: 'Gallery',
                            icon: AppIcons.gallery,
                            variant: AppButtonVariant.outline,
                            onPressed: () => _pickImage(ImageSource.gallery),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
    );
  }
}
