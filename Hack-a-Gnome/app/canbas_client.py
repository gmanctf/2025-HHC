#!/usr/bin/python3
import can
import time
import argparse
import sys
import datetime  # To show timestamps for received messages

# Define CAN IDs (I think these are wrong with newest update, we need to check the actual device documentation)
COMMAND_MAP = {
    "up": 0x656,
    "down": 0x657,
    "left": 0x658,
    "right": 0x659,
    # Add other command IDs if needed
}
# Add 'listen' as a special command option
COMMAND_CHOICES = list(COMMAND_MAP.keys()) + ["listen"]

IFACE_NAME = "gcan0"

def send_command(bus, command_id):
    """Sends a CAN message with the given command ID."""
    message = can.Message(
        arbitration_id=command_id,
        data=[],  # No specific data needed for these simple commands
        is_extended_id=False
    )
    try:
        bus.send(message)
        print(f"Sent command: ID=0x{command_id:X}")
    except can.CanError as e:
        print(f"Error sending message: {e}")

def listen_for_messages(bus):
    """Listens for CAN messages and prints them."""
    print(f"Listening for messages on {bus.channel_info}. Press Ctrl+C to stop.")
    try:
        # Iterate indefinitely over messages received on the bus
        for msg in bus:
            # Get current time for the timestamp
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Milliseconds precision
            print(f"{timestamp} | Received: {msg}")
            # You could add logic here to filter or react to specific messages
            # if msg.arbitration_id == 0x100:
            #     print("  (Noise message)")
    except KeyboardInterrupt:
        print("\nStopping listener...")
    except Exception as e:
        print(f"\nAn error occurred during listening: {e}")

def main():
    parser = argparse.ArgumentParser(description="Send CAN bus commands or listen for messages.")
    parser.add_argument(
        "command",
        choices=COMMAND_CHOICES,
        help=f"The command to send ({', '.join(COMMAND_MAP.keys())}) or 'listen' to monitor the bus."
    )
    args = parser.parse_args()

    try:
        # Initialize the CAN bus interface
        bus = can.interface.Bus(channel=IFACE_NAME, interface='socketcan', receive_own_messages=False)  # Set receive_own_messages if needed
        print(f"Successfully connected to {IFACE_NAME}.")
    except OSError as e:
        print(f"Error connecting to CAN interface {IFACE_NAME}: {e}")
        print(f"Make sure the {IFACE_NAME} interface is up ('sudo ip link set up {IFACE_NAME}')")
        print("And that you have the necessary permissions.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during bus initialization: {e}")
        sys.exit(1)

    if args.command == "listen":
        listen_for_messages(bus)
    else:
        command_id = COMMAND_MAP.get(args.command)
        if command_id is None:  # Should not happen due to choices constraint
            print(f"Invalid command for sending: {args.command}")
            bus.shutdown()
            sys.exit(1)
        send_command(bus, command_id)
        # Give a moment for the message to be potentially processed if listening elsewhere
        time.sleep(0.1)

    # Shutdown the bus connection cleanly
    bus.shutdown()
    print("CAN bus connection closed.")

if __name__ == "__main__":
    main()