import 'package:flutter/material.dart';
import '../theme/app_colors.dart';
import '../theme/app_icons.dart';
import 'dashboard_screen.dart';
import 'history_screen.dart';
import 'scan_screen.dart';
import 'settings_screen.dart';

class ShellNavigation extends StatefulWidget {
  final ValueChanged<bool>? onThemeModeChanged;
  final bool isDarkMode;

  const ShellNavigation({
    super.key,
    this.onThemeModeChanged,
    this.isDarkMode = false,
  });

  @override
  State<ShellNavigation> createState() => _ShellNavigationState();
}

class _ShellNavigationState extends State<ShellNavigation> {
  int _currentIndex = 0;

  void _navigateToScan() {
    setState(() {
      _currentIndex = 1;
    });
  }

  void _navigateToHistory() {
    setState(() {
      _currentIndex = 2;
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    final screens = [
      DashboardScreen(
        onNavigateToScan: _navigateToScan,
        onNavigateToHistory: _navigateToHistory,
      ),
      const ScanScreen(),
      const HistoryScreen(),
      SettingsScreen(
        onThemeModeChanged: widget.onThemeModeChanged,
        isDarkMode: widget.isDarkMode,
      ),
    ];

    return Scaffold(
      body: IndexedStack(
        index: _currentIndex,
        children: screens,
      ),
      bottomNavigationBar: Container(
        decoration: BoxDecoration(
          color: theme.scaffoldBackgroundColor,
          border: Border(
            top: BorderSide(
              color: isDark ? AppColors.borderDark : AppColors.borderLight,
              width: 1,
            ),
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 6.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _buildNavItem(
                  index: 0,
                  icon: AppIcons.dashboard,
                  label: 'Dashboard',
                  isSelected: _currentIndex == 0,
                  isDark: isDark,
                ),
                // Emphasized Scan Action Button in Center
                _buildEmphasizedScanButton(
                  isSelected: _currentIndex == 1,
                  isDark: isDark,
                ),
                _buildNavItem(
                  index: 2,
                  icon: AppIcons.history,
                  label: 'History',
                  isSelected: _currentIndex == 2,
                  isDark: isDark,
                ),
                _buildNavItem(
                  index: 3,
                  icon: AppIcons.settings,
                  label: 'Settings',
                  isSelected: _currentIndex == 3,
                  isDark: isDark,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildNavItem({
    required int index,
    required IconData icon,
    required String label,
    required bool isSelected,
    required bool isDark,
  }) {
    final selectedColor = isDark ? AppColors.primaryLight : AppColors.primary;
    final unselectedColor = isDark ? AppColors.textMutedDark : AppColors.textMutedLight;

    return InkWell(
      onTap: () => setState(() => _currentIndex = index),
      borderRadius: BorderRadius.circular(12),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              icon,
              size: 22,
              color: isSelected ? selectedColor : unselectedColor,
            ),
            const SizedBox(height: 3),
            Text(
              label,
              style: TextStyle(
                fontSize: 11,
                fontWeight: isSelected ? FontWeight.w700 : FontWeight.w500,
                color: isSelected ? selectedColor : unselectedColor,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEmphasizedScanButton({
    required bool isSelected,
    required bool isDark,
  }) {
    return GestureDetector(
      onTap: () => setState(() => _currentIndex = 1),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 8),
        decoration: BoxDecoration(
          color: AppColors.secondary,
          borderRadius: BorderRadius.circular(24),
          boxShadow: [
            BoxShadow(
              color: AppColors.secondary.withAlpha(isDark ? 90 : 70),
              blurRadius: 10,
              offset: const Offset(0, 3),
            ),
          ],
        ),
        child: const Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(AppIcons.scan, color: Colors.white, size: 20),
            SizedBox(width: 6),
            Text(
              'Scan Tray',
              style: TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.w700,
                fontSize: 12,
                letterSpacing: 0.2,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
