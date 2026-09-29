import 'dart:io';
import 'package:flutter/material.dart';
import '../theme/app_colors.dart';
import '../theme/app_icons.dart';
import '../theme/app_spacing.dart';
import '../theme/app_typography.dart';

class ScanningRadarView extends StatefulWidget {
  final File? imageFile;
  final String statusText;
  final String subStatusText;
  final double progress; // 0.0 to 1.0

  const ScanningRadarView({
    super.key,
    this.imageFile,
    required this.statusText,
    required this.subStatusText,
    this.progress = 0.5,
  });

  @override
  State<ScanningRadarView> createState() => _ScanningRadarViewState();
}

class _ScanningRadarViewState extends State<ScanningRadarView>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scanLineAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 2200),
    )..repeat(reverse: true);

    _scanLineAnimation = Tween<double>(begin: 0.05, end: 0.95).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Center(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Frame with Image or Schematic Tray and animated laser scanline
            Container(
              width: double.infinity,
              height: 320,
              decoration: BoxDecoration(
                color: isDark ? AppColors.surfaceVariantDark : Colors.grey.shade100,
                borderRadius: AppSpacing.roundedCard,
                border: Border.all(
                  color: isDark ? AppColors.borderDark : AppColors.borderLight,
                  width: 1.5,
                ),
                boxShadow: AppSpacing.cardShadowLight,
              ),
              clipBehavior: Clip.antiAlias,
              child: Stack(
                children: [
                  // Base image or placeholder
                  if (widget.imageFile != null)
                    Positioned.fill(
                      child: Image.file(
                        widget.imageFile!,
                        fit: BoxFit.cover,
                      ),
                    )
                  else
                    Positioned.fill(
                      child: Center(
                        child: Icon(
                          AppIcons.scan,
                          size: 64,
                          color: AppColors.primary.withAlpha(60),
                        ),
                      ),
                    ),

                  // Semi-transparent dark overlay for scan line contrast
                  Positioned.fill(
                    child: Container(
                      color: Colors.black.withAlpha(50),
                    ),
                  ),

                  // Animated Scanning Laser Line
                  AnimatedBuilder(
                    animation: _scanLineAnimation,
                    builder: (context, child) {
                      return LayoutBuilder(
                        builder: (context, constraints) {
                          final topPos = constraints.maxHeight * _scanLineAnimation.value;
                          return Positioned(
                            top: topPos,
                            left: 0,
                            right: 0,
                            child: Container(
                              height: 3,
                              decoration: BoxDecoration(
                                gradient: LinearGradient(
                                  colors: [
                                    AppColors.secondary.withAlpha(0),
                                    AppColors.secondary,
                                    AppColors.secondaryLight,
                                    AppColors.secondary,
                                    AppColors.secondary.withAlpha(0),
                                  ],
                                ),
                                boxShadow: [
                                  BoxShadow(
                                    color: AppColors.secondary.withAlpha(180),
                                    blurRadius: 10,
                                    spreadRadius: 2,
                                  ),
                                ],
                              ),
                            ),
                          );
                        },
                      );
                    },
                  ),

                  // Top corner tags
                  Positioned(
                    top: AppSpacing.sm,
                    left: AppSpacing.sm,
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: Colors.black87,
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: const Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(AppIcons.pulse, size: 12, color: AppColors.gradeA),
                          SizedBox(width: 4),
                          Text(
                            'AI INFERENCE ACTIVE',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 10,
                              fontWeight: FontWeight.w700,
                              letterSpacing: 0.5,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: AppSpacing.xl),

            // Step status and progress bar
            Text(
              widget.statusText,
              textAlign: TextAlign.center,
              style: AppTypography.headingSmall(isDark),
            ),
            const SizedBox(height: AppSpacing.xs),
            Text(
              widget.subStatusText,
              textAlign: TextAlign.center,
              style: AppTypography.bodySmall(isDark),
            ),
            const SizedBox(height: AppSpacing.lg),

            // Sleek progress bar
            ClipRRect(
              borderRadius: BorderRadius.circular(8),
              child: SizedBox(
                width: 220,
                height: 6,
                child: LinearProgressIndicator(
                  value: widget.progress > 0 ? widget.progress : null,
                  backgroundColor: isDark ? AppColors.surfaceVariantDark : AppColors.borderLight,
                  valueColor: const AlwaysStoppedAnimation<Color>(AppColors.secondary),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
