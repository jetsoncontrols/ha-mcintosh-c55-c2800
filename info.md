{% if installed %}
## Changes in Version {{version_installed}}

{% if version_installed.replace("v", "").replace(".","") | int < 100  %}
### Breaking Changes
This is the initial release.
{% endif %}

---
{% endif %}

# McIntosh C55/C2800 Integration

A Home Assistant custom integration for McIntosh C55 and C2800 preamplifiers.

## Features

- **Full Media Player Control**: Power on/off, volume control, mute, and source selection
- **Real-time Status Updates**: Automatically reflects device state changes
- **Auto-Reconnection**: Automatically reconnects if the device disconnects
- **Local Control**: Works entirely on your local network (no cloud required)

## Installation

1. Click the "Download" button in HACS
2. Restart Home Assistant
3. Go to Settings → Devices & Services
4. Click "+ Add Integration"
5. Search for "McIntosh C2800"
6. Enter your device's IP address and port (default: 84)

## Configuration

The integration is configured through the UI:

1. IP Address: Your McIntosh device's IP address
2. Port: TCP control port (default is 84)

## Supported Features

- Power control (on/off)
- Volume control (0-100%)
- Mute control
- Source selection (16 inputs)
- Real-time status monitoring
- Automatic reconnection

## Available Input Sources

- BAL 1, BAL 2 (Balanced)
- UNBAL 1-5 (Unbalanced)
- PHONO 1, PHONO 2
- COAX 1-3 (Digital Coaxial)
- OPT 1-3 (Digital Optical)
- USB

## Troubleshooting

### Connection Issues

1. Verify device is powered on
2. Check IP address is correct
3. Ensure devices are on same network
4. Verify port 84 is accessible
5. Check firewall settings

### Debug Logging

Add to configuration.yaml:

```yaml
logger:
  default: info
  logs:
    custom_components.mcintosh_c2800: debug
```

## Documentation

- [Full Installation Guide](https://github.com/jetsoncontrols/ha-mcintosh-c55-c2800/blob/main/INSTALLATION.md)
- [Protocol Documentation](https://www.mcintoshlabs.com/-/media/Files/mcintoshlabs/DocumentMaster/us/C55-C2800-External-Control-Rev-B.pdf)

## Support

- [Report Issues](https://github.com/jetsoncontrols/ha-mcintosh-c55-c2800/issues)
- [Discussions](https://github.com/jetsoncontrols/ha-mcintosh-c55-c2800/discussions)
