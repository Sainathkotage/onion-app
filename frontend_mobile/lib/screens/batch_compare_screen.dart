import 'package:flutter/material.dart';
import '../data/mock_data.dart';
import '../theme/app_colors.dart';
import '../theme/app_icons.dart';
import '../theme/app_spacing.dart';
import '../theme/app_typography.dart';
import '../widgets/grade_badge.dart';

class BatchCompareScreen extends StatefulWidget {
  const BatchCompareScreen({super.key});

  @override
  State<BatchCompareScreen> createState() => _BatchCompareScreenState();
}

class _BatchCompareScreenState extends State<BatchCompareScreen> {
  late BatchSummary _batchA;
  late BatchSummary _batchB;

  @override
  void initState() {
    super.initState();
    MockDataRepository.initialize();
    _batchA = MockDataRepository.batches.first;
    _batchB = MockDataRepository.batches.length > 1
        ? MockDataRepository.batches[1]
        : MockDataRepository.batches.first;
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final batches = MockDataRepository.batches;

    final scoreDiff = _batchA.qualityScore - _batchB.qualityScore;
    final gradeADiff = _batchA.gradeAPercent - _batchB.gradeAPercent;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Batch Lot Comparison'),
      ),
      body: SingleChildScrollView(
        padding: AppSpacing.screenPadding,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Side-by-Side Lot Analysis', style: AppTypography.headingSmall(isDark)),
            const SizedBox(height: 2),
            Text(
              'Compare quality grade, defect rates, and caliber consistency between suppliers.',
              style: AppTypography.bodySmall(isDark),
            ),
            const SizedBox(height: AppSpacing.lg),

            // Selectors Row
            Row(
              children: [
                Expanded(
                  child: _buildBatchSelector(
                    'Lot A',
                    _batchA,
                    batches,
                    (val) => setState(() => _batchA = val),
                    isDark,
                  ),
                ),
                const SizedBox(width: AppSpacing.sm),
                Expanded(
                  child: _buildBatchSelector(
                    'Lot B',
                    _batchB,
                    batches,
                    (val) => setState(() => _batchB = val),
                    isDark,
                  ),
                ),
              ],
            ),

            const SizedBox(height: AppSpacing.lg),

            // Comparison Delta Summary Card
            Container(
              padding: AppSpacing.cardPadding,
              decoration: BoxDecoration(
                color: (isDark ? AppColors.primaryLight : AppColors.primary).withAlpha(15),
                borderRadius: AppSpacing.roundedCard,
                border: Border.all(
                  color: (isDark ? AppColors.primaryLight : AppColors.primary).withAlpha(40),
                ),
              ),
              child: Row(
                children: [
                  Container(
                    width: 36,
                    height: 36,
                    decoration: BoxDecoration(
                      color: isDark ? AppColors.primaryLight : AppColors.primary,
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(AppIcons.compare, size: 18, color: Colors.white),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          scoreDiff >= 0
                              ? '${_batchA.id} leads by ${scoreDiff.abs().toStringAsFixed(1)} pts'
                              : '${_batchB.id} leads by ${scoreDiff.abs().toStringAsFixed(1)} pts',
                          style: AppTypography.titleMedium(isDark),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          'Grade A variance: ${gradeADiff >= 0 ? '+' : ''}${gradeADiff.toStringAsFixed(1)}% in favor of ${_batchA.id}',
                          style: AppTypography.bodySmall(isDark),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: AppSpacing.lg),

            // Metric Comparison Table
            _buildComparisonCard('Quality & Yield Metrics', [
              _buildCompareRow(
                'Overall Score',
                '${_batchA.qualityScore.toStringAsFixed(1)}%',
                '${_batchB.qualityScore.toStringAsFixed(1)}%',
                _batchA.qualityScore >= _batchB.qualityScore,
                isDark,
              ),
              _buildCompareRow(
                'Grade A Yield',
                '${_batchA.gradeAPercent.toStringAsFixed(1)}%',
                '${_batchB.gradeAPercent.toStringAsFixed(1)}%',
                _batchA.gradeAPercent >= _batchB.gradeAPercent,
                isDark,
              ),
              _buildCompareRow(
                'Total Volume',
                '${_batchA.totalWeightKg} kg',
                '${_batchB.totalWeightKg} kg',
                true,
                isDark,
              ),
              _buildCompareRow(
                'Procurement Grade',
                _batchA.grade,
                _batchB.grade,
                _batchA.grade == 'Grade A',
                isDark,
              ),
            ], isDark),

            const SizedBox(height: AppSpacing.lg),

            // Defect Rates Comparison
            _buildComparisonCard('Defect Breakdown (Estimated items)', [
              _buildCompareRow(
                'Sprouting Bulbs',
                '${_batchA.defectBreakdown['Sprouting'] ?? 0}',
                '${_batchB.defectBreakdown['Sprouting'] ?? 0}',
                (_batchA.defectBreakdown['Sprouting'] ?? 0) <= (_batchB.defectBreakdown['Sprouting'] ?? 0),
                isDark,
              ),
              _buildCompareRow(
                'Bruising / Cuts',
                '${_batchA.defectBreakdown['Bruising'] ?? 0}',
                '${_batchB.defectBreakdown['Bruising'] ?? 0}',
                (_batchA.defectBreakdown['Bruising'] ?? 0) <= (_batchB.defectBreakdown['Bruising'] ?? 0),
                isDark,
              ),
              _buildCompareRow(
                'Rot & Spoilage',
                '${_batchA.defectBreakdown['Rotten'] ?? 0}',
                '${_batchB.defectBreakdown['Rotten'] ?? 0}',
                (_batchA.defectBreakdown['Rotten'] ?? 0) <= (_batchB.defectBreakdown['Rotten'] ?? 0),
                isDark,
              ),
            ], isDark),

            const SizedBox(height: AppSpacing.lg),

            // Shelf Life & Market Recommendation
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
                    children: [
                      const Icon(AppIcons.lightbulb, color: AppColors.secondary, size: 18),
                      const SizedBox(width: AppSpacing.xs),
                      Expanded(
                        child: Text(
                          'Storage & Commercial Advisory',
                          style: AppTypography.headingSmall(isDark),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text(
                    '• ${_batchA.id} (${_batchA.farmName}): Optimal for long-term cold ventilation (Est. shelf-life: 90 days).\n'
                    '• ${_batchB.id} (${_batchB.farmName}): Recommended for immediate APMC auction or food processing dispatch within 14 days due to higher moisture and defect incidence.',
                    style: AppTypography.bodySmall(isDark).copyWith(height: 1.5),
                  ),
                ],
              ),
            ),
            const SizedBox(height: AppSpacing.xl),
          ],
        ),
      ),
    );
  }

  Widget _buildBatchSelector(
    String label,
    BatchSummary selected,
    List<BatchSummary> all,
    ValueChanged<BatchSummary> onChanged,
    bool isDark,
  ) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: Theme.of(context).cardTheme.color,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(
          color: isDark ? AppColors.borderDark : AppColors.borderLight,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label, style: AppTypography.labelSmall(isDark)),
          DropdownButtonHideUnderline(
            child: DropdownButton<BatchSummary>(
              isExpanded: true,
              value: selected,
              items: all.map((b) {
                return DropdownMenuItem(
                  value: b,
                  child: Text(
                    b.id,
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 13,
                      color: isDark ? AppColors.textPrimaryDark : AppColors.textPrimaryLight,
                    ),
                  ),
                );
              }).toList(),
              onChanged: (b) {
                if (b != null) onChanged(b);
              },
            ),
          ),
          Text(
            selected.farmName,
            style: AppTypography.bodySmall(isDark).copyWith(fontSize: 11),
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
          const SizedBox(height: 4),
          GradeBadge(grade: selected.grade, size: GradeBadgeSize.small),
        ],
      ),
    );
  }

  Widget _buildComparisonCard(String title, List<Widget> rows, bool isDark) {
    return Container(
      padding: AppSpacing.cardPadding,
      decoration: BoxDecoration(
        color: Theme.of(context).cardTheme.color,
        borderRadius: AppSpacing.roundedCard,
        border: Border.all(
          color: isDark ? AppColors.borderDark : AppColors.borderLight,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: AppTypography.headingSmall(isDark)),
          const SizedBox(height: 12),
          ...rows,
        ],
      ),
    );
  }

  Widget _buildCompareRow(
    String metric,
    String valA,
    String valB,
    bool isABetter,
    bool isDark,
  ) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Expanded(
            flex: 4,
            child: Text(metric, style: AppTypography.bodySmall(isDark)),
          ),
          Expanded(
            flex: 3,
            child: Text(
              valA,
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 13,
                fontWeight: isABetter ? FontWeight.bold : FontWeight.w500,
                color: isABetter ? AppColors.gradeA : (isDark ? AppColors.textPrimaryDark : AppColors.textPrimaryLight),
              ),
            ),
          ),
          Expanded(
            flex: 3,
            child: Text(
              valB,
              textAlign: TextAlign.right,
              style: TextStyle(
                fontSize: 13,
                fontWeight: !isABetter ? FontWeight.bold : FontWeight.w500,
                color: !isABetter ? AppColors.gradeA : (isDark ? AppColors.textPrimaryDark : AppColors.textPrimaryLight),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
