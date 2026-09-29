import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class RoboflowPrediction {
  final double x;
  final double y;
  final double width;
  final double height;
  final String className;
  final double confidence;

  RoboflowPrediction({
    required this.x,
    required this.y,
    required this.width,
    required this.height,
    required this.className,
    required this.confidence,
  });

  factory RoboflowPrediction.fromJson(Map<String, dynamic> json) {
    return RoboflowPrediction(
      x: (json['x'] as num?)?.toDouble() ?? 0.0,
      y: (json['y'] as num?)?.toDouble() ?? 0.0,
      width: (json['width'] as num?)?.toDouble() ?? 0.0,
      height: (json['height'] as num?)?.toDouble() ?? 0.0,
      className: json['class']?.toString() ??
          json['class_name']?.toString() ??
          json['name']?.toString() ??
          json['label']?.toString() ??
          json['top']?.toString() ??
          'onion',
      confidence: (json['confidence'] as num?)?.toDouble() ?? 0.0,
    );
  }
}

class RoboflowInferenceResult {
  final bool isSuccess;
  final String modelId;
  final List<RoboflowPrediction> predictions;
  final String? batchGrade; // e.g. Grade A, Spoiled, Double Split, Sprouted
  final Map<String, int> classCounts;
  final Map<String, double> classConfidences;
  final String? errorMessage;

  RoboflowInferenceResult({
    required this.isSuccess,
    required this.modelId,
    required this.predictions,
    this.batchGrade,
    required this.classCounts,
    this.classConfidences = const {},
    this.errorMessage,
  });
}

class RoboflowService {
  // Built-in --dart-define fallback with dynamic in-app override
  static String _apiKey = const String.fromEnvironment('ROBOFLOW_API_KEY', defaultValue: 'qven1LQPSAzHloNcHRKL');
  
  // Model 1: Batch Quality Grading (veg1-hcqsf/2 on Roboflow Universe, workspace onion-grading-nx)
  static String gradingModelEndpoint = const String.fromEnvironment('ROBOFLOW_GRADING_MODEL', defaultValue: 'https://detect.roboflow.com/veg1-hcqsf/2');

  // Model 2: Hosted Onion Disease Model (workspace: school-0xa1n, project: onion-disease-capstone-final/2)
  static String diseaseModelEndpoint = const String.fromEnvironment('ROBOFLOW_DISEASE_MODEL', defaultValue: 'https://detect.roboflow.com/onion-disease-capstone-final/2');

  static String get apiKey => _apiKey;
  static bool get hasApiKey => _apiKey.isNotEmpty;

  static void setApiKey(String key) {
    _apiKey = key.trim();
  }

  static void setDiseaseModel(String endpointOrModelId) {
    if (endpointOrModelId.startsWith('http')) {
      diseaseModelEndpoint = endpointOrModelId;
    } else {
      diseaseModelEndpoint = 'https://detect.roboflow.com/$endpointOrModelId';
    }
  }

  /// Evaluates batch quality grading using Roboflow hosted model "veg1-hcqsf/2"
  /// Classes: onion, Black smut, double_split, Spoiled, sprouted
  static Future<RoboflowInferenceResult> inferBatchGrading(File imageFile) async {
    return _callRoboflowModel(gradingModelEndpoint, imageFile, 'veg1-hcqsf/2');
  }

  /// Evaluates foliar and bulb disease detection using hosted Roboflow model
  /// Classes: Healthy, Rust, Downy Mildew, Purple Blotch, Botrytis Leaf Blight
  static Future<RoboflowInferenceResult> inferDiseaseDetection(File imageFile) async {
    return _callRoboflowModel(diseaseModelEndpoint, imageFile, 'onion-disease');
  }

  static Future<RoboflowInferenceResult> _callRoboflowModel(String endpoint, File imageFile, String modelTag) async {
    if (!hasApiKey) {
      return RoboflowInferenceResult(
        isSuccess: false,
        modelId: modelTag,
        predictions: [],
        classCounts: {},
        errorMessage: 'Roboflow API key not configured. Add via --dart-define=ROBOFLOW_API_KEY=your_key or in Settings.',
      );
    }

    try {
      final bytes = await imageFile.readAsBytes();
      final base64Image = base64Encode(bytes);

      final int confThreshold = modelTag.contains('disease') ? 20 : 40;
      final uri = Uri.parse('$endpoint?api_key=$_apiKey&confidence=$confThreshold&overlap=35');

      final response = await http.post(
        uri,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json',
        },
        body: base64Image,
      ).timeout(const Duration(seconds: 15));

      if (response.statusCode != 200) {
        return RoboflowInferenceResult(
          isSuccess: false,
          modelId: modelTag,
          predictions: [],
          classCounts: {},
          errorMessage: 'Roboflow API error (${response.statusCode}): ${response.body}',
        );
      }

      final Map<String, dynamic> data = jsonDecode(response.body);
      final List<dynamic> rawPredictions = [];
      if (data['predictions'] is List) {
        rawPredictions.addAll(data['predictions']);
      } else if (data['predictions'] is Map) {
        final Map pMap = data['predictions'];
        pMap.forEach((key, val) {
          if (val is Map) {
            rawPredictions.add({'class': key, 'confidence': val['confidence'] ?? 1.0});
          } else if (val is num) {
            rawPredictions.add({'class': key, 'confidence': val.toDouble()});
          }
        });
      } else if (data.containsKey('top')) {
        rawPredictions.add({'class': data['top'], 'confidence': data['confidence'] ?? 1.0});
      }
      final List<RoboflowPrediction> predictions = rawPredictions
          .whereType<Map<String, dynamic>>()
          .map((p) => RoboflowPrediction.fromJson(p))
          .toList();

      final Map<String, int> counts = {};
      final Map<String, double> confidences = {};
      for (final p in predictions) {
        counts[p.className] = (counts[p.className] ?? 0) + 1;
        if (!confidences.containsKey(p.className) || p.confidence > confidences[p.className]!) {
          confidences[p.className] = p.confidence;
        }
      }

      // If disease model executed with 0 lesion detections, bulb/foliage is verified Healthy
      if (modelTag.contains('disease') && predictions.isEmpty) {
        counts['Healthy (No Lesions)'] = 1;
        confidences['Healthy (No Lesions)'] = 1.0;
      }

      // Determine overall batch grade
      String batchGrade = 'Grade A (Procurement Standard)';
      if ((counts['Spoiled'] ?? 0) > 0 || (counts['Black smut'] ?? 0) > 0) {
        batchGrade = 'Rejected - Spoilage / Black Smut Detected';
      } else if ((counts['double_split'] ?? 0) > 0) {
        batchGrade = 'Grade B - Split Bulbs Present';
      } else if ((counts['sprouted'] ?? 0) > 0) {
        batchGrade = 'Rejected - Sprouted Bulbs';
      }

      return RoboflowInferenceResult(
        isSuccess: true,
        modelId: modelTag,
        predictions: predictions,
        batchGrade: batchGrade,
        classCounts: counts,
        classConfidences: confidences,
      );
    } catch (e) {
      return RoboflowInferenceResult(
        isSuccess: false,
        modelId: modelTag,
        predictions: [],
        classCounts: {},
        classConfidences: {},
        errorMessage: 'Connection to Roboflow hosted inference failed: $e',
      );
    }
  }
}
