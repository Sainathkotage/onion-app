import 'package:flutter/foundation.dart';
import 'mock_data.dart';
import '../models/onion_batch.dart';

/// In-memory repository managing scan history with ChangeNotifier for reactive updates.
class HistoryRepository extends ChangeNotifier {
  static final HistoryRepository instance = HistoryRepository._internal();
  factory HistoryRepository() => instance;

  HistoryRepository._internal() {
    MockDataRepository.initialize();
    _historyItems = List<ScanItem>.from(MockDataRepository.scans);
  }

  List<ScanItem> _historyItems = [];

  List<ScanItem> get historyItems => List.unmodifiable(_historyItems);

  void addReport(OnionBatchReport report, {String? imagePath, String? farmName}) {
    final grade = report.overallBatchGrade?.contains('Grade A') == true
        ? 'Grade A'
        : (report.gradeAPercentage >= 80 ? 'Grade A' : (report.gradeAPercentage >= 65 ? 'Grade B' : 'Reject'));

    final primaryDefect = report.defectBreakdown.entries
        .where((e) => e.key != 'Healthy' && e.value > 0)
        .fold<MapEntry<String, int>?>(null, (prev, curr) {
          if (prev == null || curr.value > prev.value) return curr;
          return prev;
        })?.key ?? 'None';

    final newItem = ScanItem(
      id: report.uploadId,
      batchId: 'BATCH-${report.uploadId.split('-').last}',
      farmName: farmName ?? 'Local Tray Inspection',
      timestamp: report.timestamp,
      score: report.gradeAPercentage,
      grade: grade,
      totalCount: report.totalOnions,
      gradeACount: report.gradeACount,
      rejectedCount: report.ursCount,
      primaryDefect: primaryDefect,
      diseaseStatus: report.diseaseBreakdown.isNotEmpty
          ? report.diseaseBreakdown.keys.first
          : (report.diseaseError == null ? 'Healthy' : 'Unchecked'),
      defectBreakdown: report.defectBreakdown,
      localImagePath: imagePath,
    );

    _historyItems.insert(0, newItem);
    notifyListeners();
  }

  void deleteItem(String id) {
    _historyItems.removeWhere((item) => item.id == id);
    notifyListeners();
  }

  List<ScanItem> filter({String query = '', String gradeFilter = 'All'}) {
    return _historyItems.where((item) {
      final matchesQuery = query.isEmpty ||
          item.id.toLowerCase().contains(query.toLowerCase()) ||
          item.batchId.toLowerCase().contains(query.toLowerCase()) ||
          item.farmName.toLowerCase().contains(query.toLowerCase());

      final matchesGrade = gradeFilter == 'All' || item.grade == gradeFilter;

      return matchesQuery && matchesGrade;
    }).toList();
  }
}
