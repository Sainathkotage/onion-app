import 'package:flutter/material.dart';
import '../theme/app_colors.dart';
import '../theme/app_icons.dart';
import '../theme/app_spacing.dart';

enum GradeBadgeSize { small, medium, large }

class GradeBadge extends StatelessWidget {
  final String grade;
  final GradeBadgeSize size;
  final bool showIcon;

  const GradeBadge({
    super.key,
    required this.grade,
    this.size = GradeBadgeSize.medium,
    this.showIcon = true,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final color = AppColors.getGradeColor(grade);
    final bgColor = AppColors.getGradeBgColor(grade, isDark: isDark);
    final borderColor = AppColors.getGradeBorderColor(grade, isDark: isDark);

    double fontSize;
    double iconSize;
    EdgeInsets padding;

    switch (size) {
      case GradeBadgeSize.small:
        fontSize = 11;
        iconSize = 12;
        padding = const EdgeInsets.symmetric(horizontal: 6, vertical: 2);
        break;
      case GradeBadgeSize.medium:
        fontSize = 12;
        iconSize = 14;
        padding = const EdgeInsets.symmetric(horizontal: 10, vertical: 4);
        break;
      case GradeBadgeSize.large:
        fontSize = 14;
        iconSize = 16;
        padding = const EdgeInsets.symmetric(horizontal: 14, vertical: 6);
        break;
    }

    IconData icon;
    final g = grade.toUpperCase();
    if (g.contains('A')) {
      icon = AppIcons.gradeA;
    } else if (g.contains('B')) {
      icon = AppIcons.gradeB;
    } else if (g.contains('C')) {
      icon = AppIcons.gradeC;
    } else {
      icon = AppIcons.reject;
    }

    return Container(
      padding: padding,
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: borderColor, width: 1),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (showIcon) ...[
            Icon(icon, size: iconSize, color: color),
            const SizedBox(width: AppSpacing.xxs),
          ],
          Text(
            grade,
            style: TextStyle(
              fontSize: fontSize,
              fontWeight: FontWeight.w700,
              color: color,
              letterSpacing: 0.1,
            ),
          ),
        ],
      ),
    );
  }
}
