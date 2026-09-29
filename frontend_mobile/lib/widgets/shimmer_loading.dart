import 'package:flutter/material.dart';
import '../theme/app_colors.dart';
import '../theme/app_spacing.dart';

class ShimmerSkeleton extends StatefulWidget {
  final double width;
  final double height;
  final double borderRadius;

  const ShimmerSkeleton({
    super.key,
    required this.width,
    required this.height,
    this.borderRadius = 8,
  });

  @override
  State<ShimmerSkeleton> createState() => _ShimmerSkeletonState();
}

class _ShimmerSkeletonState extends State<ShimmerSkeleton>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1400),
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final baseColor = isDark ? AppColors.surfaceVariantDark : Colors.grey.shade200;
    final highlightColor = isDark ? const Color(0xFF2E3440) : Colors.grey.shade100;

    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return Container(
          width: widget.width,
          height: widget.height,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(widget.borderRadius),
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [baseColor, highlightColor, baseColor],
              stops: [
                (_controller.value - 0.3).clamp(0.0, 1.0),
                _controller.value,
                (_controller.value + 0.3).clamp(0.0, 1.0),
              ],
            ),
          ),
        );
      },
    );
  }
}

class DashboardSkeletonLoader extends StatelessWidget {
  const DashboardSkeletonLoader({super.key});

  @override
  Widget build(BuildContext context) {
    return const SingleChildScrollView(
      padding: AppSpacing.screenPadding,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          ShimmerSkeleton(width: 180, height: 28, borderRadius: 8),
          SizedBox(height: AppSpacing.xs),
          ShimmerSkeleton(width: 260, height: 16, borderRadius: 6),
          SizedBox(height: AppSpacing.lg),
          ShimmerSkeleton(width: double.infinity, height: 130, borderRadius: 16),
          SizedBox(height: AppSpacing.lg),
          Row(
            children: [
              Expanded(child: ShimmerSkeleton(width: double.infinity, height: 110, borderRadius: 16)),
              SizedBox(width: AppSpacing.sm),
              Expanded(child: ShimmerSkeleton(width: double.infinity, height: 110, borderRadius: 16)),
            ],
          ),
          SizedBox(height: AppSpacing.sm),
          Row(
            children: [
              Expanded(child: ShimmerSkeleton(width: double.infinity, height: 110, borderRadius: 16)),
              SizedBox(width: AppSpacing.sm),
              Expanded(child: ShimmerSkeleton(width: double.infinity, height: 110, borderRadius: 16)),
            ],
          ),
          SizedBox(height: AppSpacing.xl),
          ShimmerSkeleton(width: double.infinity, height: 220, borderRadius: 16),
        ],
      ),
    );
  }
}
