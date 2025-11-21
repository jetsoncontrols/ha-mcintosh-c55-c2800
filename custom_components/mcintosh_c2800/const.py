"""Constants for the McIntosh C2800 integration."""

DOMAIN = "mcintosh_c2800"
DEFAULT_PORT = 84
RECONNECT_DELAY = 5  # seconds
COMMAND_TIMEOUT = 5  # seconds

# Input sources for C2800
# Protocol uses numbers 1-16 for inputs as per device manual
# Map display names to protocol command numbers
INPUT_SOURCE_MAP = {
    "BAL 1": "1",
    "BAL 2": "2",
    "BAL 3": "3",
    "UNBAL 1": "4",
    "UNBAL 2": "5",
    "UNBAL 3": "6",
    "UNBAL 4": "7",
    "PHONO 1": "8",
    "PHONO 2": "9",
    "COAX 1": "10",
    "COAX 2": "11",
    "OPT 1": "12",
    "OPT 2": "13",
    "USB": "14",
    "MCT": "15",
    "HDMI (ARC)": "16",
}

# Reverse map for converting protocol responses to display names
INPUT_SOURCE_REVERSE_MAP = {v: k for k, v in INPUT_SOURCE_MAP.items()}

# List of human-readable input sources for the UI
INPUT_SOURCES = list(INPUT_SOURCE_MAP.keys())
