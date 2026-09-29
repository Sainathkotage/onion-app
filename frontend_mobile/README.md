# OnionIQ Mobile — Flutter Application

OnionIQ Mobile is a Flutter application designed for procurement centers to photograph onion batches, detect individual onions, classify defect classes (`Healthy`, `Damaged`, `Rotten`, `Sprouted`, `Undersized`), calculate Grade A vs URS (Unusable / Rejected Supply) percentages, and export digital PDF quality reports.

---

## Features

- **Procurement Dashboard**: Tracks overall procurement metrics, Grade A compliance, and historical scan logs.
- **Onion Tray Camera & Scanner**: High-resolution tray scanner with auto-focus guides.
- **Defect Tagging & Bounding Boxes**: Visual detection overlay for Healthy, Damaged, Rotten, Sprouted, and Undersized onions.
- **Grade A vs URS Ratio Calculation**: Immediate percentage breakdown against baseline procurement standards.
- **Digital PDF Export**: Generates printable and shareable quality reports.

---

## Local Development & Setup

### Prerequisites

- Flutter SDK (>= 3.0.0)
- Android Studio / Xcode for simulator testing or connected physical device

### Commands

```bash
# Navigate to mobile frontend directory
cd frontend_mobile

# Get dependencies
flutter pub get

# Run on connected device / emulator
flutter run
```

---

## API Backend Integration

The app connects to the FastAPI backend at `http://<your-backend-ip>:8000/api/upload`. Update `lib/services/api_service.dart` with your network server IP address when testing on a physical phone.
