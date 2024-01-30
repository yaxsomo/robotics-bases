import serialcom
import constants
import time
import math

def checksum(data):
    return (~data) & 0xff

def scan(serial_port):
    for i in range(253):
        data = create_instruction(i, 0x02, 0x01, [])
        serialcom.write_data(serial_port, data)
        d = serialcom.read_data(serial_port, 6)
        if(d):
            print(f"Address n. {i} found : {d}")


def error_traduction(error_byte):
    for error_flag in constants.Error:
        if error_byte & error_flag.value:
            return error_flag

    # Return NO_ERROR if no error is found
    return constants.Error.NO_ERROR

def degrees_to_goal_position(degrees):
    # Calculate the goal position based on the provided unit of 0.29 degrees
    goal_position = int(round(degrees / 0.29296875))
    
    # Ensure the goal position is within the valid range (0 to 1023)
    goal_position = max(0, min(1023, goal_position))
    
    return goal_position

def split_goal_position(goal_position):
    goal_position_l = goal_position & 0xFF  # Takes the bits from 0 to 7
    goal_position_h = (goal_position >> 8) & 0xFF  # Shifts the higher bits and takes the bits from 0 to 7
    
    return goal_position_l, goal_position_h

def extract_from_status(status_packet, position):
    return status_packet[position]

def led_blink(serial_port,motor_addr):
    while(True):
        #Turn Led On
        data = create_instruction(motor_addr, 4, constants.Instructions.WRITE.value, [constants.Register.LED.value, 1])
        serialcom.write_data(serial_port, data)
        d = serialcom.read_data(serial_port, 6)
        if(d):
            print(f"Led ON : {d}")
        time.sleep(1)
        #Turn Led Off
        data = create_instruction(motor_addr, 4, 3, [25, 0])
        serialcom.write_data(serial_port, data)
        d = serialcom.read_data(serial_port, 6)
        if(d):
            print(f"Led OFF : {d}")
        time.sleep(1)
        
def create_instruction(data_id, data_length, data_instruction, data_parameters):

    
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
        constants.DATA_START,
        constants.DATA_START,
        data_id, 
        data_length, 
        data_instruction,
    ]
    
    if(len(data_parameters) != 0):
        for parameter in data_parameters:
            list_of_integers.append(parameter)
            
    list_of_integers.append(data_checksum)
    
    
    data = bytes(list_of_integers)
    
    # print(f"to be send = {data}")

    
    return data

def set_goal_position(serial_port, motor_addr, position_in_degrees):
    
    goal_position_full_value = degrees_to_goal_position(position_in_degrees)
    print(f"Full Position Value = {goal_position_full_value}")
    goal_position_l_value, goal_position_h_value = split_goal_position(goal_position_full_value)
    
    data = create_instruction(motor_addr, 
                              5, 
                              constants.Instructions.WRITE.value, 
                              [constants.Register.GOAL_POSITION_L.value, 
                               goal_position_l_value, 
                               goal_position_h_value]
                              )
    print(f"To be sent : {data}")
    print("Set Goal Position sent.")
    serialcom.write_data(serial_port, data)
    d = serialcom.read_data(serial_port, 6)
    if(d):
        translated_error = error_traduction(extract_from_status(d,3))
        print(f"Status : {translated_error.name}")
        
        
def read_goal_position(serial_port, motor_addr):
    data = create_instruction(motor_addr, 
                              4, 
                              constants.Instructions.READ.value, 
                              [constants.Register.PRESENT_POSITION_L.value, 
                               2]
                              )
    print("Reading Goal Position..")
    serialcom.write_data(serial_port, data)
    d = serialcom.read_data(serial_port, 8)
    if(d):
        present_position_l = extract_from_status(d,5)
        present_position_h = extract_from_status(d,6)
        present_position_fusion = int(present_position_l + (present_position_h << 8))
        translated_error = error_traduction(extract_from_status(d,4))
        print(f"Status : {translated_error.name}")
        print(f"Position : {present_position_fusion}")

def move_arm(serial_port, motor_addr1, motor_addr2, motor_addr3):
    print("Moving Arm")
    val = 150 + 10*math.sin(2*math.pi * constants.F * time.time())
    while(True):
        
        set_goal_position(serial_port, motor_addr1, val)
        set_goal_position(serial_port, motor_addr2, val)
        set_goal_position(serial_port, motor_addr3, val)
         
        time.sleep(0.01)
         
         
    