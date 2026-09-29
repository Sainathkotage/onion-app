class DetectedOnion {
  final String id;
  final String label; // Healthy, Damaged, Rotten, Sprouted, Undersized
  final double confidence;
  final List<double> bbox; // [x, y, w, h] normalized 0-1 or pixel coords
  final String grade; // Grade A vs URS
  final String? diseaseLabel; // Healthy, Rust, Downy Mildew, Purple Blotch, Botrytis
  final double? diseaseConfidence;
  final List<String> defects;

  DetectedOnion({
    required this.id,
    required this.label,
    required this.confidence,
    required this.bbox,
    required this.grade,
    this.diseaseLabel,
    this.diseaseConfidence,
    this.defects = const [],
  });

  factory DetectedOnion.fromJson(Map<String, dynamic> json) {
    List<double> parsedBbox;
    if (json['bbox'] is List) {
      parsedBbox = (json['bbox'] as List).map((e) => (e as num).toDouble()).toList();
    } else {
      parsedBbox = [0.1, 0.1, 0.2, 0.2];
    }

    return DetectedOnion(
      id: json['id']?.toString() ?? 'onion_0',
      label: json['label'] ?? 'Healthy',
      confidence: (json['confidence'] as num?)?.toDouble() ?? 0.95,
      bbox: parsedBbox,
      grade: json['grade'] ?? 'Grade A',
      diseaseLabel: json['disease_label'] ?? json['disease'],
      diseaseConfidence: (json['disease_confidence'] as num?)?.toDouble(),
      defects: List<String>.from(json['defects'] ?? []),
    );
  }
}

class OnionBatchReport {
  final String uploadId;
  final DateTime timestamp;
  final int totalOnions;
  final int gradeACount;
  final int ursCount; // Unusable / Rejected Supply
  final double gradeAPercentage;
  final double ursPercentage;
  final Map<String, int> defectBreakdown;
  final List<DetectedOnion> onions;
  final String decision; // APPROVED / REJECTED / MANUAL_INSPECTION
  final List<List<double>> rawBoxes; // Raw bounding boxes before filtering for debug overlay
  final String? overallBatchGrade;
  final Map<String, int> diseaseBreakdown;
  final Map<String, double> diseaseConfidences;
  final String? diseaseError;
  final String? roboflowModelInfo;

  OnionBatchReport({
    required this.uploadId,
    required this.timestamp,
    required this.totalOnions,
    required this.gradeACount,
    required this.ursCount,
    required this.gradeAPercentage,
    required this.ursPercentage,
    required this.defectBreakdown,
    required this.onions,
    required this.decision,
    this.rawBoxes = const [],
    this.overallBatchGrade,
    this.diseaseBreakdown = const {},
    this.diseaseConfidences = const {},
    this.diseaseError,
    this.roboflowModelInfo,
  });

  factory OnionBatchReport.fromJson(Map<String, dynamic> json) {
    var rawOnions = (json['onions'] as List? ?? []);
    List<DetectedOnion> parsedOnions = rawOnions.map((e) => DetectedOnion.fromJson(e)).toList();

    int total = json['total_onions'] ?? parsedOnions.length;
    int gradeA = json['grade_a_count'] ?? parsedOnions.where((o) => o.grade == 'Grade A').length;
    int urs = total - gradeA;

    List<List<double>> parsedRaw = [];
    if (json['raw_boxes'] is List) {
      for (var item in (json['raw_boxes'] as List)) {
        if (item is List) {
          parsedRaw.add(item.map((e) => (e as num).toDouble()).toList());
        }
      }
    }

    return OnionBatchReport(
      uploadId: json['upload_id'] ?? 'BATCH-${DateTime.now().millisecondsSinceEpoch}',
      timestamp: DateTime.now(),
      totalOnions: total,
      gradeACount: gradeA,
      ursCount: urs,
      gradeAPercentage: total > 0 ? (gradeA / total) * 100 : 0.0,
      ursPercentage: total > 0 ? (urs / total) * 100 : 0.0,
      defectBreakdown: Map<String, int>.from(json['defect_breakdown'] ?? {
        'Healthy': gradeA,
        'Damaged': 0,
        'Rotten': 0,
        'Sprouted': 0,
        'Undersized': 0,
      }),
      onions: parsedOnions,
      decision: json['decision'] ?? (total > 0 && (gradeA / total) >= 0.8 ? 'ACCEPTED (GRADE A BATCH)' : 'REJECTED (HIGH URS)'),
      rawBoxes: parsedRaw,
      overallBatchGrade: json['overall_batch_grade'] ?? (total > 0 && (gradeA / total) >= 0.8 ? 'Grade A' : 'Sub-Standard'),
      diseaseBreakdown: Map<String, int>.from(json['disease_breakdown'] ?? {}),
      diseaseConfidences: (json['disease_confidences'] as Map<String, dynamic>?)?.map(
            (k, v) => MapEntry(k, (v as num).toDouble()),
          ) ??
          {},
      diseaseError: json['disease_error'],
      roboflowModelInfo: json['roboflow_model_info'],
    );
  }
}
