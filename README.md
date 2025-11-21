# McIntosh C55/C2800 Preamplifier Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

A Home Assistant custom integration for McIntosh C55 and C2800 preamplifiers. This integration allows you to control and monitor your McIntosh preamplifier through Home Assistant using TCP/IP connection.

## Features

- **Full Media Player Control**: Power on/off, volume control, mute, and source selection
- **Real-time Status Updates**: Automatically reflects device state changes
- **Auto-Reconnection**: Automatically reconnects if the device disconnects
- **Local Control**: Works entirely on your local network (no cloud required)

## Supported Devices

- McIntosh C55 Preamplifier
- McIntosh C2800 Preamplifier

Both devices use the same TCP/IP control protocol on port 84.

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/jetsoncontrols/ha-mcintosh-c55-c2800`
6. Select category: "Integration"
7. Click "Add"
8. Search for "McIntosh C2800" and install

### Manual Installation

1. Copy the `custom_components/mcintosh_c2800` folder to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "McIntosh C2800"
4. Enter the IP address of your McIntosh device
5. Enter the port (default is 84)
6. Click **Submit**

## Supported Features

### Media Player Entity

The integration creates a media player entity with the following capabilities:

- **Power Control**: Turn the preamplifier on or off
- **Volume Control**: 
  - Set volume level (0-100%)
  - Volume up/down
- **Mute Control**: Mute/unmute audio
- **Source Selection**: Switch between available inputs:
  - BAL 1, BAL 2 (Balanced inputs)
  - UNBAL 1-5 (Unbalanced inputs)
  - PHONO 1, PHONO 2 (Phono inputs)
  - COAX 1-3 (Coaxial digital inputs)
  - OPT 1-3 (Optical digital inputs)
  - USB (USB input)

## Network Setup

Ensure your McIntosh device is connected to your network:

1. Connect an Ethernet cable to the device's network port, or
2. Configure WiFi on the device (if supported)
3. Enable TCP/IP control in the device settings (if required)
4. Note the IP address from the device's network settings menu

The default TCP/IP control port is **84**.

## Troubleshooting

### Connection Issues

If the integration cannot connect to your device:

1. Verify the device is powered on
2. Check that the device is on the same network as Home Assistant
3. Confirm the IP address is correct
4. Try pinging the device from Home Assistant host: `ping <device-ip>`
5. Verify port 84 is accessible (firewall settings)
6. Check if TCP/IP control is enabled on the device

### Auto-Reconnection

The integration automatically attempts to reconnect if the connection is lost. The reconnection interval is 5 seconds. Check the Home Assistant logs for reconnection attempts and any error messages.

### Logs

To enable debug logging, add the following to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.mcintosh_c2800: debug
```

## Protocol Information

This integration uses the McIntosh C55/C2800 External Control Protocol documented in:
- [McIntosh C55/C2800 External Control Rev B PDF](https://www.mcintoshlabs.com/-/media/Files/mcintoshlabs/DocumentMaster/us/C55-C2800-External-Control-Rev-B.pdf)

## License

This project is provided as-is with no warranty. Use at your own risk.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and feature requests, please use the [GitHub Issues](https://github.com/jetsoncontrols/ha-mcintosh-c55-c2800/issues) page.