import 'package:flutter/material.dart';
import '../main.dart';
import '../services/roboflow_service.dart';
import '../theme/app_colors.dart';
import '../theme/app_icons.dart';
import '../theme/app_spacing.dart';
import '../theme/app_typography.dart';

class SettingsScreen extends StatefulWidget {
  final ValueChanged<bool>? onThemeModeChanged;
  final bool isDarkMode;

  const SettingsScreen({
    super.key,
    this.onThemeModeChanged,
    this.isDarkMode = false,
  });

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  late bool _darkMode;
  bool _offlineCache = true;
  bool _hapticFeedback = true;
  String _selectedLanguage = 'English';
  String _selectedUnits = 'Metric (kg, mm)';
  double _gradeAThreshold = 80.0;
  double _maxUrsThreshold = 20.0;

  @override
  void initState() {
    super.initState();
    _darkMode = appThemeModeNotifier.value == ThemeMode.dark;
  }

  void _showThresholdDialog() {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    double tempGradeA = _gradeAThreshold;

    showDialog(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setDialogState) => AlertDialog(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          title: Text('Procurement Standards', style: AppTypography.headingSmall(isDark)),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Batches meeting this Grade A threshold will be automatically approved:',
                style: AppTypography.bodySmall(isDark),
              ),
              const SizedBox(height: 16),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('Grade A Minimum:'),
                  Text(
                    '${tempGradeA.toStringAsFixed(0)}%',
                    style: const TextStyle(fontWeight: FontWeight.bold, color: AppColors.gradeA),
                  ),
                ],
              ),
              Slider(
                value: tempGradeA,
                min: 60.0,
                max: 95.0,
                divisions: 35,
                activeColor: AppColors.gradeA,
                onChanged: (val) {
                  setDialogState(() {
                    tempGradeA = val;
                  });
                },
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () {
                setState(() {
                  _gradeAThreshold = tempGradeA;
                  _maxUrsThreshold = 100.0 - tempGradeA;
                });
                Navigator.pop(context);
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Procurement thresholds updated.')),
                );
              },
              child: const Text('Save'),
            ),
          ],
        ),
      ),
    );
  }

  void _showRoboflowConfigDialog() {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final controller = TextEditingController(text: RoboflowService.apiKey);

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: Text('Roboflow AI Key', style: AppTypography.headingSmall(isDark)),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              'Configures hosted inference for batch grading and foliar disease pathology detection.',
              style: AppTypography.bodySmall(isDark),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: controller,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'API Key',
                hintText: 'rf_xxxxxxxxxxxxxx',
                prefixIcon: Icon(AppIcons.apiKey, size: 18),
              ),
              obscureText: true,
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () {
              RoboflowService.setApiKey(controller.text);
              Navigator.pop(context);
              setState(() {});
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Roboflow API key saved.')),
              );
            },
            child: const Text('Save'),
          ),
        ],
      ),
    );
  }

  void _showLanguageSelector() {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => Padding(
        padding: AppSpacing.screenPadding.copyWith(top: 20, bottom: 28),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Select Language', style: AppTypography.headingSmall(isDark)),
            const SizedBox(height: 16),
            ...['English', 'Hindi (हिंदी)', 'Marathi (मराठी)'].map((lang) {
              final isSelected = _selectedLanguage == lang;
              return ListTile(
                title: Text(lang, style: TextStyle(fontWeight: isSelected ? FontWeight.bold : FontWeight.normal)),
                trailing: isSelected ? const Icon(AppIcons.check, color: AppColors.primary) : null,
                onTap: () {
                  setState(() {
                    _selectedLanguage = lang;
                  });
                  Navigator.pop(context);
                },
              );
            }),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings & Configuration'),
      ),
      body: ListView(
        padding: AppSpacing.screenPadding,
        children: [
          // User / Procurement Profile Card
          Container(
            padding: AppSpacing.cardPadding,
            decoration: BoxDecoration(
              color: theme.cardTheme.color,
              borderRadius: AppSpacing.roundedCard,
              border: Border.all(
                color: isDark ? AppColors.borderDark : AppColors.borderLight,
              ),
            ),
            child: Row(
              children: [
                Container(
                  width: 50,
                  height: 50,
                  decoration: BoxDecoration(
                    color: (isDark ? AppColors.primaryLight : AppColors.primary).withAlpha(25),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Icon(
                    AppIcons.userCheck,
                    size: 24,
                    color: isDark ? AppColors.primaryLight : AppColors.primary,
                  ),
                ),
                const SizedBox(width: AppSpacing.md),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Senior Produce Inspector', style: AppTypography.titleMedium(isDark)),
                      const SizedBox(height: 2),
                      Text(
                        'Procurement Terminal #260 • Nashik Hub',
                        style: AppTypography.bodySmall(isDark),
                      ),
                    ],
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: AppColors.gradeABg,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: AppColors.gradeABorder),
                  ),
                  child: const Text(
                    'ONLINE',
                    style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: AppColors.gradeA),
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: AppSpacing.lg),

          // Group 1: Preferences & Display
          _buildGroupHeader('App Preferences', isDark),
          _buildSettingsCard([
            _buildSwitchTile(
              icon: AppIcons.moon,
              title: 'Dark Mode',
              subtitle: 'Switch between light and high-contrast dark theme',
              value: _darkMode,
              onChanged: (val) {
                setState(() {
                  _darkMode = val;
                });
                appThemeModeNotifier.value = val ? ThemeMode.dark : ThemeMode.light;
                widget.onThemeModeChanged?.call(val);
              },
              isDark: isDark,
            ),
            const Divider(),
            _buildActionTile(
              icon: AppIcons.language,
              title: 'Language',
              subtitle: _selectedLanguage,
              onTap: _showLanguageSelector,
              isDark: isDark,
            ),
            const Divider(),
            _buildSwitchTile(
              icon: AppIcons.vibrate,
              title: 'Haptic Feedback',
              subtitle: 'Vibration response upon successful scan capture',
              value: _hapticFeedback,
              onChanged: (val) => setState(() => _hapticFeedback = val),
              isDark: isDark,
            ),
          ], isDark),

          const SizedBox(height: AppSpacing.lg),

          // Group 2: Procurement Standards
          _buildGroupHeader('Procurement Rules', isDark),
          _buildSettingsCard([
            _buildActionTile(
              icon: AppIcons.sliders,
              title: 'Quality Grade Thresholds',
              subtitle: 'Grade A >= ${_gradeAThreshold.toStringAsFixed(0)}% • Max URS <= ${_maxUrsThreshold.toStringAsFixed(0)}%',
              onTap: _showThresholdDialog,
              isDark: isDark,
            ),
            const Divider(),
            _buildActionTile(
              icon: AppIcons.scale,
              title: 'Measurement Standard',
              subtitle: _selectedUnits,
              onTap: () {
                setState(() {
                  _selectedUnits = _selectedUnits.contains('Metric')
                      ? 'Imperial (lbs, in)'
                      : 'Metric (kg, mm)';
                });
              },
              isDark: isDark,
            ),
            const Divider(),
            _buildSwitchTile(
              icon: AppIcons.database,
              title: 'Offline Model Caching',
              subtitle: 'Cache model inferences for remote field inspections',
              value: _offlineCache,
              onChanged: (val) => setState(() => _offlineCache = val),
              isDark: isDark,
            ),
          ], isDark),

          const SizedBox(height: AppSpacing.lg),

          // Group 3: AI Inference Services
          _buildGroupHeader('AI & Cloud Inference', isDark),
          _buildSettingsCard([
            _buildActionTile(
              icon: AppIcons.apiKey,
              title: 'Roboflow API Configuration',
              subtitle: RoboflowService.hasApiKey ? 'Connected (Key configured)' : 'Key not configured',
              onTap: _showRoboflowConfigDialog,
              isDark: isDark,
            ),
            const Divider(),
            _buildInfoTile(
              icon: AppIcons.cpu,
              title: 'Local TFLite Segmentation',
              subtitle: 'assets/models/onion_classifier.tflite (Active)',
              isDark: isDark,
            ),
          ], isDark),

          const SizedBox(height: AppSpacing.lg),

          // Group 4: About
          _buildGroupHeader('About', isDark),
          _buildSettingsCard([
            _buildInfoTile(
              icon: AppIcons.info,
              title: 'OnionIQ Mobile',
              subtitle: 'Version 1.0.0 (Build 2026.09)',
              isDark: isDark,
            ),
            const Divider(),
            _buildInfoTile(
              icon: AppIcons.shieldCheck,
              title: 'Compliance & Quality Standards',
              subtitle: 'APMC Agricultural Grade Verification Standard',
              isDark: isDark,
            ),
          ], isDark),

          const SizedBox(height: AppSpacing.xxl),
        ],
      ),
    );
  }

  Widget _buildGroupHeader(String title, bool isDark) {
    return Padding(
      padding: const EdgeInsets.only(left: 4, bottom: 8),
      child: Text(
        title,
        style: TextStyle(
          fontSize: 12,
          fontWeight: FontWeight.w700,
          letterSpacing: 0.5,
          color: isDark ? AppColors.textMutedDark : AppColors.textMutedLight,
        ),
      ),
    );
  }

  Widget _buildSettingsCard(List<Widget> children, bool isDark) {
    return Container(
      decoration: BoxDecoration(
        color: Theme.of(context).cardTheme.color,
        borderRadius: AppSpacing.roundedCard,
        border: Border.all(
          color: isDark ? AppColors.borderDark : AppColors.borderLight,
        ),
      ),
      child: Column(children: children),
    );
  }

  Widget _buildSwitchTile({
    required IconData icon,
    required String title,
    required String subtitle,
    required bool value,
    required ValueChanged<bool> onChanged,
    required bool isDark,
  }) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
      child: Row(
        children: [
          Icon(icon, size: 20, color: isDark ? AppColors.textSecondaryDark : AppColors.textSecondaryLight),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: AppTypography.titleMedium(isDark)),
                const SizedBox(height: 2),
                Text(subtitle, style: AppTypography.bodySmall(isDark)),
              ],
            ),
          ),
          Switch(
            value: value,
            activeThumbColor: isDark ? AppColors.primaryLight : AppColors.primary,
            onChanged: onChanged,
          ),
        ],
      ),
    );
  }

  Widget _buildActionTile({
    required IconData icon,
    required String title,
    required String subtitle,
    required VoidCallback onTap,
    required bool isDark,
  }) {
    return InkWell(
      onTap: onTap,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
        child: Row(
          children: [
            Icon(icon, size: 20, color: isDark ? AppColors.textSecondaryDark : AppColors.textSecondaryLight),
            const SizedBox(width: 14),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title, style: AppTypography.titleMedium(isDark)),
                  const SizedBox(height: 2),
                  Text(subtitle, style: AppTypography.bodySmall(isDark)),
                ],
              ),
            ),
            Icon(AppIcons.chevronRight, size: 16, color: isDark ? AppColors.textMutedDark : AppColors.textMutedLight),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoTile({
    required IconData icon,
    required String title,
    required String subtitle,
    required bool isDark,
  }) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
      child: Row(
        children: [
          Icon(icon, size: 20, color: isDark ? AppColors.textSecondaryDark : AppColors.textSecondaryLight),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: AppTypography.titleMedium(isDark)),
                const SizedBox(height: 2),
                Text(subtitle, style: AppTypography.bodySmall(isDark)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
