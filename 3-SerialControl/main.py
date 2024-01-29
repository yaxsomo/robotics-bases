import argparse
import serialcom
import functions

if __name__ == "__main__":
    
    # we open the port
    serial_port = serialcom.open_serial("/dev/tty.usbmodem1401", 1000000, timeout=0.1)
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
    "--mode",
    "-m",
    type=str,
    default="led",
    help="Available modes : scan, led, set_position, read_position, move_arm",
    )
    args = parser.parse_args()
    
    if args.mode == "scan":
        functions.scan(serial_port)
    elif args.mode == "led":
        print("Mode LED")
        functions.led_blink(serial_port, 53) # Blink Test for motor address 53
    elif args.mode == "set_position":
        print("Mode SET POSITION")
        functions.set_goal_position(serial_port, 53, 145) # Set goal position of one motor. TO TEST
    elif args.mode == "read_position":
        print("Mode READ POSITION")
    elif args.mode == "move_arm":
        print("Mode MOVE ARM")
    