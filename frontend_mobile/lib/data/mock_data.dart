import 'dart:math';
import 'package:flutter/material.dart';
import '../theme/app_colors.dart';

/// Models for Dashboard and Historical Analytics
class BatchSummary {
  final String id;
  final String farmName;
  final String region;
  final int totalWeightKg;
  final int totalOnions;
  final double gradeAPercent;
  final double qualityScore; // 0 - 100
  final String grade; // Grade A, Grade B, Grade C, Reject
  final DateTime timestamp;
  final String status; // ACCEPTED, UNDER_REVIEW, REJECTED
  final Map<String, int> defectBreakdown;
  final Map<String, double> sizeDistribution;

  const BatchSummary({
    required this.id,
    required this.farmName,
    required this.region,
    required this.totalWeightKg,
    required this.totalOnions,
    required this.gradeAPercent,
    required this.qualityScore,
    required this.grade,
    required this.timestamp,
    required this.status,
    required this.defectBreakdown,
    required this.sizeDistribution,
  });
}

class ScanItem {
  final String id;
  final String batchId;
  final String farmName;
  final DateTime timestamp;
  final double score; // 0 - 100
  final String grade;
  final int totalCount;
  final int gradeACount;
  final int rejectedCount;
  final String primaryDefect;
  final String diseaseStatus; // Healthy, Downy Mildew, Purple Blotch, etc.
  final Map<String, int> defectBreakdown;
  final String? localImagePath;

  const ScanItem({
    required this.id,
    required this.batchId,
    required this.farmName,
    required this.timestamp,
    required this.score,
    required this.grade,
    required this.totalCount,
    required this.gradeACount,
    required this.rejectedCount,
    required this.primaryDefect,
    required this.diseaseStatus,
    required this.defectBreakdown,
    this.localImagePath,
  });
}

class SupplierRanking {
  final String id;
  final String name;
  final String region;
  final int totalBatches;
  final double avgScore;
  final double gradeAPercent;
  final double trendPercent; // Positive = improvement

  const SupplierRanking({
    required this.id,
    required this.name,
    required this.region,
    required this.totalBatches,
    required this.avgScore,
    required this.gradeAPercent,
    required this.trendPercent,
  });
}

class AlertInsight {
  final String id;
  final String title;
  final String message;
  final String severity; // warning, info, danger, success
  final DateTime timestamp;
  final String? batchId;
  final String actionLabel;

  const AlertInsight({
    required this.id,
    required this.title,
    required this.message,
    required this.severity,
    required this.timestamp,
    this.batchId,
    required this.actionLabel,
  });
}

class QualityTrendPoint {
  final DateTime date;
  final double score;
  final int scanCount;

  const QualityTrendPoint({
    required this.date,
    required this.score,
    required this.scanCount,
  });
}

class DefectStat {
  final String label;
  final int count;
  final double percentage;
  final Color color;

  const DefectStat({
    required this.label,
    required this.count,
    required this.percentage,
    required this.color,
  });
}

/// Central Mock Repository providing over 60 realistic scans across 30 days,
/// batch records, supplier rankings, and live analytics.
class MockDataRepository {
  static final List<String> farmNames = [
    'Nashik Valley Orchards',
    'Deccan Harvest Agri',
    'Krishna Valley Farms',
    'Solapur Agro Syndicate',
    'Pimpalgaon Cooperative',
    'Sahyadri Fresh Farms',
    'Godavari Basin Farms',
    'Malegaon Red Onion Co',
  ];

  static final List<String> regions = [
    'Nashik, Maharashtra',
    'Pune, Maharashtra',
    'Solapur, Maharashtra',
    'Ahmednagar, Maharashtra',
    'Dindori, Maharashtra',
  ];

  static late final List<ScanItem> scans;
  static late final List<BatchSummary> batches;
  static late final List<SupplierRanking> suppliers;
  static late final List<AlertInsight> alerts;

  static bool _isInitialized = false;

  static void initialize() {
    if (_isInitialized) return;
    _generateMockScans();
    _generateMockBatches();
    _generateSuppliers();
    _generateAlerts();
    _isInitialized = true;
  }

  static void _generateMockScans() {
    final list = <ScanItem>[];
    final random = Random(42); // Deterministic seed for consistency
    final now = DateTime.now();

    final defectTypes = ['Sprouting', 'Bruising', 'Neck Rot', 'Discoloration', 'Cracks', 'Undersized'];
    final diseases = ['Healthy (No Lesions)', 'Downy Mildew', 'Purple Blotch', 'Rust'];

    // Generate 72 realistic scans across 30 days
    for (int i = 0; i < 72; i++) {
      final daysAgo = (i * 30 / 72).floor();
      final scanTime = now.subtract(Duration(days: daysAgo, hours: random.nextInt(12), minutes: random.nextInt(59)));
      final farm = farmNames[random.nextInt(farmNames.length)];
      final batchNum = 1000 + (72 - i ~/ 3);

      final totalOnions = 15 + random.nextInt(25); // 15 - 40 onions per tray
      final scoreBase = 72.0 + (random.nextDouble() * 26.0) - (daysAgo > 20 ? 5.0 : 0.0);
      final score = (scoreBase.clamp(52.0, 98.5) * 10).round() / 10;

      String grade;
      String primaryDefect = 'None';
      String disease = 'Healthy (No Lesions)';

      if (score >= 85.0) {
        grade = 'Grade A';
      } else if (score >= 72.0) {
        grade = 'Grade B';
        primaryDefect = defectTypes[random.nextInt(3)];
      } else if (score >= 60.0) {
        grade = 'Grade C';
        primaryDefect = defectTypes[random.nextInt(defectTypes.length)];
        disease = random.nextBool() ? diseases[random.nextInt(diseases.length)] : 'Healthy (No Lesions)';
      } else {
        grade = 'Reject';
        primaryDefect = random.nextBool() ? 'Neck Rot' : 'Sprouting';
        disease = diseases[1 + random.nextInt(diseases.length - 1)];
      }

      int gradeACount = ((score / 100.0) * totalOnions).round();
      if (gradeACount > totalOnions) gradeACount = totalOnions;
      int rejectedCount = totalOnions - gradeACount;

      final breakdown = <String, int>{
        'Healthy': gradeACount,
        'Sprouting': grade == 'Grade A' ? 0 : random.nextInt(3),
        'Bruising': grade == 'Grade A' ? 0 : random.nextInt(3),
        'Rotten': grade == 'Reject' ? 2 + random.nextInt(3) : (grade == 'Grade C' ? 1 : 0),
        'Discoloration': random.nextInt(2),
        'Undersized': random.nextInt(2),
      };

      list.add(ScanItem(
        id: 'SCN-${10000 + i}',
        batchId: 'LOT-#$batchNum',
        farmName: farm,
        timestamp: scanTime,
        score: score,
        grade: grade,
        totalCount: totalOnions,
        gradeACount: gradeACount,
        rejectedCount: rejectedCount,
        primaryDefect: primaryDefect,
        diseaseStatus: disease,
        defectBreakdown: breakdown,
      ));
    }

    scans = list;
  }

  static void _generateMockBatches() {
    final list = <BatchSummary>[];
    final random = Random(99);
    final now = DateTime.now();

    for (int i = 0; i < 15; i++) {
      final daysAgo = i * 2;
      final time = now.subtract(Duration(days: daysAgo, hours: 2 + (i % 6)));
      final farm = farmNames[i % farmNames.length];
      final region = regions[i % regions.length];
      final weight = 1200 + random.nextInt(3500);
      final onionsEst = weight * 8; // approx 8 onions per kg

      final gradeScore = 65.0 + random.nextDouble() * 32.0;
      final score = (gradeScore * 10).round() / 10;
      final gradeAPercent = (score * 0.95).clamp(55.0, 97.0);

      String grade = 'Grade A';
      String status = 'ACCEPTED';
      if (score < 65.0) {
        grade = 'Reject';
        status = 'REJECTED';
      } else if (score < 75.0) {
        grade = 'Grade C';
        status = 'UNDER_REVIEW';
      } else if (score < 84.0) {
        grade = 'Grade B';
        status = 'ACCEPTED';
      }

      list.add(BatchSummary(
        id: 'LOT-#${1045 - i}',
        farmName: farm,
        region: region,
        totalWeightKg: weight,
        totalOnions: onionsEst,
        gradeAPercent: (gradeAPercent * 10).round() / 10,
        qualityScore: score,
        grade: grade,
        timestamp: time,
        status: status,
        defectBreakdown: {
          'Sprouting': (onionsEst * 0.04).round(),
          'Bruising': (onionsEst * 0.03).round(),
          'Rotten': (onionsEst * (grade == 'Reject' ? 0.08 : 0.015)).round(),
          'Discoloration': (onionsEst * 0.02).round(),
          'Cracks': (onionsEst * 0.01).round(),
        },
        sizeDistribution: {
          'Small (<45mm)': 12.0 + random.nextInt(8),
          'Medium (45-65mm)': 48.0 + random.nextInt(12),
          'Large (65-80mm)': 26.0 + random.nextInt(8),
          'Jumbo (>80mm)': 8.0 + random.nextInt(5),
        },
      ));
    }

    batches = list;
  }

  static void _generateSuppliers() {
    suppliers = [
      const SupplierRanking(
        id: 'SUP-01',
        name: 'Nashik Valley Orchards',
        region: 'Nashik, Maharashtra',
        totalBatches: 28,
        avgScore: 92.4,
        gradeAPercent: 94.2,
        trendPercent: 4.8,
      ),
      const SupplierRanking(
        id: 'SUP-02',
        name: 'Sahyadri Fresh Farms',
        region: 'Dindori, Maharashtra',
        totalBatches: 22,
        avgScore: 89.1,
        gradeAPercent: 91.0,
        trendPercent: 2.3,
      ),
      const SupplierRanking(
        id: 'SUP-03',
        name: 'Krishna Valley Farms',
        region: 'Solapur, Maharashtra',
        totalBatches: 19,
        avgScore: 86.7,
        gradeAPercent: 88.5,
        trendPercent: -1.2,
      ),
      const SupplierRanking(
        id: 'SUP-04',
        name: 'Pimpalgaon Cooperative',
        region: 'Nashik, Maharashtra',
        totalBatches: 31,
        avgScore: 84.3,
        gradeAPercent: 85.0,
        trendPercent: 1.5,
      ),
      const SupplierRanking(
        id: 'SUP-05',
        name: 'Deccan Harvest Agri',
        region: 'Pune, Maharashtra',
        totalBatches: 16,
        avgScore: 79.8,
        gradeAPercent: 78.4,
        trendPercent: -3.4,
      ),
    ];
  }

  static void _generateAlerts() {
    alerts = [
      AlertInsight(
        id: 'ALT-01',
        title: 'High Spoilage Detected',
        message: 'Rot rate increased by 6.2% in Batch #LOT-1041. Immediate inspection recommended.',
        severity: 'danger',
        timestamp: DateTime.now().subtract(const Duration(hours: 3)),
        batchId: 'LOT-#1041',
        actionLabel: 'Inspect Batch',
      ),
      AlertInsight(
        id: 'ALT-02',
        title: 'Storage Life Warning',
        message: 'Elevated moisture pattern in Deccan Harvest lot. Estimated shelf-life reduced to 18 days.',
        severity: 'warning',
        timestamp: DateTime.now().subtract(const Duration(hours: 8)),
        batchId: 'LOT-#1040',
        actionLabel: 'View Advisory',
      ),
      AlertInsight(
        id: 'ALT-03',
        title: 'Procurement Target Achieved',
        message: 'Weekly Grade A ratio reached 88.4%, exceeding the procurement threshold by 8.4%.',
        severity: 'success',
        timestamp: DateTime.now().subtract(const Duration(days: 1)),
        actionLabel: 'View Analytics',
      ),
    ];
  }

  // Dashboard Aggregates
  static int get totalScansCount => scans.length;
  static double get averageQualityScore =>
      scans.isEmpty ? 0 : scans.map((s) => s.score).reduce((a, b) => a + b) / scans.length;
  static double get gradeAPercentage {
    if (scans.isEmpty) return 0;
    final gradeACount = scans.where((s) => s.grade == 'Grade A').length;
    return (gradeACount / scans.length) * 100;
  }
  static double get rejectionRate {
    if (scans.isEmpty) return 0;
    final rejectCount = scans.where((s) => s.grade == 'Reject').length;
    return (rejectCount / scans.length) * 100;
  }

  // Quality Trend for Line Chart (7D, 30D, 90D)
  static List<QualityTrendPoint> getTrendData(int days) {
    initialize();
    final now = DateTime.now();
    final points = <QualityTrendPoint>[];

    for (int i = days - 1; i >= 0; i--) {
      final date = now.subtract(Duration(days: i));
      final dayScans = scans.where((s) =>
          s.timestamp.year == date.year &&
          s.timestamp.month == date.month &&
          s.timestamp.day == date.day).toList();

      double dayAvg;
      if (dayScans.isNotEmpty) {
        dayAvg = dayScans.map((s) => s.score).reduce((a, b) => a + b) / dayScans.length;
      } else {
        // Smooth interpolation based on day of week and baseline 82.0
        final wave = sin(i * 0.4) * 5.0;
        dayAvg = (82.0 + wave).clamp(70.0, 95.0);
      }
      points.add(QualityTrendPoint(
        date: date,
        score: (dayAvg * 10).round() / 10,
        scanCount: dayScans.length,
      ));
    }
    return points;
  }

  // Defect breakdown stats for Bar Chart
  static List<DefectStat> getDefectStats() {
    return const [
      DefectStat(label: 'Sprouting', count: 184, percentage: 34.2, color: AppColors.defectSprouting),
      DefectStat(label: 'Bruising', count: 142, percentage: 26.4, color: AppColors.defectBruising),
      DefectStat(label: 'Neck Rot', count: 96, percentage: 17.8, color: AppColors.defectRot),
      DefectStat(label: 'Discoloration', count: 68, percentage: 12.6, color: AppColors.defectDiscoloration),
      DefectStat(label: 'Cracks', count: 48, percentage: 9.0, color: AppColors.defectCracks),
    ];
  }

  // Grade Distribution for Donut Chart
  static Map<String, double> getGradeDistribution() {
    initialize();
    int countA = scans.where((s) => s.grade == 'Grade A').length;
    int countB = scans.where((s) => s.grade == 'Grade B').length;
    int countC = scans.where((s) => s.grade == 'Grade C').length;
    int countReject = scans.where((s) => s.grade == 'Reject').length;
    int total = scans.length;
    if (total == 0) return {'Grade A': 100};

    return {
      'Grade A': (countA / total) * 100,
      'Grade B': (countB / total) * 100,
      'Grade C': (countC / total) * 100,
      'Reject': (countReject / total) * 100,
    };
  }

  // Size Distribution
  static Map<String, double> getOverallSizeDistribution() {
    return const {
      'Small (<45mm)': 14.5,
      'Medium (45-65mm)': 52.0,
      'Large (65-80mm)': 24.5,
      'Jumbo (>80mm)': 9.0,
    };
  }
}
