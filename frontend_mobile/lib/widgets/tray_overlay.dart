import 'package:flutter/material.dart';
import '../theme/app_colors.dart';
import '../theme/app_icons.dart';
import '../theme/app_spacing.dart';

class TrayAlignmentOverlay extends StatelessWidget {
  final bool isLevel;
  final String statusText;

  const TrayAlignmentOverlay({
    super.key,
    this.isLevel = true,
    this.statusText = 'Align tray within corner markers',
  });

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        return Stack(
          children: [
            // Dark vignette overlay with transparent cutout in center
            CustomPaint(
              size: Size(constraints.maxWidth, constraints.maxHeight),
              painter: _TrayCutoutPainter(),
            ),

            // Top Guidance Pill
            Positioned(
              top: AppSpacing.md,
              left: AppSpacing.md,
              right: AppSpacing.md,
              child: Center(
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                  decoration: BoxDecoration(
                    color: Colors.black87,
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(
                      color: isLevel ? AppColors.gradeA : AppColors.secondary,
                      width: 1.2,
                    ),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(
                        isLevel ? AppIcons.gradeA : AppIcons.compass,
                        size: 16,
                        color: isLevel ? AppColors.gradeA : AppColors.secondary,
                      ),
                      const SizedBox(width: AppSpacing.xs),
                      Text(
                        statusText,
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 12,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),

            // Bottom Lighting Tip
            Positioned(
              bottom: AppSpacing.md,
              left: AppSpacing.md,
              right: AppSpacing.md,
              child: Center(
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: Colors.black54,
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: const Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(AppIcons.sun, size: 14, color: AppColors.secondaryLight),
                      SizedBox(width: AppSpacing.xs),
                      Text(
                        'Ensure even lighting without heavy shadows',
                        style: TextStyle(
                          color: Colors.white70,
                          fontSize: 11,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        );
      },
    );
  }
}

class _TrayCutoutPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    const marginHorizontal = 24.0;
    const marginVertical = 50.0;

    final cutoutRect = Rect.fromLTRB(
      marginHorizontal,
      marginVertical,
      size.width - marginHorizontal,
      size.height - marginVertical,
    );

    final rrect = RRect.fromRectAndRadius(cutoutRect, const Radius.circular(18));

    // Outer dark semi-transparent fill
    final outerPath = Path()..addRect(Rect.fromLTWH(0, 0, size.width, size.height));
    final innerPath = Path()..addRRect(rrect);
    final combinedPath = Path.combine(PathOperation.difference, outerPath, innerPath);

    final bgPaint = Paint()..color = Colors.black.withAlpha(90);
    canvas.drawPath(combinedPath, bgPaint);

    // Subtle dashed/solid guide border
    final borderPaint = Paint()
      ..color = Colors.white.withAlpha(140)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.5;
    canvas.drawRRect(rrect, borderPaint);

    // Corner brackets
    const bracketLen = 28.0;
    final bracketPaint = Paint()
      ..color = AppColors.secondary
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3.5
      ..strokeCap = StrokeCap.round;

    // Top-left
    canvas.drawLine(cutoutRect.topLeft, cutoutRect.topLeft + const Offset(bracketLen, 0), bracketPaint);
    canvas.drawLine(cutoutRect.topLeft, cutoutRect.topLeft + const Offset(0, bracketLen), bracketPaint);

    // Top-right
    canvas.drawLine(cutoutRect.topRight, cutoutRect.topRight - const Offset(bracketLen, 0), bracketPaint);
    canvas.drawLine(cutoutRect.topRight, cutoutRect.topRight + const Offset(0, bracketLen), bracketPaint);

    // Bottom-left
    canvas.drawLine(cutoutRect.bottomLeft, cutoutRect.bottomLeft + const Offset(bracketLen, 0), bracketPaint);
    canvas.drawLine(cutoutRect.bottomLeft, cutoutRect.bottomLeft - const Offset(0, bracketLen), bracketPaint);

    // Bottom-right
    canvas.drawLine(cutoutRect.bottomRight, cutoutRect.bottomRight - const Offset(bracketLen, 0), bracketPaint);
    canvas.drawLine(cutoutRect.bottomRight, cutoutRect.bottomRight - const Offset(0, bracketLen), bracketPaint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
