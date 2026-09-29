import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import '../data/mock_data.dart';
import '../theme/app_colors.dart';
import '../theme/app_spacing.dart';
import '../theme/app_typography.dart';

class QualityTrendChart extends StatefulWidget {
  const QualityTrendChart({super.key});

  @override
  State<QualityTrendChart> createState() => _QualityTrendChartState();
}

class _QualityTrendChartState extends State<QualityTrendChart> {
  int _selectedDays = 30; // 7, 30, or 90
  List<QualityTrendPoint> _points = [];

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  void _loadData() {
    setState(() {
      _points = MockDataRepository.getTrendData(_selectedDays);
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    final spots = <FlSpot>[];
    for (int i = 0; i < _points.length; i++) {
      spots.add(FlSpot(i.toDouble(), _points[i].score));
    }

    final latestScore = _points.isNotEmpty ? _points.last.score : 85.0;
    final firstScore = _points.isNotEmpty ? _points.first.score : 80.0;
    final diff = latestScore - firstScore;

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
          // Header with Duration Toggle
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Quality Score Trend',
                      style: AppTypography.headingSmall(isDark),
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 2),
                    Wrap(
                      spacing: AppSpacing.xs,
                      crossAxisAlignment: WrapCrossAlignment.center,
                      children: [
                        Text(
                          '${latestScore.toStringAsFixed(1)}% avg',
                          style: AppTypography.statSmall(
                            isDark ? AppColors.textPrimaryDark : AppColors.textPrimaryLight,
                          ),
                        ),
                        Text(
                          '(${diff >= 0 ? '+' : ''}${diff.toStringAsFixed(1)}% in $_selectedDays d)',
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.w600,
                            color: diff >= 0 ? AppColors.gradeA : AppColors.reject,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 8),
              // Segmented Toggle for 7D / 30D / 90D
              Container(
                padding: const EdgeInsets.all(3),
                decoration: BoxDecoration(
                  color: isDark ? AppColors.surfaceVariantDark : AppColors.surfaceVariantLight,
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [7, 30, 90].map((days) {
                    final isSelected = _selectedDays == days;
                    return InkWell(
                      onTap: () {
                        setState(() {
                          _selectedDays = days;
                          _loadData();
                        });
                      },
                      borderRadius: BorderRadius.circular(8),
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                        decoration: BoxDecoration(
                          color: isSelected
                              ? (isDark ? AppColors.primaryLight : AppColors.primary)
                              : Colors.transparent,
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(
                          '${days}D',
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.w700,
                            color: isSelected
                                ? Colors.white
                                : (isDark ? AppColors.textMutedDark : AppColors.textMutedLight),
                          ),
                        ),
                      ),
                    );
                  }).toList(),
                ),
              ),
            ],
          ),

          const SizedBox(height: AppSpacing.lg),

          // Line Chart Area
          SizedBox(
            height: 190,
            child: spots.isEmpty
                ? const Center(child: Text('No trend data available'))
                : LineChart(
                    LineChartData(
                      gridData: FlGridData(
                        show: true,
                        drawVerticalLine: false,
                        horizontalInterval: 10,
                        getDrawingHorizontalLine: (value) {
                          return FlLine(
                            color: isDark ? AppColors.borderDark : AppColors.borderLight,
                            strokeWidth: 1,
                            dashArray: [4, 4],
                          );
                        },
                      ),
                      titlesData: FlTitlesData(
                        show: true,
                        rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                        topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                        leftTitles: AxisTitles(
                          sideTitles: SideTitles(
                            showTitles: true,
                            reservedSize: 32,
                            interval: 15,
                            getTitlesWidget: (value, meta) {
                              return Text(
                                '${value.toInt()}%',
                                style: AppTypography.labelSmall(isDark).copyWith(fontSize: 10),
                              );
                            },
                          ),
                        ),
                        bottomTitles: AxisTitles(
                          sideTitles: SideTitles(
                            showTitles: true,
                            reservedSize: 22,
                            interval: (_points.length / 4).clamp(1, 30),
                            getTitlesWidget: (value, meta) {
                              final index = value.toInt();
                              if (index < 0 || index >= _points.length) return const SizedBox();
                              final date = _points[index].date;
                              return Text(
                                '${date.day}/${date.month}',
                                style: AppTypography.labelSmall(isDark).copyWith(fontSize: 10),
                              );
                            },
                          ),
                        ),
                      ),
                      borderData: FlBorderData(show: false),
                      minX: 0,
                      maxX: (_points.length - 1).toDouble(),
                      minY: 55,
                      maxY: 100,
                      lineBarsData: [
                        LineChartBarData(
                          spots: spots,
                          isCurved: true,
                          curveSmoothness: 0.25,
                          color: isDark ? AppColors.primaryLight : AppColors.primary,
                          barWidth: 3,
                          isStrokeCapRound: true,
                          dotData: const FlDotData(show: false),
                          belowBarData: BarAreaData(
                            show: true,
                            gradient: LinearGradient(
                              begin: Alignment.topCenter,
                              end: Alignment.bottomCenter,
                              colors: [
                                (isDark ? AppColors.primaryLight : AppColors.primary).withAlpha(80),
                                (isDark ? AppColors.primaryLight : AppColors.primary).withAlpha(0),
                              ],
                            ),
                          ),
                        ),
                      ],
                      lineTouchData: LineTouchData(
                        touchTooltipData: LineTouchTooltipData(
                          getTooltipColor: (touchedSpot) =>
                              isDark ? AppColors.surfaceVariantDark : Colors.black87,
                          getTooltipItems: (touchedSpots) {
                            return touchedSpots.map((spot) {
                              final index = spot.x.toInt();
                              final p = index < _points.length ? _points[index] : null;
                              final dateStr = p != null ? '${p.date.day}/${p.date.month}' : '';
                              return LineTooltipItem(
                                '$dateStr: ${spot.y.toStringAsFixed(1)}%\n${p?.scanCount ?? 0} scans',
                                const TextStyle(
                                  color: Colors.white,
                                  fontSize: 11,
                                  fontWeight: FontWeight.w600,
                                ),
                              );
                            }).toList();
                          },
                        ),
                      ),
                    ),
                  ),
          ),
        ],
      ),
    );
  }
}
