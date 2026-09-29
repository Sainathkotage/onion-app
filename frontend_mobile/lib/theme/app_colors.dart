import 'package:flutter/material.dart';

/// Central color palette inspired by onions and agricultural produce.
/// Features deep red-onion plum primary, warm harvest amber secondary,
/// and standardized semantic grading tokens.
class AppColors {
  // Brand Colors - Onion Produce Palette
  static const Color primary = Color(0xFF5C1D42); // Deep Red Onion Plum
  static const Color primaryLight = Color(0xFF7E2A5C);
  static const Color primaryDark = Color(0xFF3F112D);
  static const Color primaryContainer = Color(0xFFFBEBF3);
  static const Color onPrimaryContainer = Color(0xFF3F112D);

  static const Color secondary = Color(0xFFD97706); // Warm Golden Harvest Amber
  static const Color secondaryLight = Color(0xFFFBBF24);
  static const Color secondaryDark = Color(0xFFB45309);
  static const Color secondaryContainer = Color(0xFFFEF3C7);
  static const Color onSecondaryContainer = Color(0xFF78350F);

  // Semantic Quality Grading Colors
  static const Color gradeA = Color(0xFF10B981); // Emerald Green - Grade A
  static const Color gradeABg = Color(0xFFECFDF5);
  static const Color gradeABorder = Color(0xFFA7F3D0);

  static const Color gradeB = Color(0xFFF59E0B); // Amber/Gold - Grade B
  static const Color gradeBBg = Color(0xFFFFFBEB);
  static const Color gradeBBorder = Color(0xFFFDE68A);

  static const Color gradeC = Color(0xFFF97316); // Orange - Grade C
  static const Color gradeCBg = Color(0xFFFFF7ED);
  static const Color gradeCBorder = Color(0xFFFED7AA);

  static const Color reject = Color(0xFFEF4444); // Crimson Red - Reject / URS
  static const Color rejectBg = Color(0xFFFEF2F2);
  static const Color rejectBorder = Color(0xFFFECACA);

  // Neutral Colors - Light Mode
  static const Color bgLight = Color(0xFFF8F9FA); // Soft off-white
  static const Color surfaceLight = Color(0xFFFFFFFF);
  static const Color surfaceVariantLight = Color(0xFFF1F3F5);
  static const Color borderLight = Color(0xFFE5E7EB);
  static const Color textPrimaryLight = Color(0xFF111827);
  static const Color textSecondaryLight = Color(0xFF4B5563);
  static const Color textMutedLight = Color(0xFF9CA3AF);

  // Neutral Colors - Dark Mode
  static const Color bgDark = Color(0xFF0F1115);
  static const Color surfaceDark = Color(0xFF171A21);
  static const Color surfaceVariantDark = Color(0xFF222631);
  static const Color borderDark = Color(0xFF2E3440);
  static const Color textPrimaryDark = Color(0xFFF9FAFB);
  static const Color textSecondaryDark = Color(0xFFD1D5DB);
  static const Color textMutedDark = Color(0xFF6B7280);

  // Accent and Category Colors (for defect breakdown charts)
  static const Color defectSprouting = Color(0xFF8B5CF6); // Purple
  static const Color defectRot = Color(0xFFEF4444); // Red
  static const Color defectBruising = Color(0xFFF59E0B); // Amber
  static const Color defectDiscoloration = Color(0xFF06B6D4); // Cyan
  static const Color defectCracks = Color(0xFFF97316); // Orange
  static const Color defectUndersized = Color(0xFF64748B); // Slate

  // Helper method for quality grade color
  static Color getGradeColor(String grade) {
    final g = grade.toUpperCase();
    if (g.contains('A')) return gradeA;
    if (g.contains('B')) return gradeB;
    if (g.contains('C')) return gradeC;
    if (g.contains('REJECT') || g.contains('URS') || g.contains('SUB')) return reject;
    return textSecondaryLight;
  }

  static Color getGradeBgColor(String grade, {bool isDark = false}) {
    if (isDark) {
      return getGradeColor(grade).withAlpha(40);
    }
    final g = grade.toUpperCase();
    if (g.contains('A')) return gradeABg;
    if (g.contains('B')) return gradeBBg;
    if (g.contains('C')) return gradeCBg;
    if (g.contains('REJECT') || g.contains('URS') || g.contains('SUB')) return rejectBg;
    return surfaceVariantLight;
  }

  static Color getGradeBorderColor(String grade, {bool isDark = false}) {
    if (isDark) {
      return getGradeColor(grade).withAlpha(80);
    }
    final g = grade.toUpperCase();
    if (g.contains('A')) return gradeABorder;
    if (g.contains('B')) return gradeBBorder;
    if (g.contains('C')) return gradeCBorder;
    if (g.contains('REJECT') || g.contains('URS') || g.contains('SUB')) return rejectBorder;
    return borderLight;
  }
}
