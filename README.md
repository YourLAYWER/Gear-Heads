# 🤖 Autonomous Multi-Sensor AGV & Line-Following Vehicle

An industrial-inspired autonomous mobile robot engineered in **MicroPython (Pybricks)** using the LEGO Mindstorms EV3 architecture. Designed to simulate modern factory floor **Automated Guided Vehicles (AGVs)**, this project replaces rigid, hardcoded paths with a closed-loop **Proportional (P) Control** navigation system, dynamic ambient calibration, two-stage obstacle verification, and gyro-assisted path recovery.

---

## 🌟 Key Features

* **Dynamic Light Calibration:** Eliminates hardcoded reflection values by sampling local floor conditions before launch to compute an accurate midpoint threshold ($\text{Threshold} = \frac{\text{Black} + \text{White}}{2}$).
* **Proportional (P) Control Loop:** Smooth, high-frequency line edge-following using closed-loop proportional error correction ($\text{Steering} = \text{Color Error} \times \text{COLOR\_GAIN}$) to prevent jagged overshooting.
* **Multi-Sensor Fusion:** Synchronizes three concurrent sensor inputs (Color, Ultrasonic, and Gyro) alongside drive motor encoders to manage navigation, safety, and path recovery.
* **Two-Step Obstacle Verification:** Prevents false-positive stops from transient sensor noise by pausing, re-sampling the distance via Ultrasonic sensor, and only executing avoidance maneuvers when an obstacle is confirmed.
* **Gyro-Bounded Arc-Search:** Operates a closed-loop 180° sweep at 200 Hz sampling frequency using the Gyro sensor to reliably relocate and lock back onto the track after navigating around obstacles.
* **Interactive Auditory & Visual Telemetry:** Displays calibrated thresholds on-screen and provides status updates via built-in Text-to-Speech (TTS).

---

## 📐 Hardware & Port Mapping

| Component | Port | Description |
| :--- | :--- | :--- |
| **Left Drive Motor** | `Port B` | Left wheel drive motor |
| **Right Drive Motor** | `Port C` | Right wheel drive motor |
| **Color Sensor** | `Port S3` | Surface reflection measurement and color detection |
| **Ultrasonic Sensor**| `Port S4` | Distance tracking and obstacle detection |
| **Gyro Sensor** | `Port S1` | Angle tracking during arc-search recovery |

---

## 🏗️ System Logic & Control Flow

```mermaid
flowchart TD
    A[Start Program] --> B[Interactive Calibration: Black, White, Red]
    B --> C[Compute Dynamic THRESHOLD]
    C --> D[Initialize Line Following Loop]
    
    D --> E{Check Finish Line: Color.RED?}
    E -- Yes --> F[Stop Robot & Mission Complete]
    E -- No --> G{Check Ultrasonic Distance}
    
    G -- Object < Target + 10mm --> H[Stop Drive & Pause]
    H --> I{Re-verify Distance}
    I -- Verified --> J[Execute Avoidance Geometry]
    J --> K[Run Gyro Arc-Search]
    K -- Line Found --> D
    K -- Line Not Found --> L[Stop Safety Abort]
    
    I -- False Alarm --> D
    G -- Clear Track --> M[Calculate Proportional Steering]
    M --> N[Apply Motor Speeds & Repeat Loop] --> D
