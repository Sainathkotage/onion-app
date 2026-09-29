import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:onion_iq_mobile/main.dart';
import 'package:onion_iq_mobile/screens/dashboard_screen.dart';
import 'package:onion_iq_mobile/screens/history_screen.dart';
import 'package:onion_iq_mobile/screens/batch_compare_screen.dart';

void main() {
  testWidgets('OnionIQ App smoke test - launches and renders onboarding', (WidgetTester tester) async {
    await tester.pumpWidget(const OnionIQApp());
    expect(find.text('OnionIQ'), findsOneWidget);
    expect(find.text('Place Onions on Tray'), findsOneWidget);
  });

  testWidgets('DashboardScreen renders KPIs and charts', (WidgetTester tester) async {
    await tester.binding.setSurfaceSize(const Size(400, 900));
    await tester.pumpWidget(
      const MaterialApp(
        home: DashboardScreen(),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('Good Morning, Inspector'), findsOneWidget);
    expect(find.text('Total Scans'), findsOneWidget);
    expect(find.text('Avg Quality Score'), findsOneWidget);
  });

  testWidgets('HistoryScreen renders search and records', (WidgetTester tester) async {
    await tester.binding.setSurfaceSize(const Size(400, 900));
    await tester.pumpWidget(
      const MaterialApp(
        home: HistoryScreen(),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('Inspection History'), findsOneWidget);
    expect(find.byType(TextField), findsOneWidget);
  });

  testWidgets('BatchCompareScreen renders comparison metrics', (WidgetTester tester) async {
    await tester.binding.setSurfaceSize(const Size(400, 900));
    await tester.pumpWidget(
      const MaterialApp(
        home: BatchCompareScreen(),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('Batch Lot Comparison'), findsOneWidget);
    expect(find.text('Quality & Yield Metrics'), findsOneWidget);
  });
}
