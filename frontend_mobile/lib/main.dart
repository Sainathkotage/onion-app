import 'package:flutter/material.dart';
import 'screens/splash_onboarding_screen.dart';
import 'theme/app_theme.dart';

final ValueNotifier<ThemeMode> appThemeModeNotifier = ValueNotifier<ThemeMode>(ThemeMode.light);

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const OnionIQApp());
}

class OnionIQApp extends StatelessWidget {
  const OnionIQApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<ThemeMode>(
      valueListenable: appThemeModeNotifier,
      builder: (context, currentThemeMode, _) {
        return MaterialApp(
          title: 'OnionIQ Mobile',
          debugShowCheckedModeBanner: false,
          theme: AppTheme.lightTheme,
          darkTheme: AppTheme.darkTheme,
          themeMode: currentThemeMode,
          home: const SplashOnboardingScreen(),
        );
      },
    );
  }
}
