import 'package:flutter/material.dart';
import '../data/mock_data.dart';
import '../theme/app_colors.dart';
import '../theme/app_icons.dart';
import '../theme/app_spacing.dart';
import '../theme/app_typography.dart';
import '../widgets/defect_bar_chart.dart';
import '../widgets/grade_badge.dart';
import '../widgets/quality_donut_chart.dart';
import '../widgets/quality_trend_chart.dart';
import '../widgets/section_header.dart';
import '../widgets/shimmer_loading.dart';
import '../widgets/stat_card.dart';
import 'batch_compare_screen.dart';
import 'scan_screen.dart';

class DashboardScreen extends StatefulWidget {
  final VoidCallback? onNavigateToScan;
  final VoidCallback? onNavigateToHistory;

  const DashboardScreen({
    super.key,
    this.onNavigateToScan,
    this.onNavigateToHistory,
  });

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    MockDataRepository.initialize();
  }

  Future<void> _refreshData() async {
    setState(() => _isLoading = true);
    await Future.delayed(const Duration(milliseconds: 700));
    if (mounted) {
      setState(() => _isLoading = false);
    }
  }

  void _showAddBatchModal() {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final farmController = TextEditingController(text: 'Nashik Valley Orchards');
    final weightController = TextEditingController(text: '2400');

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => Padding(
        padding: EdgeInsets.only(
          bottom: MediaQuery.of(context).viewInsets.bottom + 24,
          left: 20,
          right: 20,
          top: 20,
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('Add Incoming Onion Lot', style: AppTypography.headingSmall(isDark)),
                IconButton(
                  icon: const Icon(AppIcons.close, size: 20),
                  onPressed: () => Navigator.pop(context),
                ),
              ],
            ),
            const SizedBox(height: 16),
            TextField(
              controller: farmController,
              decoration: const InputDecoration(
                labelText: 'Source Farm / Cooperative',
                border: OutlineInputBorder(),
                prefixIcon: Icon(AppIcons.farm, size: 18),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: weightController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: 'Total Lot Weight (kg)',
                border: OutlineInputBorder(),
                prefixIcon: Icon(AppIcons.scale, size: 18),
              ),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.pop(context);
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Lot for ${farmController.text} created. Ready for tray scanning.')),
                );
              },
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(double.infinity, 48),
              ),
              child: const Text('Register Lot & Proceed to Scan'),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final now = DateTime.now();
    final months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    final dateStr = '${now.day} ${months[now.month - 1]} ${now.year}';

    if (_isLoading) {
      return const Scaffold(body: SafeArea(child: DashboardSkeletonLoader()));
    }

    final totalScans = MockDataRepository.totalScansCount;
    final avgScore = MockDataRepository.averageQualityScore;
    final gradeAPercent = MockDataRepository.gradeAPercentage;
    final rejectRate = MockDataRepository.rejectionRate;
    final batches = MockDataRepository.batches;
    final suppliers = MockDataRepository.suppliers;
    final alerts = MockDataRepository.alerts;
    final recentScans = MockDataRepository.scans.take(8).toList();

    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            Container(
              width: 32,
              height: 32,
              decoration: BoxDecoration(
                color: isDark ? AppColors.primaryLight : AppColors.primary,
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Icon(AppIcons.scan, color: Colors.white, size: 18),
            ),
            const SizedBox(width: AppSpacing.xs),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'OnionIQ Mobile',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w800,
                    color: isDark ? AppColors.textPrimaryDark : AppColors.textPrimaryLight,
                    letterSpacing: -0.3,
                  ),
                ),
                Text(
                  'Procurement Center #260',
                  style: AppTypography.labelSmall(isDark).copyWith(fontSize: 10),
                ),
              ],
            ),
          ],
        ),
        actions: [
          IconButton(
            tooltip: 'Compare Batches',
            icon: const Icon(AppIcons.compare, size: 20),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const BatchCompareScreen()),
              );
            },
          ),
          IconButton(
            tooltip: 'Refresh Analytics',
            icon: const Icon(AppIcons.refresh, size: 20),
            onPressed: _refreshData,
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: _refreshData,
        color: AppColors.primary,
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: AppSpacing.screenPadding,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // 1. Greeting & Date Banner
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Good Morning, Inspector',
                          style: AppTypography.headingMedium(isDark),
                          overflow: TextOverflow.ellipsis,
                        ),
                        const SizedBox(height: 2),
                        Text(
                          '$dateStr • Automated APMC Grading Standard',
                          style: AppTypography.bodySmall(isDark),
                          overflow: TextOverflow.ellipsis,
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(width: 8),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(
                      color: AppColors.gradeABg,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: AppColors.gradeABorder),
                    ),
                    child: const Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(AppIcons.wifi, size: 12, color: AppColors.gradeA),
                        SizedBox(width: 4),
                        Text(
                          'LIVE SYNC',
                          style: TextStyle(fontSize: 10, fontWeight: FontWeight.w700, color: AppColors.gradeA),
                        ),
                      ],
                    ),
                  ),
                ],
              ),

              const SizedBox(height: AppSpacing.md),

              // 2. Quick Action Shortcut Pills Row
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: [
                    _buildQuickActionPill(
                      AppIcons.camera,
                      'New Scan',
                      isPrimary: true,
                      onTap: () {
                        if (widget.onNavigateToScan != null) {
                          widget.onNavigateToScan!();
                        } else {
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (context) => const ScanScreen()),
                          );
                        }
                      },
                      isDark: isDark,
                    ),
                    _buildQuickActionPill(
                      AppIcons.compare,
                      'Compare Batches',
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => const BatchCompareScreen()),
                        );
                      },
                      isDark: isDark,
                    ),
                    _buildQuickActionPill(
                      AppIcons.add,
                      'Add Lot',
                      onTap: _showAddBatchModal,
                      isDark: isDark,
                    ),
                    _buildQuickActionPill(
                      AppIcons.exportCsv,
                      'Export Report',
                      onTap: () {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Exporting 30-day Procurement Quality Summary...')),
                        );
                      },
                      isDark: isDark,
                    ),
                  ],
                ),
              ),

              const SizedBox(height: AppSpacing.lg),

              // 3. KPI Grid (4 core metrics with trends)
              GridView.count(
                crossAxisCount: 2,
                crossAxisSpacing: AppSpacing.sm,
                mainAxisSpacing: AppSpacing.sm,
                childAspectRatio: 1.25,
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                children: [
                  StatCard(
                    title: 'Total Scans',
                    value: '$totalScans',
                    icon: AppIcons.scan,
                    trendPercent: 8.4,
                    trendLabel: 'vs last week',
                    accentColor: isDark ? AppColors.primaryLight : AppColors.primary,
                  ),
                  StatCard(
                    title: 'Avg Quality Score',
                    value: '${avgScore.toStringAsFixed(1)}%',
                    icon: AppIcons.medal,
                    trendPercent: 2.1,
                    trendLabel: 'vs last week',
                    accentColor: AppColors.secondary,
                  ),
                  StatCard(
                    title: 'Grade A %',
                    value: '${gradeAPercent.toStringAsFixed(1)}%',
                    icon: AppIcons.success,
                    trendPercent: 4.2,
                    trendLabel: 'target: 80%',
                    accentColor: AppColors.gradeA,
                  ),
                  StatCard(
                    title: 'Rejection Rate',
                    value: '${rejectRate.toStringAsFixed(1)}%',
                    icon: AppIcons.warningOctagon,
                    trendPercent: -1.6,
                    trendLabel: 'limit: 20%',
                    accentColor: AppColors.reject,
                  ),
                ],
              ),

              const SizedBox(height: AppSpacing.lg),

              // 4. Alerts & Insights Card
              if (alerts.isNotEmpty) ...[
                _buildAlertsSection(alerts, isDark),
                const SizedBox(height: AppSpacing.lg),
              ],

              // 5. Line/Area Chart: 30-Day Quality Score Trend (7D / 30D / 90D)
              const QualityTrendChart(),

              const SizedBox(height: AppSpacing.lg),

              // 6. Quality Distribution Donut Chart
              QualityDonutChart(distribution: MockDataRepository.getGradeDistribution()),

              const SizedBox(height: AppSpacing.lg),

              // 7. Defect Frequency Bar Chart
              const DefectBarChart(),

              const SizedBox(height: AppSpacing.lg),

              // 8. Size Caliber Distribution (Horizontal Stacked Bar)
              _buildSizeDistributionCard(isDark),

              const SizedBox(height: AppSpacing.lg),

              // 9. Recent Scans Carousel
              SectionHeader(
                title: 'Recent Tray Scans',
                badgeText: '${recentScans.length}',
                actionText: 'View All',
                onAction: () {
                  if (widget.onNavigateToHistory != null) {
                    widget.onNavigateToHistory!();
                  }
                },
              ),
              const SizedBox(height: AppSpacing.xs),
              SizedBox(
                height: 130,
                child: ListView.builder(
                  scrollDirection: Axis.horizontal,
                  itemCount: recentScans.length,
                  itemBuilder: (context, idx) {
                    final scan = recentScans[idx];
                    return _buildRecentScanCard(scan, isDark);
                  },
                ),
              ),

              const SizedBox(height: AppSpacing.lg),

              // 10. Recent Batch / Lot List
              SectionHeader(
                title: 'Procurement Batches',
                badgeText: '${batches.length} Active',
                actionText: 'Compare',
                onAction: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const BatchCompareScreen()),
                  );
                },
              ),
              const SizedBox(height: AppSpacing.xs),
              ...batches.take(4).map((b) => _buildBatchTile(b, isDark)),

              const SizedBox(height: AppSpacing.lg),

              // 11. Top Suppliers / Farms Ranking
              const SectionHeader(
                title: 'Top Suppliers & Farms',
                subtitle: 'Ranked by average APMC grade yield',
              ),
              const SizedBox(height: AppSpacing.xs),
              _buildSuppliersCard(suppliers, isDark),

              const SizedBox(height: AppSpacing.xxl),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildQuickActionPill(
    IconData icon,
    String label, {
    bool isPrimary = false,
    required VoidCallback onTap,
    required bool isDark,
  }) {
    return Padding(
      padding: const EdgeInsets.only(right: 8.0),
      child: Material(
        color: isPrimary
            ? (isDark ? AppColors.primaryLight : AppColors.primary)
            : (isDark ? AppColors.surfaceVariantDark : Colors.white),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
          side: BorderSide(
            color: isPrimary
                ? Colors.transparent
                : (isDark ? AppColors.borderDark : AppColors.borderLight),
          ),
        ),
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(20),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(
                  icon,
                  size: 15,
                  color: isPrimary
                      ? Colors.white
                      : (isDark ? AppColors.textPrimaryDark : AppColors.textPrimaryLight),
                ),
                const SizedBox(width: 6),
                Text(
                  label,
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w600,
                    color: isPrimary
                        ? Colors.white
                        : (isDark ? AppColors.textPrimaryDark : AppColors.textPrimaryLight),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildAlertsSection(List<AlertInsight> alerts, bool isDark) {
    final alert = alerts.first;
    Color alertBg;
    Color alertBorder;
    Color alertIconColor;
    IconData alertIcon;

    if (alert.severity == 'danger') {
      alertBg = isDark ? AppColors.rejectBg.withAlpha(20) : AppColors.rejectBg;
      alertBorder = AppColors.rejectBorder;
      alertIconColor = AppColors.reject;
      alertIcon = AppIcons.warningOctagon;
    } else if (alert.severity == 'warning') {
      alertBg = isDark ? AppColors.gradeBBg.withAlpha(20) : AppColors.gradeBBg;
      alertBorder = AppColors.gradeBBorder;
      alertIconColor = AppColors.gradeB;
      alertIcon = AppIcons.gradeB;
    } else {
      alertBg = isDark ? AppColors.gradeABg.withAlpha(20) : AppColors.gradeABg;
      alertBorder = AppColors.gradeABorder;
      alertIconColor = AppColors.gradeA;
      alertIcon = AppIcons.gradeA;
    }

    return Container(
      padding: AppSpacing.cardPadding,
      decoration: BoxDecoration(
        color: alertBg,
        borderRadius: AppSpacing.roundedCard,
        border: Border.all(color: alertBorder),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: const EdgeInsets.all(6),
            decoration: BoxDecoration(
              color: alertIconColor.withAlpha(25),
              shape: BoxShape.circle,
            ),
            child: Icon(alertIcon, size: 18, color: alertIconColor),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Text(
                        alert.title,
                        style: TextStyle(
                          fontSize: 13,
                          fontWeight: FontWeight.w700,
                          color: alertIconColor,
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    const SizedBox(width: 8),
                    Text(
                      '3h ago',
                      style: AppTypography.labelSmall(isDark).copyWith(fontSize: 10),
                    ),
                  ],
                ),
                const SizedBox(height: 2),
                Text(
                  alert.message,
                  style: AppTypography.bodySmall(isDark).copyWith(
                    color: isDark ? AppColors.textSecondaryDark : const Color(0xFF374151),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSizeDistributionCard(bool isDark) {
    final sizes = MockDataRepository.getOverallSizeDistribution();
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
          Text('Bulb Caliber Size Distribution', style: AppTypography.headingSmall(isDark)),
          const SizedBox(height: 2),
          Text('Optimal procurement target: Medium 45-65mm', style: AppTypography.bodySmall(isDark)),
          const SizedBox(height: AppSpacing.md),

          // Stacked horizontal bar
          ClipRRect(
            borderRadius: BorderRadius.circular(6),
            child: SizedBox(
              height: 12,
              child: Row(
                children: [
                  Expanded(
                    flex: (sizes['Small (<45mm)']! * 10).toInt(),
                    child: Container(color: AppColors.defectUndersized),
                  ),
                  Expanded(
                    flex: (sizes['Medium (45-65mm)']! * 10).toInt(),
                    child: Container(color: AppColors.gradeA),
                  ),
                  Expanded(
                    flex: (sizes['Large (65-80mm)']! * 10).toInt(),
                    child: Container(color: AppColors.secondary),
                  ),
                  Expanded(
                    flex: (sizes['Jumbo (>80mm)']! * 10).toInt(),
                    child: Container(color: AppColors.defectSprouting),
                  ),
                ],
              ),
            ),
          ),

          const SizedBox(height: AppSpacing.md),

          // Legend grid
          Wrap(
            spacing: 12,
            runSpacing: 6,
            children: [
              _buildSizeLegend('Small (<45mm)', sizes['Small (<45mm)']!, AppColors.defectUndersized, isDark),
              _buildSizeLegend('Medium (45-65mm)', sizes['Medium (45-65mm)']!, AppColors.gradeA, isDark),
              _buildSizeLegend('Large (65-80mm)', sizes['Large (65-80mm)']!, AppColors.secondary, isDark),
              _buildSizeLegend('Jumbo (>80mm)', sizes['Jumbo (>80mm)']!, AppColors.defectSprouting, isDark),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildSizeLegend(String label, double val, Color color, bool isDark) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(width: 8, height: 8, decoration: BoxDecoration(color: color, shape: BoxShape.circle)),
        const SizedBox(width: 6),
        Text(
          '$label: ${val.toStringAsFixed(1)}%',
          style: AppTypography.labelSmall(isDark).copyWith(fontSize: 11),
        ),
      ],
    );
  }

  Widget _buildRecentScanCard(ScanItem scan, bool isDark) {
    return Container(
      width: 140,
      margin: const EdgeInsets.only(right: 10),
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: Theme.of(context).cardTheme.color,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(
          color: isDark ? AppColors.borderDark : AppColors.borderLight,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: Text(
                  scan.id,
                  style: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: Colors.grey),
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              const SizedBox(width: 4),
              GradeBadge(grade: scan.grade, size: GradeBadgeSize.small, showIcon: false),
            ],
          ),
          Text(
            '${scan.score.toStringAsFixed(1)}%',
            style: AppTypography.statMedium(AppColors.getGradeColor(scan.grade)),
          ),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                '${scan.totalCount} onions',
                style: AppTypography.labelSmall(isDark).copyWith(fontSize: 10),
              ),
              Text(
                scan.farmName.split(' ').first,
                style: AppTypography.bodySmall(isDark).copyWith(fontSize: 10),
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildBatchTile(BatchSummary b, bool isDark) {
    Color statusColor;
    if (b.status == 'ACCEPTED') {
      statusColor = AppColors.gradeA;
    } else if (b.status == 'UNDER_REVIEW') {
      statusColor = AppColors.gradeB;
    } else {
      statusColor = AppColors.reject;
    }

    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Theme.of(context).cardTheme.color,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: isDark ? AppColors.borderDark : AppColors.borderLight,
        ),
      ),
      child: Row(
        children: [
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              color: statusColor.withAlpha(20),
              borderRadius: BorderRadius.circular(10),
            ),
            child: Icon(AppIcons.package, size: 20, color: statusColor),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Expanded(
                      child: Text(
                        b.id,
                        style: AppTypography.titleMedium(isDark),
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    const SizedBox(width: 6),
                    GradeBadge(grade: b.grade, size: GradeBadgeSize.small),
                  ],
                ),
                const SizedBox(height: 2),
                Text(
                  '${b.farmName} • ${b.totalWeightKg} kg',
                  style: AppTypography.bodySmall(isDark).copyWith(fontSize: 11),
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          ),
          Column(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Text(
                '${b.qualityScore.toStringAsFixed(1)}%',
                style: AppTypography.statSmall(statusColor),
              ),
              Text(
                b.status.replaceAll('_', ' '),
                style: TextStyle(fontSize: 9, fontWeight: FontWeight.bold, color: statusColor),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildSuppliersCard(List<SupplierRanking> suppliers, bool isDark) {
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
        children: suppliers.asMap().entries.map((entry) {
          final idx = entry.key;
          final s = entry.value;
          final isTop = idx == 0;

          return Padding(
            padding: const EdgeInsets.symmetric(vertical: 6.0),
            child: Row(
              children: [
                Container(
                  width: 24,
                  height: 24,
                  decoration: BoxDecoration(
                    color: isTop ? AppColors.secondary : (isDark ? AppColors.surfaceVariantDark : Colors.grey.shade200),
                    shape: BoxShape.circle,
                  ),
                  child: Center(
                    child: Text(
                      '#${idx + 1}',
                      style: TextStyle(
                        fontSize: 11,
                        fontWeight: FontWeight.bold,
                        color: isTop ? Colors.white : (isDark ? AppColors.textPrimaryDark : Colors.black87),
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(s.name, style: AppTypography.labelMedium(isDark)),
                      Text('${s.region} • ${s.totalBatches} batches', style: AppTypography.labelSmall(isDark).copyWith(fontSize: 10)),
                    ],
                  ),
                ),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    Text('${s.avgScore.toStringAsFixed(1)}%', style: AppTypography.statSmall(AppColors.gradeA)),
                    Text(
                      '${s.gradeAPercent.toStringAsFixed(0)}% Grade A',
                      style: AppTypography.labelSmall(isDark).copyWith(fontSize: 10),
                    ),
                  ],
                ),
              ],
            ),
          );
        }).toList(),
      ),
    );
  }
}
