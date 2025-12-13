# 🎄 GnomeBot CAN Bus Protocol - Top Secret Workshop Edition!

Ho ho hold on there! Welcome to the inner workings of the GnomeBot's communication system. This marvelous contraption uses the **CAN (Controller Area Network)** bus to chatter away about its status and sometimes even listen to requests. It's like the reindeer telegraph, but with more wires and less sneezing.

This document details the known signals whizzing around on the `gcan0` interface. Remember, all multi-byte values are sent **Big Endian** (Most Significant Byte first), just like how Santa lists the nicest kids first!

---
## 🎁 CAN Data Requests (Client -> GnomeBot )

Sometimes, you need to poke the GnomeBot to get specific information *right now*. Send one of these messages, and the *should* reply with the corresponding Status/Data message (see below).

| CAN ID (Hex) | Constant Name             | Description                                         | Data Sent |
| ------------ | ------------------------- | --------------------------------------------------- | --------- |
| `0x400`      | `requestBatteryVoltageID` | Asks for the current battery voltage reading.       | (Empty)   |
| `0x410`      | `requestMotorSpeedLeftID` | Requests the current speed of the left motor.       | (Empty)   |
| `0x460`      | `requestSystemTempID`     | Asks for the GnomeBot's internal temperature.       | (Empty)   |
| `0x470`      | `requestGPSFixID`         | Inquires about the current GPS fix status.          | (Empty)   |
| `0x4C0`      | `requestPayloadStatusID`  | Requests the current status of the payload/gripper. | (Empty    |

---

## ✨ CAN Status & Data Responses (GnomeBot -> Client)

These messages are the GnomeBot telling the world (or at least the CAN bus) what's going on. Some are sent automatically like clockwork (Periodic), some only when asked (Response Only), and some do both!

| (Hex)   | Constant Name                | Behavior            | Data Bytes | Data Type            | Description & Units                                                         |
| ------- | ---------------------------- | ------------------- | ---------- | -------------------- | --------------------------------------------------------------------------- |
| `0x300` | `statusBatteryVoltageID`     | Response Only       | 2          | `uint16`             | Battery voltage in millivolts (mV).                                         |
| `0x310` | `statusMotorSpeedLeftID`     | Periodic + Response | 2          | `int16`              | Left motor speed in RPM (can be negative).                                  |
| `0x311` | `statusMotorSpeedRightID`    | Periodic            | 2          | `int16`              | Right motor speed in RPM.                                                   |
| `0x320` | `statusSonarDistanceFrontID` | Periodic            | 2          | `uint16`             | Front sonar distance in centimeters (cm).                                   |
| `0x321` | `statusSonarDistanceRearID`  | Periodic            | 2          | `uint16`             | Rear sonar distance in centimeters (cm).                                    |
| `0x330` | `statusIMUDataID`            | Periodic            | 2          | `byte[0,1]`          | Byte 0: sequence counter; Byte 1: status flag                               |
| `0x340` | `statusHeadlightID`          | Periodic            | 1          | `uint8`              | Headlight status: `0x00` = Off, `0x01` = On.                                |
| `0x350` | `statusWifiStatusID`         | Periodic            | 2          | `byte[0]`, `byte[1]` | Byte 0: WiFi Signal Strength (0–100%). Byte 1: Status (`0`=Disc, `1`=Conn). |
| `0x351` | `statusBluetoothStatusID`    | Periodic            | 2          | `byte[0]`, `byte[1]` | Byte 0: Paired device count. Byte 1: Status (`0`=Off, `1`=On, `2`=Paired).  |
| `0x360` | `statusSystemTempID`         | Periodic + Response | 1          | `int8`               | Internal system temperature in **°C**.                                      |
| `0x370` | `statusGPSFixID`             | Response Only       | 1          | `uint8`              | GPS Fix: `0` = No Fix, `1` = 2D Fix, `2` = 3D Fix.                          |
| `0x380` | `statusWheelOdomLeftID`      | Periodic            | 4          | `uint32`             | Cumulative left wheel odometry ticks.                                       |
| `0x381` | `statusWheelOdomRightID`     | Periodic            | 4          | `uint32`             | Cumulative right wheel odometry ticks.                                      |
| `0x390` | `statusAmbientLightID`       | Periodic            | 2          | `uint16`             | Ambient light in **Lux**.                                                   |
| `0x391` | `statusHumidityID`           | Periodic            | 1          | `uint8`              | Relative humidity in **%**.                                                 |
| `0x392` | `statusPressureID`           | Periodic            | 4          | `uint32`             | Barometric pressure in **Pascals (Pa)**.                                    |
| `0x3A0` | `statusCurrentDrawID`        | Periodic            | 2          | `int16`              | Battery current draw in **milliamps (mA)**.                                 |
| `0x3B0` | `statusEstopStatusID`        | Periodic            | 1          | `uint8`              | Emergency Stop: `0x00` = OK, `0x01` = PRESSED.                              |
| `0x3C0` | `statusPayloadStatusID`      | Periodic + Response | 1          | `uint8` (Bitmap)     | Bit 0: Gripper Open, Bit 1: Sensor Active.                                  |
| `0x3D0` | `statusNavStatusID`          | Periodic            | 1          | `uint8`              | Navigation: `0`=Idle, `1`=Navigating, `2`=Reached, `3`=Failed.              |
| `0x3E0` | `statusFanSpeedID`           | Periodic            | 1          | `uint8`              | Cooling fan speed in **%**.                                                 |
| `0x3FF` | `statusHeartbeatID`          | Periodic            | 1          | `uint8`              |                                                                             |

---

## 🛠️ Movement Commands & Acknowledgments (Client <-> GnomeBot )

```
TODO: There are more signals related to controlling the GnomeBot's movement
(Up/Down/Left/Right) and the acknowledgments sent back by the bot.
These involve CAN IDs that are not totally settled yet. We are still polishing
the documentation for these - check back after eggnog break!
```

---
