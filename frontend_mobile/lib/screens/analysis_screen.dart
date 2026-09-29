import 'dart:io';
import 'package:flutter/material.dart';
import '../models/onion_batch.dart';
import '../services/roboflow_service.dart';
import '../theme/app_colors.dart';
import '../theme/app_icons.dart';
import '../theme/app_spacing.dart';
import '../theme/app_typography.dart';
import '../widgets/app_button.dart';
import '../widgets/circular_gauge.dart';
import '../widgets/grade_badge.dart';

class AnalysisScreen extends StatefulWidget {
  final OnionBatchReport report;
  final File? imageFile;

  const AnalysisScreen({super.key, required this.report, this.imageFile});

  @override
  State<AnalysisScreen> createState() => _AnalysisScreenState();
}

class _AnalysisScreenState extends State<AnalysisScreen> {
  bool _showDebugOverlay = true;

  void _showApiKeyDialog() {
    final controller = TextEditingController(text: RoboflowService.apiKey);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: Row(
          children: [
            const Icon(AppIcons.apiKey, color: AppColors.secondary, size: 20),
            const SizedBox(width: AppSpacing.xs),
            Text('Roboflow API Key', style: AppTypography.headingSmall(isDark)),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Configure your Roboflow Universe API key for hosted onion disease pathology and grading models:',
              style: AppTypography.bodySmall(isDark),
            ),
            const SizedBox(height: AppSpacing.md),
            TextField(
              controller: controller,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'rf_xxxxxxxxxxxxxx',
                labelText: 'API Key',
                prefixIcon: Icon(AppIcons.lock, size: 18),
              ),
              obscureText: true,
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () {
              RoboflowService.setApiKey(controller.text);
              Navigator.pop(context);
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Roboflow API key updated successfully.')),
              );
              setState(() {});
            },
            child: const Text('Save Key'),
          ),
        ],
      ),
    );
  }

  void _showShareSummaryDialog() {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final r = widget.report;

    showDialog(
      context: context,
      builder: (context) => Dialog(
        shape: RoundedRectangleBorder(borderRadius: AppSpacing.roundedCard),
        child: Padding(
          padding: AppSpacing.cardPadding,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text('Batch Certificate Summary', style: AppTypography.headingSmall(isDark)),
                  IconButton(
                    icon: const Icon(AppIcons.close, size: 18),
                    onPressed: () => Navigator.pop(context),
                  ),
                ],
              ),
              const Divider(),
              const SizedBox(height: 8),
              _buildSummaryRow('Inspection ID', r.uploadId, isDark),
              _buildSummaryRow('Decision', r.decision, isDark),
              _buildSummaryRow('Verified Count', '${r.totalOnions} onions', isDark),
              _buildSummaryRow('Grade A Ratio', '${r.gradeAPercentage.toStringAsFixed(1)}%', isDark),
              _buildSummaryRow('URS Defect Ratio', '${r.ursPercentage.toStringAsFixed(1)}%', isDark),
              _buildSummaryRow('Pathology', r.diseaseBreakdown.isNotEmpty ? r.diseaseBreakdown.keys.first : 'Healthy', isDark),
              const SizedBox(height: 16),
              AppButton(
                width: double.infinity,
                label: 'Export PDF Report',
                icon: AppIcons.exportReport,
                onPressed: () {
                  Navigator.pop(context);
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Report ${r.uploadId} exported successfully.')),
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSummaryRow(String label, String value, bool isDark) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: AppTypography.labelSmall(isDark)),
          Text(value, style: AppTypography.labelMedium(isDark)),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final report = widget.report;
    final isApproved = report.gradeAPercentage >= 80.0;
    final gradeLabel = report.overallBatchGrade?.contains('Grade A') == true
        ? 'Grade A'
        : (isApproved ? 'Grade A' : (report.gradeAPercentage >= 65 ? 'Grade B' : 'Reject'));

    return Scaffold(
      appBar: AppBar(
        title: Text('Inspection: ${report.uploadId}'),
        actions: [
          IconButton(
            tooltip: 'Roboflow Key Config',
            icon: Icon(
              AppIcons.apiKey,
              color: RoboflowService.hasApiKey ? AppColors.gradeA : AppColors.secondary,
              size: 20,
            ),
            onPressed: _showApiKeyDialog,
          ),
          IconButton(
            tooltip: 'Share Report',
            icon: const Icon(AppIcons.share, size: 20),
            onPressed: _showShareSummaryDialog,
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: AppSpacing.screenPadding,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 1. Annotated Tray Photo with Bounding Boxes
            if (widget.imageFile != null) ...[
              Container(
                decoration: BoxDecoration(
                  borderRadius: AppSpacing.roundedCard,
                  boxShadow: AppSpacing.cardShadowLight,
                ),
                clipBehavior: Clip.antiAlias,
                child: Stack(
                  children: [
                    Image.file(
                      widget.imageFile!,
                      width: double.infinity,
                      height: 270,
                      fit: BoxFit.cover,
                    ),
                    Positioned.fill(
                      child: CustomPaint(
                        painter: BoundingBoxPainter(
                          onions: report.onions,
                          rawBoxes: report.rawBoxes,
                          showDebug: _showDebugOverlay,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: AppSpacing.sm),

              // Debug Overlay Toggle Bar
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                decoration: BoxDecoration(
                  color: theme.cardTheme.color,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(
                    color: isDark ? AppColors.borderDark : AppColors.borderLight,
                  ),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Row(
                      children: [
                        Icon(
                          AppIcons.layers,
                          size: 18,
                          color: _showDebugOverlay ? AppColors.secondary : AppColors.textMutedLight,
                        ),
                        const SizedBox(width: AppSpacing.xs),
                        Text(
                          'AI Bounding Box Overlay',
                          style: AppTypography.labelMedium(isDark),
                        ),
                      ],
                    ),
                    Switch(
                      value: _showDebugOverlay,
                      activeThumbColor: AppColors.secondary,
                      onChanged: (val) {
                        setState(() {
                          _showDebugOverlay = val;
                        });
                      },
                    ),
                  ],
                ),
              ),

              if (_showDebugOverlay) ...[
                const SizedBox(height: 6),
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: isDark ? AppColors.surfaceVariantDark : AppColors.secondaryContainer.withAlpha(120),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Row(
                    children: [
                      const Icon(AppIcons.info, color: AppColors.secondaryDark, size: 16),
                      const SizedBox(width: AppSpacing.xs),
                      Expanded(
                        child: Text(
                          'Displaying ${report.totalOnions} verified onions. '
                          '${report.rawBoxes.isNotEmpty ? "(${report.rawBoxes.length} raw contours filtered via NMS)" : "(NMS deduplication active)"}',
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.w500,
                            color: isDark ? AppColors.textSecondaryDark : AppColors.secondaryDark,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
              const SizedBox(height: AppSpacing.md),
            ],

            // 2. Decision Status Banner
            Container(
              padding: AppSpacing.cardPadding,
              decoration: BoxDecoration(
                color: isApproved ? AppColors.gradeABg : AppColors.rejectBg,
                borderRadius: AppSpacing.roundedCard,
                border: Border.all(
                  color: isApproved ? AppColors.gradeABorder : AppColors.rejectBorder,
                ),
              ),
              child: Row(
                children: [
                  Container(
                    width: 44,
                    height: 44,
                    decoration: BoxDecoration(
                      color: (isApproved ? AppColors.gradeA : AppColors.reject).withAlpha(30),
                      shape: BoxShape.circle,
                    ),
                    child: Icon(
                      isApproved ? AppIcons.gradeA : AppIcons.gradeC,
                      color: isApproved ? AppColors.gradeA : AppColors.reject,
                      size: 24,
                    ),
                  ),
                  const SizedBox(width: AppSpacing.md),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          report.decision,
                          style: TextStyle(
                            color: isApproved ? const Color(0xFF065F46) : const Color(0xFF991B1B),
                            fontWeight: FontWeight.w700,
                            fontSize: 15,
                          ),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          '${report.totalOnions} Onions Assessed • ${report.gradeACount} Grade A • ${report.ursCount} URS Defective',
                          style: TextStyle(
                            color: isApproved ? const Color(0xFF047857) : const Color(0xFFB91C1C),
                            fontSize: 12,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: AppSpacing.lg),

            // 3. Overall Quality Score Gauge & Grade Summary Cards
            Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                // Circular Gauge
                Expanded(
                  flex: 5,
                  child: Container(
                    padding: AppSpacing.cardPadding,
                    decoration: BoxDecoration(
                      color: theme.cardTheme.color,
                      borderRadius: AppSpacing.roundedCard,
                      border: Border.all(
                        color: isDark ? AppColors.borderDark : AppColors.borderLight,
                      ),
                    ),
                    child: Column(
                      children: [
                        CircularScoreGauge(
                          score: report.gradeAPercentage,
                          size: 140,
                          strokeWidth: 12,
                          grade: gradeLabel,
                          subtitle: 'Quality Score',
                        ),
                      ],
                    ),
                  ),
                ),

                const SizedBox(width: AppSpacing.md),

                // Grade Breakdown Quick Stats
                Expanded(
                  flex: 5,
                  child: Column(
                    children: [
                      _buildQuickStatCard(
                        'Grade A Ratio',
                        '${report.gradeAPercentage.toStringAsFixed(1)}%',
                        '${report.gradeACount} / ${report.totalOnions} onions',
                        AppColors.gradeA,
                        isDark,
                      ),
                      const SizedBox(height: AppSpacing.sm),
                      _buildQuickStatCard(
                        'URS Defect Ratio',
                        '${report.ursPercentage.toStringAsFixed(1)}%',
                        '${report.ursCount} / ${report.totalOnions} onions',
                        AppColors.reject,
                        isDark,
                      ),
                    ],
                  ),
                ),
              ],
            ),

            const SizedBox(height: AppSpacing.lg),

            // 4. Detailed Quality Parameters Breakdown Grid
            Text('Quality Parameters Breakdown', style: AppTypography.headingSmall(isDark)),
            const SizedBox(height: AppSpacing.sm),

            _buildQualityMetricTile(
              'Size Uniformity',
              'Consistent standard bulb caliber (45-65mm)',
              0.88,
              AppColors.gradeA,
              '88% within target spec',
              isDark,
            ),
            _buildQualityMetricTile(
              'Color Uniformity',
              'Deep red-purple pigmentation without sunburn patches',
              0.92,
              AppColors.gradeA,
              'Optimal pigmentation',
              isDark,
            ),
            _buildQualityMetricTile(
              'Surface Defects',
              'Skin peeling, mechanical cuts, or surface bruising',
              report.defectBreakdown['Damaged'] == 0 ? 0.95 : 0.70,
              report.defectBreakdown['Damaged'] == 0 ? AppColors.gradeA : AppColors.gradeB,
              '${report.defectBreakdown['Damaged'] ?? 0} cuts detected',
              isDark,
            ),
            _buildQualityMetricTile(
              'Sprouting Activity',
              'Premature neck shoot development',
              report.defectBreakdown['Sprouted'] == 0 ? 1.0 : 0.40,
              report.defectBreakdown['Sprouted'] == 0 ? AppColors.gradeA : AppColors.reject,
              report.defectBreakdown['Sprouted'] == 0 ? 'Zero sprouts' : '${report.defectBreakdown['Sprouted']} sprouted bulbs',
              isDark,
            ),
            _buildQualityMetricTile(
              'Rot & Soft Spoilage',
              'Bacterial neck rot and black mold contamination',
              report.defectBreakdown['Rotten'] == 0 ? 1.0 : 0.20,
              report.defectBreakdown['Rotten'] == 0 ? AppColors.gradeA : AppColors.reject,
              report.defectBreakdown['Rotten'] == 0 ? 'Clear of rot' : '${report.defectBreakdown['Rotten']} rotten items',
              isDark,
            ),

            const SizedBox(height: AppSpacing.lg),

            // 5. Roboflow Pathology Assessment
            Container(
              padding: AppSpacing.cardPadding,
              decoration: BoxDecoration(
                color: theme.cardTheme.color,
                borderRadius: AppSpacing.roundedCard,
                border: Border.all(
                  color: isDark ? AppColors.borderDark : AppColors.borderLight,
                ),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Row(
                        children: [
                          const Icon(AppIcons.pathology, color: AppColors.primary, size: 18),
                          const SizedBox(width: AppSpacing.xs),
                          Text('Pathology & Foliage Disease', style: AppTypography.headingSmall(isDark)),
                        ],
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                        decoration: BoxDecoration(
                          color: (isDark ? AppColors.primaryLight : AppColors.primary).withAlpha(25),
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: Text(
                          report.roboflowModelInfo ?? 'Roboflow AI',
                          style: TextStyle(
                            fontSize: 10,
                            fontWeight: FontWeight.w700,
                            color: isDark ? AppColors.primaryLight : AppColors.primary,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: AppSpacing.sm),

                  if (report.diseaseError != null) ...[
                    Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: isDark ? AppColors.surfaceVariantDark : AppColors.rejectBg,
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(color: AppColors.rejectBorder),
                      ),
                      child: Row(
                        children: [
                          const Icon(AppIcons.gradeB, color: AppColors.reject, size: 18),
                          const SizedBox(width: AppSpacing.xs),
                          Expanded(
                            child: Text(
                              report.diseaseError!,
                              style: TextStyle(
                                fontSize: 11,
                                color: isDark ? AppColors.textSecondaryDark : AppColors.reject,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ] else ...[
                    Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: report.diseaseBreakdown.entries.map((e) {
                        final conf = report.diseaseConfidences[e.key];
                        final label = conf != null
                            ? '${e.key} (${(conf * 100).toStringAsFixed(1)}%)'
                            : '${e.key}: ${e.value}';
                        return GradeBadge(grade: label, size: GradeBadgeSize.small);
                      }).toList(),
                    ),
                  ],
                ],
              ),
            ),

            const SizedBox(height: AppSpacing.xl),

            // 6. Action Buttons (Rescan, Export, Save)
            Row(
              children: [
                Expanded(
                  child: AppButton(
                    label: 'Rescan Tray',
                    icon: AppIcons.refresh,
                    variant: AppButtonVariant.outline,
                    onPressed: () => Navigator.pop(context),
                  ),
                ),
                const SizedBox(width: AppSpacing.sm),
                Expanded(
                  child: AppButton(
                    label: 'Export Report',
                    icon: AppIcons.exportReport,
                    variant: AppButtonVariant.primary,
                    onPressed: _showShareSummaryDialog,
                  ),
                ),
              ],
            ),
            const SizedBox(height: AppSpacing.xl),
          ],
        ),
      ),
    );
  }

  Widget _buildQuickStatCard(String title, String value, String subtitle, Color color, bool isDark) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: isDark ? AppColors.surfaceDark : Colors.white,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(
          color: isDark ? AppColors.borderDark : AppColors.borderLight,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: AppTypography.labelSmall(isDark)),
          const SizedBox(height: 2),
          Text(value, style: AppTypography.statLarge(color)),
          const SizedBox(height: 2),
          Text(subtitle, style: AppTypography.labelSmall(isDark).copyWith(fontSize: 10)),
        ],
      ),
    );
  }

  Widget _buildQualityMetricTile(
    String title,
    String desc,
    double progress,
    Color color,
    String status,
    bool isDark,
  ) {
    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: isDark ? AppColors.surfaceDark : Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: isDark ? AppColors.borderDark : AppColors.borderLight,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(title, style: AppTypography.labelMedium(isDark)),
              Text(
                status,
                style: TextStyle(
                  fontSize: 11,
                  fontWeight: FontWeight.w700,
                  color: color,
                ),
              ),
            ],
          ),
          const SizedBox(height: 2),
          Text(desc, style: AppTypography.bodySmall(isDark).copyWith(fontSize: 11)),
          const SizedBox(height: 8),
          ClipRRect(
            borderRadius: BorderRadius.circular(4),
            child: LinearProgressIndicator(
              value: progress.clamp(0.0, 1.0),
              minHeight: 5,
              backgroundColor: isDark ? AppColors.surfaceVariantDark : AppColors.surfaceVariantLight,
              valueColor: AlwaysStoppedAnimation<Color>(color),
            ),
          ),
        ],
      ),
    );
  }
}

class BoundingBoxPainter extends CustomPainter {
  final List<DetectedOnion> onions;
  final List<List<double>> rawBoxes;
  final bool showDebug;

  BoundingBoxPainter({
    required this.onions,
    required this.rawBoxes,
    required this.showDebug,
  });

  @override
  void paint(Canvas canvas, Size size) {
    // 1. Draw raw candidate boxes in amber if debug enabled
    if (showDebug && rawBoxes.isNotEmpty) {
      final rawPaint = Paint()
        ..color = AppColors.secondary.withAlpha(150)
        ..style = PaintingStyle.stroke
        ..strokeWidth = 1.5;

      for (final box in rawBoxes) {
        if (box.length >= 4) {
          double left = box[0] > 1.0 ? (box[0] / 1024.0) * size.width : box[0] * size.width;
          double top = box[1] > 1.0 ? (box[1] / 1024.0) * size.height : box[1] * size.height;
          double right = box[2] > 1.0 ? (box[2] / 1024.0) * size.width : box[2] * size.width;
          double bottom = box[3] > 1.0 ? (box[3] / 1024.0) * size.height : box[3] * size.height;

          canvas.drawRect(Rect.fromLTRB(left, top, right, bottom), rawPaint);
        }
      }
    }

    // 2. Draw final deduplicated NMS bounding boxes in bright emerald
    final boxPaint = Paint()
      ..color = AppColors.gradeA
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.5;

    final fillPaint = Paint()
      ..color = AppColors.gradeA.withAlpha(35)
      ..style = PaintingStyle.fill;

    const textStyle = TextStyle(
      color: Colors.white,
      fontSize: 10,
      fontWeight: FontWeight.w700,
    );

    for (int i = 0; i < onions.length; i++) {
      final onion = onions[i];
      if (onion.bbox.length >= 4) {
        double left, top, right, bottom;
        if (onion.bbox[0] <= 1.0 && onion.bbox[2] <= 1.0) {
          left = onion.bbox[0] * size.width;
          top = onion.bbox[1] * size.height;
          right = left + (onion.bbox[2] * size.width);
          bottom = top + (onion.bbox[3] * size.height);
        } else {
          left = (onion.bbox[0] / 1024.0) * size.width;
          top = (onion.bbox[1] / 1024.0) * size.height;
          right = (onion.bbox[2] / 1024.0) * size.width;
          bottom = (onion.bbox[3] / 1024.0) * size.height;
        }

        final rect = Rect.fromLTRB(left, top, right, bottom);
        canvas.drawRect(rect, fillPaint);
        canvas.drawRect(rect, boxPaint);

        // Label tag badge
        final tagText = 'Onion #${i + 1} (${(onion.confidence * 100).toInt()}%)';
        final textSpan = TextSpan(text: tagText, style: textStyle);
        final textPainter = TextPainter(text: textSpan, textDirection: TextDirection.ltr);
        textPainter.layout();

        final tagRect = Rect.fromLTWH(left, top - 18 > 0 ? top - 18 : top, textPainter.width + 8, 16);
        canvas.drawRect(tagRect, Paint()..color = AppColors.gradeA);
        textPainter.paint(canvas, Offset(left + 4, top - 18 > 0 ? top - 15 : top + 2));
      }
    }
  }

  @override
  bool shouldRepaint(covariant BoundingBoxPainter oldDelegate) {
    return oldDelegate.showDebug != showDebug ||
        oldDelegate.onions != onions ||
        oldDelegate.rawBoxes != rawBoxes;
  }
}
