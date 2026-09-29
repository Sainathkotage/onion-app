import 'dart:math';
import 'package:flutter/material.dart';
import '../theme/app_colors.dart';
import '../theme/app_typography.dart';
import 'grade_badge.dart';

class CircularScoreGauge extends StatelessWidget {
  final double score; // 0 to 100
  final double size;
  final double strokeWidth;
  final String? grade;
  final String? subtitle;

  const CircularScoreGauge({
    super.key,
    required this.score,
    this.size = 180,
    this.strokeWidth = 14,
    this.grade,
    this.subtitle,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final color = AppColors.getGradeColor(grade ?? (score >= 80 ? 'Grade A' : (score >= 65 ? 'Grade B' : 'Reject')));
    final trackColor = isDark ? AppColors.surfaceVariantDark : AppColors.borderLight;

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        SizedBox(
          width: size,
          height: size,
          child: TweenAnimationBuilder<double>(
            tween: Tween<double>(begin: 0.0, end: (score / 100).clamp(0.0, 1.0)),
            duration: const Duration(milliseconds: 1200),
            curve: Curves.easeOutCubic,
            builder: (context, value, child) {
              return Stack(
                alignment: Alignment.center,
                children: [
                  CustomPaint(
                    size: Size(size, size),
                    painter: _GaugePainter(
                      progress: value,
                      color: color,
                      trackColor: trackColor,
                      strokeWidth: strokeWidth,
                    ),
                  ),
                  Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        '${(value * 100).toStringAsFixed(1)}%',
                        style: AppTypography.statHero(
                          isDark ? AppColors.textPrimaryDark : AppColors.textPrimaryLight,
                        ).copyWith(fontSize: size * 0.18),
                      ),
                      if (grade != null) ...[
                        const SizedBox(height: 4),
                        GradeBadge(grade: grade!, size: GradeBadgeSize.small),
                      ],
                    ],
                  ),
                ],
              );
            },
          ),
        ),
        if (subtitle != null) ...[
          const SizedBox(height: 8),
          Text(
            subtitle!,
            style: AppTypography.labelSmall(isDark),
          ),
        ],
      ],
    );
  }
}

class _GaugePainter extends CustomPainter {
  final double progress;
  final Color color;
  final Color trackColor;
  final double strokeWidth;

  _GaugePainter({
    required this.progress,
    required this.color,
    required this.trackColor,
    required this.strokeWidth,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = (size.width - strokeWidth) / 2;

    // Background track
    final trackPaint = Paint()
      ..color = trackColor
      ..style = PaintingStyle.stroke
      ..strokeWidth = strokeWidth
      ..strokeCap = StrokeCap.round;

    canvas.drawCircle(center, radius, trackPaint);

    // Active progress arc
    final progressPaint = Paint()
      ..color = color
      ..style = PaintingStyle.stroke
      ..strokeWidth = strokeWidth
      ..strokeCap = StrokeCap.round;

    // Start from top (-pi / 2)
    final sweepAngle = 2 * pi * progress;
    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      -pi / 2,
      sweepAngle,
      false,
      progressPaint,
    );
  }

  @override
  bool shouldRepaint(covariant _GaugePainter oldDelegate) {
    return oldDelegate.progress != progress ||
        oldDelegate.color != color ||
        oldDelegate.trackColor != trackColor;
  }
}
