import 'package:flutter/material.dart';
import '../data/mock_data.dart';
import '../theme/app_colors.dart';
import '../theme/app_spacing.dart';
import '../theme/app_typography.dart';

class DefectBarChart extends StatelessWidget {
  final List<DefectStat>? stats;

  const DefectBarChart({super.key, this.stats});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final items = stats ?? MockDataRepository.getDefectStats();

    final totalDefects = items.fold<int>(0, (sum, item) => sum + item.count);

    return Container(
      padding: AppSpacing.cardPadding,
      decoration: BoxDecoration(
        color: theme.cardTheme.color,
        borderRadius: AppSpacing.roundedCard,
        border: Border.all(
          color: isDark ? AppColors.borderDark : AppColors.borderLight,
          width: 1,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Defect Frequency Analysis',
                style: AppTypography.headingSmall(isDark),
              ),
              const SizedBox(height: 2),
              Text(
                '$totalDefects defect instances logged across 30 days',
                style: AppTypography.bodySmall(isDark),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.lg),

          // Horizontal Bar Rows
          ...items.map((stat) => Padding(
                padding: const EdgeInsets.only(bottom: 12.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Expanded(
                          child: Row(
                            children: [
                              Container(
                                width: 10,
                                height: 10,
                                decoration: BoxDecoration(
                                  color: stat.color,
                                  borderRadius: BorderRadius.circular(3),
                                ),
                              ),
                              const SizedBox(width: 8),
                              Expanded(
                                child: Text(
                                  stat.label,
                                  style: TextStyle(
                                    fontSize: 13,
                                    fontWeight: FontWeight.w600,
                                    color: isDark ? AppColors.textPrimaryDark : AppColors.textPrimaryLight,
                                  ),
                                  overflow: TextOverflow.ellipsis,
                                ),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(width: 8),
                        Row(
                          children: [
                            Text(
                              '${stat.count} items',
                              style: AppTypography.labelSmall(isDark),
                            ),
                            const SizedBox(width: 8),
                            Text(
                              '${stat.percentage.toStringAsFixed(1)}%',
                              style: TextStyle(
                                fontSize: 12,
                                fontWeight: FontWeight.w700,
                                color: stat.color,
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                    const SizedBox(height: 6),
                    ClipRRect(
                      borderRadius: BorderRadius.circular(4),
                      child: Stack(
                        children: [
                          Container(
                            height: 7,
                            width: double.infinity,
                            color: isDark ? AppColors.surfaceVariantDark : AppColors.surfaceVariantLight,
                          ),
                          FractionallySizedBox(
                            widthFactor: (stat.percentage / 100).clamp(0.01, 1.0),
                            child: Container(
                              height: 7,
                              decoration: BoxDecoration(
                                color: stat.color,
                                borderRadius: BorderRadius.circular(4),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              )),
        ],
      ),
    );
  }
}
