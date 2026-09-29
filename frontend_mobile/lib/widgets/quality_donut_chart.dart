import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import '../theme/app_colors.dart';
import '../theme/app_spacing.dart';
import '../theme/app_typography.dart';

class QualityDonutChart extends StatefulWidget {
  final Map<String, double> distribution;

  const QualityDonutChart({super.key, required this.distribution});

  @override
  State<QualityDonutChart> createState() => _QualityDonutChartState();
}

class _QualityDonutChartState extends State<QualityDonutChart> {
  int _touchedIndex = -1;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    final gradeA = widget.distribution['Grade A'] ?? 0;
    final gradeB = widget.distribution['Grade B'] ?? 0;
    final gradeC = widget.distribution['Grade C'] ?? 0;
    final reject = widget.distribution['Reject'] ?? 0;

    final sections = [
      _buildSection(0, gradeA, AppColors.gradeA, 'A'),
      _buildSection(1, gradeB, AppColors.gradeB, 'B'),
      _buildSection(2, gradeC, AppColors.gradeC, 'C'),
      _buildSection(3, reject, AppColors.reject, 'R'),
    ];

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
          Text(
            'Batch Grade Distribution',
            style: AppTypography.headingSmall(isDark),
          ),
          const SizedBox(height: 2),
          Text(
            'Procurement standard vs rejected supply',
            style: AppTypography.bodySmall(isDark),
          ),
          const SizedBox(height: AppSpacing.lg),
          Row(
            children: [
              // Donut Chart
              Expanded(
                flex: 5,
                child: SizedBox(
                  height: 160,
                  child: Stack(
                    alignment: Alignment.center,
                    children: [
                      PieChart(
                        PieChartData(
                          pieTouchData: PieTouchData(
                            touchCallback: (event, pieTouchResponse) {
                              setState(() {
                                if (!event.isInterestedForInteractions ||
                                    pieTouchResponse == null ||
                                    pieTouchResponse.touchedSection == null) {
                                  _touchedIndex = -1;
                                  return;
                                }
                                _touchedIndex = pieTouchResponse.touchedSection!.touchedSectionIndex;
                              });
                            },
                          ),
                          borderData: FlBorderData(show: false),
                          sectionsSpace: 3,
                          centerSpaceRadius: 42,
                          sections: sections,
                        ),
                      ),
                      Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text(
                            '${gradeA.toStringAsFixed(0)}%',
                            style: AppTypography.statLarge(AppColors.gradeA),
                          ),
                          Text(
                            'Grade A',
                            style: AppTypography.labelSmall(isDark),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),

              const SizedBox(width: AppSpacing.md),

              // Legend
              Expanded(
                flex: 4,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    _buildLegendItem('Grade A', gradeA, AppColors.gradeA, isDark),
                    const SizedBox(height: 8),
                    _buildLegendItem('Grade B', gradeB, AppColors.gradeB, isDark),
                    const SizedBox(height: 8),
                    _buildLegendItem('Grade C', gradeC, AppColors.gradeC, isDark),
                    const SizedBox(height: 8),
                    _buildLegendItem('Reject', reject, AppColors.reject, isDark),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  PieChartSectionData _buildSection(int index, double value, Color color, String title) {
    final isTouched = index == _touchedIndex;
    final radius = isTouched ? 26.0 : 20.0;

    return PieChartSectionData(
      color: color,
      value: value > 0 ? value : 0.001,
      title: '',
      radius: radius,
      showTitle: false,
    );
  }

  Widget _buildLegendItem(String label, double percent, Color color, bool isDark) {
    return Row(
      children: [
        Container(
          width: 8,
          height: 8,
          decoration: BoxDecoration(
            color: color,
            shape: BoxShape.circle,
          ),
        ),
        const SizedBox(width: 6),
        Expanded(
          child: Text(
            label,
            style: AppTypography.labelSmall(isDark),
            overflow: TextOverflow.ellipsis,
          ),
        ),
        Text(
          '${percent.toStringAsFixed(1)}%',
          style: TextStyle(
            fontSize: 11,
            fontWeight: FontWeight.w700,
            color: color,
          ),
        ),
      ],
    );
  }
}
