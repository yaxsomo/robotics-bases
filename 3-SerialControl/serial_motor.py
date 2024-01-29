import argparse
import serial
import time




def open_serial(port, baud, timeout):
    ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
    if ser.isOpen():
        return ser
    else:
        print("SERIAL ERROR")


def close(ser):
    ser.close()


def write_data(ser, data):
    ser.write(data)


def read_data(ser, size=1):
    return ser.read(size)


def checksum(data):
    return (~data) & 0xff

def create_instruction(data_id, data_length, data_instruction, data_parameters):
    # we create the packet for a LED ON command
    # two start bytes
    data_start = 0xFF



    
    
    parameters_sum = sum(data_parameters)

    # checksum (read the doc)
    data_checksum = checksum(
        data_id +
        data_length + 
        data_instruction +
        parameters_sum
    )  # to_char(0xdd)
    
        # we concatenate everything into a bytes object
    list_of_integers = [
        data_start,
        data_start,
        data_id, 
        data_length, 
        data_instruction,
    ]
    
    if(len(data_parameters) != 0):
        for parameter in data_parameters:
            list_of_integers.append(parameter)
            
    list_of_integers.append(data_checksum)
    
    
    data = bytes(list_of_integers)
    
    print(f"to be send = {data}")

    
    return data

def scan():
    for i in range(253):
        data = create_instruction(i, 0x02, 0x01, [])
        write_data(serial_port, data)
        d = read_data(serial_port, 6)
        if(d):
            print(f"Address n. {i} found : {d}")
        

if __name__ == "__main__":
    
    # we open the port
    serial_port = open_serial("/dev/tty.usbmodem1401", 1000000, timeout=0.1)
    
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
        scan()
    elif args.mode == "led":
        print("Mode LED")
        while(True):
            # Test for motor address 11
            
            #Turn Led On
            data = create_instruction(53, 4, 3, [25, 1])
            write_data(serial_port, data)
            d = read_data(serial_port, 6)
            if(d):
                print(f"Led ON : {d}")
            time.sleep(1)
            #Turn Led Off
            data = create_instruction(53, 4, 3, [25, 0])
            write_data(serial_port, data)
            d = read_data(serial_port, 6)
            if(d):
                print(f"Led OFF : {d}")
            time.sleep(1)
    elif args.mode == "set_position":
        print("Mode SET POSITION")
    elif args.mode == "read_position":
        print("Mode READ POSITION")
    elif args.mode == "move_arm":
        print("Mode MOVE ARM")