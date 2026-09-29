import 'package:flutter/material.dart';
import '../theme/app_colors.dart';
import '../theme/app_icons.dart';
import '../theme/app_spacing.dart';
import '../theme/app_typography.dart';
import '../widgets/app_button.dart';
import 'shell_navigation.dart';

class SplashOnboardingScreen extends StatefulWidget {
  const SplashOnboardingScreen({super.key});

  @override
  State<SplashOnboardingScreen> createState() => _SplashOnboardingScreenState();
}

class _SplashOnboardingScreenState extends State<SplashOnboardingScreen> {
  final PageController _pageController = PageController();
  int _currentPage = 0;

  final List<_OnboardingSlide> _slides = const [
    _OnboardingSlide(
      icon: AppIcons.gridFour,
      title: 'Place Onions on Tray',
      description:
          'Spread onions in a single, unstacked layer across the inspection tray on a clean, flat surface.',
    ),
    _OnboardingSlide(
      icon: AppIcons.camera,
      title: 'Top-Down Capture',
      description:
          'Align the camera parallel to the tray within corner guides under uniform, diffused lighting.',
    ),
    _OnboardingSlide(
      icon: AppIcons.fileCheck,
      title: 'Instant Quality Report',
      description:
          'Get automated defect segmentation, Grade A vs URS ratio, disease pathology, and procurement decisions.',
    ),
  ];

  void _finishOnboarding() {
    Navigator.pushReplacement(
      context,
      PageRouteBuilder(
        pageBuilder: (context, anim1, anim2) => const ShellNavigation(),
        transitionsBuilder: (context, anim, secondaryAnim, child) {
          return FadeTransition(opacity: anim, child: child);
        },
        transitionDuration: const Duration(milliseconds: 350),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            // Top Bar with Minimal Logo & Skip Button
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg, vertical: AppSpacing.md),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
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
                      Text(
                        'OnionIQ',
                        style: AppTypography.headingSmall(isDark).copyWith(
                          fontWeight: FontWeight.w800,
                          letterSpacing: -0.3,
                        ),
                      ),
                    ],
                  ),
                  if (_currentPage < _slides.length - 1)
                    TextButton(
                      onPressed: _finishOnboarding,
                      child: Text(
                        'Skip',
                        style: TextStyle(
                          color: isDark ? AppColors.textMutedDark : AppColors.textMutedLight,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    )
                  else
                    const SizedBox(height: 36),
                ],
              ),
            ),

            // Page View Carousel
            Expanded(
              child: PageView.builder(
                controller: _pageController,
                itemCount: _slides.length,
                onPageChanged: (idx) {
                  setState(() {
                    _currentPage = idx;
                  });
                },
                itemBuilder: (context, index) {
                  final slide = _slides[index];
                  return Padding(
                    padding: const EdgeInsets.symmetric(horizontal: AppSpacing.xl),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        // Icon Illustration Container
                        Container(
                          width: 140,
                          height: 140,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            color: (isDark ? AppColors.primaryLight : AppColors.primary).withAlpha(20),
                            border: Border.all(
                              color: (isDark ? AppColors.primaryLight : AppColors.primary).withAlpha(50),
                              width: 2,
                            ),
                          ),
                          child: Icon(
                            slide.icon,
                            size: 64,
                            color: isDark ? AppColors.primaryLight : AppColors.primary,
                          ),
                        ),
                        const SizedBox(height: AppSpacing.xxl),

                        Text(
                          slide.title,
                          textAlign: TextAlign.center,
                          style: AppTypography.displayMedium(isDark),
                        ),
                        const SizedBox(height: AppSpacing.md),

                        Text(
                          slide.description,
                          textAlign: TextAlign.center,
                          style: AppTypography.bodyLarge(isDark),
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),

            // Bottom Navigation Indicators & Buttons
            Padding(
              padding: const EdgeInsets.all(AppSpacing.xl),
              child: Column(
                children: [
                  // Dot Indicators
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: List.generate(_slides.length, (idx) {
                      final isSelected = _currentPage == idx;
                      return AnimatedContainer(
                        duration: const Duration(milliseconds: 250),
                        margin: const EdgeInsets.symmetric(horizontal: 4),
                        width: isSelected ? 24 : 8,
                        height: 8,
                        decoration: BoxDecoration(
                          color: isSelected
                              ? (isDark ? AppColors.primaryLight : AppColors.primary)
                              : (isDark ? AppColors.surfaceVariantDark : AppColors.borderLight),
                          borderRadius: BorderRadius.circular(4),
                        ),
                      );
                    }),
                  ),
                  const SizedBox(height: AppSpacing.xl),

                  // Action Button
                  AppButton(
                    width: double.infinity,
                    label: _currentPage == _slides.length - 1 ? 'Get Started' : 'Next',
                    icon: _currentPage == _slides.length - 1
                        ? AppIcons.arrowRight
                        : AppIcons.chevronRight,
                    onPressed: () {
                      if (_currentPage < _slides.length - 1) {
                        _pageController.nextPage(
                          duration: const Duration(milliseconds: 300),
                          curve: Curves.easeInOut,
                        );
                      } else {
                        _finishOnboarding();
                      }
                    },
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _OnboardingSlide {
  final IconData icon;
  final String title;
  final String description;

  const _OnboardingSlide({
    required this.icon,
    required this.title,
    required this.description,
  });
}
