import 'package:flutter/material.dart';

/// 8pt spacing grid system, consistent corner radii (16-20px for cards),
/// minimum 48px touch targets, and subtle shadows.
class AppSpacing {
  // Spacing Scale
  static const double xxs = 4.0;
  static const double xs = 8.0;
  static const double sm = 12.0;
  static const double md = 16.0;
  static const double lg = 20.0;
  static const double xl = 24.0;
  static const double xxl = 32.0;
  static const double xxxl = 40.0;
  static const double huge = 48.0;

  // Minimum Touch Target
  static const double minTouchTarget = 48.0;

  // Corner Radii
  static const double radiusXs = 6.0;
  static const double radiusSm = 10.0;
  static const double radiusMd = 14.0;
  static const double radiusCard = 18.0; // Standard 16-20px card radius
  static const double radiusLg = 22.0;
  static const double radiusFull = 999.0;

  static final BorderRadius roundedCard = BorderRadius.circular(radiusCard);
  static final BorderRadius roundedSm = BorderRadius.circular(radiusSm);
  static final BorderRadius roundedMd = BorderRadius.circular(radiusMd);
  static final BorderRadius roundedLg = BorderRadius.circular(radiusLg);
  static final BorderRadius roundedFull = BorderRadius.circular(radiusFull);

  // Common Paddings
  static const EdgeInsets screenPadding = EdgeInsets.symmetric(horizontal: 16.0, vertical: 12.0);
  static const EdgeInsets cardPadding = EdgeInsets.all(16.0);
  static const EdgeInsets cardPaddingCompact = EdgeInsets.all(12.0);
  static const EdgeInsets chipPadding = EdgeInsets.symmetric(horizontal: 10.0, vertical: 5.0);

  // Subtle Box Shadows
  static const List<BoxShadow> cardShadowLight = [
    BoxShadow(
      color: Color(0x0A000000),
      offset: Offset(0, 2),
      blurRadius: 8,
      spreadRadius: 0,
    ),
  ];

  static const List<BoxShadow> elevatedShadowLight = [
    BoxShadow(
      color: Color(0x12000000),
      offset: Offset(0, 4),
      blurRadius: 16,
      spreadRadius: 0,
    ),
  ];

  static const List<BoxShadow> cardShadowDark = [
    BoxShadow(
      color: Color(0x28000000),
      offset: Offset(0, 2),
      blurRadius: 8,
      spreadRadius: 0,
    ),
  ];
}
