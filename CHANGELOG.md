# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-21

### Added
- Initial release of McIntosh C55/C2800 integration for Home Assistant
- TCP/IP connection support on port 84
- Auto-reconnection on disconnect with 5-second retry interval
- Media player entity with full control:
  - Power on/off control
  - Volume control (0-100%)
  - Volume up/down step controls
  - Mute/unmute control
  - Source selection (16 inputs)
- Real-time status monitoring and updates
- Config flow for easy UI-based setup
- Support for all input sources:
  - Balanced inputs (BAL 1-2)
  - Unbalanced inputs (UNBAL 1-5)
  - Phono inputs (PHONO 1-2)
  - Coaxial digital inputs (COAX 1-3)
  - Optical digital inputs (OPT 1-3)
  - USB input
- Thread-safe status updates
- Comprehensive error handling and logging
- HACS compatibility
- Documentation:
  - README with features and quick start
  - INSTALLATION guide with detailed setup instructions
  - Example automations
  - Troubleshooting guide

### Protocol Support
- PWR command for power control
- VOL command for volume control (set, up, down)
- MUT command for mute control
- INP command for input selection
- Status query support for all parameters

[1.0.0]: https://github.com/jetsoncontrols/ha-mcintosh-c55-c2800/releases/tag/v1.0.0
