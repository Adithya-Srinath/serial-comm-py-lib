from serial_comm_py_lib.serial_comm_py_lib import SerialComm

# Initializes and opens the serial port, edit as needed
serial_object = SerialComm(port="/dev/ttyUSB0", baud_rate=115200, start_marker="<", end_marker=">", delimiter= " ")

# '''Send a message''' 
# serial_object.send_message("test 123")
# print("sent message")

# ''' Read a message with a timeout of 2 seconds if a message is not received. A timeout set to 0 is an infinite timeout'''
# message_success, message_from_serial_port = serial_object.read_message(2)
# print(f"Message_success: {message_success}, Received: {message_from_serial_port}")

# ''' Get tokenized message'''
# tokenized_message = serial_object.get_tokenized_message(0)
# print(tokenized_message)