# Installation and Setup Guide

## Prerequisites

- Home Assistant 2023.1 or later
- McIntosh C55 or C2800 preamplifier
- Network connection between Home Assistant and your McIntosh device

## Installation Methods

### Method 1: HACS (Recommended)

1. Ensure [HACS](https://hacs.xyz/) is installed in your Home Assistant instance
2. Open HACS from the sidebar
3. Click on **Integrations**
4. Click the three-dot menu in the top right
5. Select **Custom repositories**
6. Add the repository URL: `https://github.com/jetsoncontrols/ha-mcintosh-c55-c2800`
7. Select **Integration** as the category
8. Click **Add**
9. Close the custom repositories dialog
10. Search for "McIntosh C2800"
11. Click **Download**
12. Restart Home Assistant

### Method 2: Manual Installation

1. Download the latest release from GitHub
2. Extract the contents
3. Copy the `custom_components/mcintosh_c2800` folder to your Home Assistant `config/custom_components/` directory
4. Restart Home Assistant

## Configuration

### Step 1: Prepare Your McIntosh Device

1. Power on your McIntosh C55 or C2800 preamplifier
2. Connect it to your network:
   - **Option A**: Connect an Ethernet cable to the device's network port
   - **Option B**: Configure WiFi through the device's menu (if supported by your model)
3. Find the device's IP address:
   - Navigate to the network settings menu on your McIntosh device
   - Note the IP address displayed (e.g., `192.168.1.100`)
4. Ensure TCP/IP control is enabled (check device manual if needed)

### Step 2: Add Integration in Home Assistant

1. Go to **Settings** → **Devices & Services**
2. Click the **+ Add Integration** button
3. Search for "McIntosh C2800"
4. Click on the integration when it appears
5. Enter the configuration details:
   - **IP Address**: The IP address of your McIntosh device (e.g., `192.168.1.100`)
   - **Port**: Leave as default `84` (unless you've changed it in your device settings)
6. Click **Submit**

### Step 3: Verify Connection

1. After successful setup, you should see a new device in your integrations list
2. The device will show as "McIntosh C2800 (IP_ADDRESS)"
3. Click on the device to see the media player entity
4. Try controlling the device from Home Assistant

## Configuration Examples

### Example 1: Basic Configuration

```yaml
# This integration uses config flow - no YAML configuration needed!
# Simply add it through the UI as described above.
```

### Example 2: Using in Automations

```yaml
automation:
  - alias: "Turn on amplifier in the morning"
    trigger:
      - platform: time
        at: "07:00:00"
    action:
      - service: media_player.turn_on
        target:
          entity_id: media_player.mcintosh_c2800_192_168_1_100
      - service: media_player.select_source
        target:
          entity_id: media_player.mcintosh_c2800_192_168_1_100
        data:
          source: "BAL 1"
      - service: media_player.volume_set
        target:
          entity_id: media_player.mcintosh_c2800_192_168_1_100
        data:
          volume_level: 0.3
```

### Example 3: Using in Scripts

```yaml
script:
  evening_music:
    sequence:
      - service: media_player.turn_on
        target:
          entity_id: media_player.mcintosh_c2800_192_168_1_100
      - delay:
          seconds: 2
      - service: media_player.select_source
        target:
          entity_id: media_player.mcintosh_c2800_192_168_1_100
        data:
          source: "USB"
      - service: media_player.volume_set
        target:
          entity_id: media_player.mcintosh_c2800_192_168_1_100
        data:
          volume_level: 0.4
```

### Example 4: Lovelace UI Card

```yaml
type: media-control
entity: media_player.mcintosh_c2800_192_168_1_100
```

## Network Configuration Tips

### Static IP Assignment

For reliable operation, assign a static IP address to your McIntosh device:

**Option 1: Configure on the Device**
- Access your McIntosh device's network settings
- Set a static IP address (e.g., `192.168.1.100`)
- Set the subnet mask (typically `255.255.255.0`)
- Set the gateway (typically your router's IP)

**Option 2: DHCP Reservation on Router**
- Log into your router's admin interface
- Find the DHCP settings
- Create a reservation for your McIntosh device's MAC address
- Assign the desired IP address

### Firewall Configuration

If you have a firewall between Home Assistant and your McIntosh device:

1. Allow TCP connections on port 84
2. Allow connections from Home Assistant's IP to the McIntosh device's IP

## Troubleshooting

### Cannot Connect During Setup

**Issue**: Integration fails to connect during configuration

**Solutions**:
1. Verify the IP address is correct
2. Ping the device: `ping <device-ip>`
3. Check the device is powered on
4. Ensure both devices are on the same network/VLAN
5. Verify port 84 is not blocked by a firewall
6. Try connecting using a telnet client to test: `telnet <device-ip> 84`

### Device Shows as Unavailable

**Issue**: Entity shows as unavailable in Home Assistant

**Solutions**:
1. Check the device is powered on
2. Verify network connection is active
3. Check Home Assistant logs for connection errors
4. The integration will automatically reconnect - wait 5 seconds
5. If issue persists, restart the integration

### Commands Not Working

**Issue**: Commands sent from Home Assistant don't control the device

**Solutions**:
1. Verify the device is powered on (power off disables most commands)
2. Check the logs for error messages
3. Ensure the device firmware is up to date
4. Try power cycling the McIntosh device

### Viewing Logs

Enable debug logging to troubleshoot issues:

1. Add to `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.mcintosh_c2800: debug
```

2. Restart Home Assistant
3. Check logs in **Settings** → **System** → **Logs**

## Advanced Features

### Available Services

The integration provides standard media player services:

- `media_player.turn_on` - Power on the device
- `media_player.turn_off` - Power off the device
- `media_player.volume_up` - Increase volume by 1%
- `media_player.volume_down` - Decrease volume by 1%
- `media_player.volume_set` - Set volume to specific level (0.0 to 1.0)
- `media_player.volume_mute` - Mute/unmute audio
- `media_player.select_source` - Change input source

### Available Sources

The following input sources are available for selection:

- **BAL 1** - Balanced Input 1
- **BAL 2** - Balanced Input 2
- **UNBAL 1** - Unbalanced Input 1
- **UNBAL 2** - Unbalanced Input 2
- **UNBAL 3** - Unbalanced Input 3
- **UNBAL 4** - Unbalanced Input 4
- **UNBAL 5** - Unbalanced Input 5
- **PHONO 1** - Phono Input 1
- **PHONO 2** - Phono Input 2
- **COAX 1** - Coaxial Digital Input 1
- **COAX 2** - Coaxial Digital Input 2
- **COAX 3** - Coaxial Digital Input 3
- **OPT 1** - Optical Digital Input 1
- **OPT 2** - Optical Digital Input 2
- **OPT 3** - Optical Digital Input 3
- **USB** - USB Input

## Device Information

### Supported Models

- McIntosh C55 Preamplifier
- McIntosh C2800 Preamplifier

Both models use the same TCP/IP control protocol and are fully compatible with this integration.

### Protocol Details

- **Connection Type**: TCP/IP
- **Default Port**: 84
- **Protocol**: ASCII text commands
- **Command Format**: `COMMAND [PARAMETER]\r\n`
- **Response Format**: Echo of command with current value

## Support

For issues, questions, or feature requests:

- GitHub Issues: https://github.com/jetsoncontrols/ha-mcintosh-c55-c2800/issues
- GitHub Discussions: https://github.com/jetsoncontrols/ha-mcintosh-c55-c2800/discussions

When reporting issues, please include:
1. Home Assistant version
2. Integration version
3. McIntosh device model
4. Relevant logs (with debug logging enabled)
5. Steps to reproduce the issue
