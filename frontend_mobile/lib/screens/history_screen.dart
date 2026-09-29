import 'dart:io';
import 'package:flutter/material.dart';
import '../data/history_repository.dart';
import '../data/mock_data.dart';
import '../models/onion_batch.dart';
import '../theme/app_colors.dart';
import '../theme/app_icons.dart';
import '../theme/app_typography.dart';
import '../widgets/empty_state.dart';
import '../widgets/grade_badge.dart';
import 'analysis_screen.dart';

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  final TextEditingController _searchController = TextEditingController();
  String _selectedGradeFilter = 'All';

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  void _openDetail(ScanItem item) {
    // Construct OnionBatchReport from ScanItem to display in AnalysisScreen
    final report = OnionBatchReport(
      uploadId: item.id,
      timestamp: item.timestamp,
      totalOnions: item.totalCount,
      gradeACount: item.gradeACount,
      ursCount: item.rejectedCount,
      gradeAPercentage: item.score,
      ursPercentage: item.totalCount > 0 ? (item.rejectedCount / item.totalCount) * 100 : 0.0,
      defectBreakdown: item.defectBreakdown,
      onions: [],
      decision: item.grade == 'Grade A' ? 'ACCEPTED (GRADE A PROCUREMENT)' : 'BATCH REJECTED (HIGH URS)',
      overallBatchGrade: item.grade,
      diseaseBreakdown: {item.diseaseStatus: 1},
      roboflowModelInfo: 'Roboflow veg1-hcqsf/2',
    );

    File? imageFile;
    if (item.localImagePath != null && File(item.localImagePath!).existsSync()) {
      imageFile = File(item.localImagePath!);
    }

    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => AnalysisScreen(report: report, imageFile: imageFile),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return AnimatedBuilder(
      animation: HistoryRepository.instance,
      builder: (context, _) {
        final items = HistoryRepository.instance.filter(
          query: _searchController.text,
          gradeFilter: _selectedGradeFilter,
        );

        return Scaffold(
          appBar: AppBar(
            title: const Text('Inspection History'),
            actions: [
              IconButton(
                tooltip: 'Export CSV',
                icon: const Icon(AppIcons.exportCsv, size: 20),
                onPressed: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Exported ${items.length} records to CSV.')),
                  );
                },
              ),
            ],
          ),
          body: Column(
            children: [
              // Search & Filter Header
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
                child: Column(
                  children: [
                    // Search Bar
                    TextField(
                      controller: _searchController,
                      onChanged: (_) => setState(() {}),
                      decoration: InputDecoration(
                        hintText: 'Search batch ID, farm, or lot...',
                        prefixIcon: const Icon(AppIcons.search, size: 18),
                        suffixIcon: _searchController.text.isNotEmpty
                            ? IconButton(
                                icon: const Icon(AppIcons.close, size: 16),
                                onPressed: () {
                                  _searchController.clear();
                                  setState(() {});
                                },
                              )
                            : null,
                        contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                        filled: true,
                        fillColor: isDark ? AppColors.surfaceVariantDark : Colors.white,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                          borderSide: BorderSide(
                            color: isDark ? AppColors.borderDark : AppColors.borderLight,
                          ),
                        ),
                        enabledBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                          borderSide: BorderSide(
                            color: isDark ? AppColors.borderDark : AppColors.borderLight,
                          ),
                        ),
                      ),
                    ),

                    const SizedBox(height: 10),

                    // Filter Chips Row
                    SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: Row(
                        children: ['All', 'Grade A', 'Grade B', 'Grade C', 'Reject'].map((grade) {
                          final isSelected = _selectedGradeFilter == grade;
                          Color chipColor = grade == 'All'
                              ? (isDark ? AppColors.primaryLight : AppColors.primary)
                              : AppColors.getGradeColor(grade);

                          return Padding(
                            padding: const EdgeInsets.only(right: 6.0),
                            child: FilterChip(
                              label: Text(grade),
                              selected: isSelected,
                              onSelected: (val) {
                                setState(() {
                                  _selectedGradeFilter = grade;
                                });
                              },
                              backgroundColor: isDark ? AppColors.surfaceDark : Colors.white,
                              selectedColor: chipColor.withAlpha(isDark ? 50 : 30),
                              side: BorderSide(
                                color: isSelected
                                    ? chipColor
                                    : (isDark ? AppColors.borderDark : AppColors.borderLight),
                              ),
                              labelStyle: TextStyle(
                                fontSize: 12,
                                fontWeight: isSelected ? FontWeight.w700 : FontWeight.w500,
                                color: isSelected
                                    ? chipColor
                                    : (isDark ? AppColors.textSecondaryDark : AppColors.textSecondaryLight),
                              ),
                            ),
                          );
                        }).toList(),
                      ),
                    ),
                  ],
                ),
              ),

              const Divider(),

              // List of Scan Records
              Expanded(
                child: items.isEmpty
                    ? EmptyStateView(
                        icon: AppIcons.searchEmpty,
                        title: 'No Inspections Found',
                        message: _searchController.text.isNotEmpty
                            ? 'No records match "${_searchController.text}". Try a different search.'
                            : 'No inspections found under "$_selectedGradeFilter".',
                        actionLabel: 'Reset Filters',
                        onAction: () {
                          setState(() {
                            _searchController.clear();
                            _selectedGradeFilter = 'All';
                          });
                        },
                      )
                    : ListView.builder(
                        padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
                        itemCount: items.length,
                        itemBuilder: (context, index) {
                          final item = items[index];
                          final formattedDate =
                              '${item.timestamp.day}/${item.timestamp.month}/${item.timestamp.year} • ${item.timestamp.hour.toString().padLeft(2, '0')}:${item.timestamp.minute.toString().padLeft(2, '0')}';

                          return Dismissible(
                            key: Key(item.id),
                            direction: DismissDirection.endToStart,
                            background: Container(
                              alignment: Alignment.centerRight,
                              padding: const EdgeInsets.only(right: 20),
                              margin: const EdgeInsets.only(bottom: 8),
                              decoration: BoxDecoration(
                                color: AppColors.reject,
                                borderRadius: BorderRadius.circular(14),
                              ),
                              child: const Icon(AppIcons.delete, color: Colors.white, size: 20),
                            ),
                            onDismissed: (_) {
                              HistoryRepository.instance.deleteItem(item.id);
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(
                                  content: Text('Removed ${item.id} from history.'),
                                  action: SnackBarAction(
                                    label: 'Dismiss',
                                    onPressed: () {},
                                  ),
                                ),
                              );
                            },
                            child: Container(
                              margin: const EdgeInsets.only(bottom: 8),
                              decoration: BoxDecoration(
                                color: theme.cardTheme.color,
                                borderRadius: BorderRadius.circular(14),
                                border: Border.all(
                                  color: isDark ? AppColors.borderDark : AppColors.borderLight,
                                ),
                              ),
                              child: Material(
                                color: Colors.transparent,
                                child: InkWell(
                                  onTap: () => _openDetail(item),
                                  borderRadius: BorderRadius.circular(14),
                                  child: Padding(
                                    padding: const EdgeInsets.all(12.0),
                                    child: Row(
                                      children: [
                                        // Leading Thumbnail / Icon Box with Hero animation
                                        Hero(
                                          tag: 'scan_thumb_${item.id}',
                                          child: Container(
                                            width: 48,
                                            height: 48,
                                            decoration: BoxDecoration(
                                              color: (isDark ? AppColors.primaryLight : AppColors.primary)
                                                  .withAlpha(20),
                                              borderRadius: BorderRadius.circular(10),
                                            ),
                                            child: Icon(
                                              AppIcons.camera,
                                              size: 22,
                                              color: isDark ? AppColors.primaryLight : AppColors.primary,
                                            ),
                                          ),
                                        ),
                                        const SizedBox(width: 12),

                                        // Center Info
                                        Expanded(
                                          child: Column(
                                            crossAxisAlignment: CrossAxisAlignment.start,
                                            children: [
                                              Row(
                                                children: [
                                                  Expanded(
                                                    child: Text(
                                                      item.batchId,
                                                      style: AppTypography.titleMedium(isDark),
                                                      overflow: TextOverflow.ellipsis,
                                                    ),
                                                  ),
                                                  const SizedBox(width: 6),
                                                  GradeBadge(grade: item.grade, size: GradeBadgeSize.small),
                                                ],
                                              ),
                                              const SizedBox(height: 2),
                                              Text(
                                                item.farmName,
                                                style: AppTypography.bodySmall(isDark),
                                                maxLines: 1,
                                                overflow: TextOverflow.ellipsis,
                                              ),
                                              const SizedBox(height: 4),
                                              Row(
                                                children: [
                                                  Icon(AppIcons.calendar, size: 12, color: isDark ? AppColors.textMutedDark : AppColors.textMutedLight),
                                                  const SizedBox(width: 4),
                                                  Expanded(
                                                    child: Text(
                                                      formattedDate,
                                                      style: AppTypography.labelSmall(isDark).copyWith(fontSize: 10),
                                                      overflow: TextOverflow.ellipsis,
                                                    ),
                                                  ),
                                                ],
                                              ),
                                            ],
                                          ),
                                        ),

                                        // Right Score & Arrow
                                        Column(
                                          crossAxisAlignment: CrossAxisAlignment.end,
                                          children: [
                                            Text(
                                              '${item.score.toStringAsFixed(1)}%',
                                              style: AppTypography.statMedium(
                                                AppColors.getGradeColor(item.grade),
                                              ),
                                            ),
                                            Text(
                                              '${item.totalCount} onions',
                                              style: AppTypography.labelSmall(isDark).copyWith(fontSize: 10),
                                            ),
                                          ],
                                        ),
                                        const SizedBox(width: 4),
                                        Icon(
                                          AppIcons.chevronRight,
                                          size: 16,
                                          color: isDark ? AppColors.textMutedDark : AppColors.textMutedLight,
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          );
                        },
                      ),
              ),
            ],
          ),
        );
      },
    );
  }
}
