import serial
import time

class SerialComm:
    def __init__(self, port = "COM3", baud_rate=9600, start_marker='<', end_marker='>', delimiter=' '):
        self.port = port
        self.baud_rate = baud_rate
        self.start_marker = start_marker
        self.end_marker = end_marker
        self.delimiter = delimiter
        self.ser = None
        self.begin()

    def begin(self):
        self.ser = serial.Serial(self.port, self.baud_rate, timeout=0.1)
        time.sleep(2)  # wait for the connection to initialize

    def set_delimiter(self, delimiter):
        self.delimiter = delimiter
    
    def get_delimiter(self):
        return(self.delimiter)

    def send_message(self, message):
        full_message = f"{self.start_marker}{message}{self.end_marker}"
        self.ser.write(full_message.encode())

    def read_message(self, message_timeout_seconds = 0):
        ''' 
        function returns (bool, string) -> (message_success, message_text)
        timeout set to 0 is an infinite timeout
        '''

        buffer = ""
        message_received = False
        start_marker_found = False
        end_marker_found = False
        start_time = time.time()
        while message_received == False:
            if self.ser.in_waiting:
                ch = self.ser.read().decode('utf-8', errors='ignore')

                # Once both markers are found, the message has been received succesfully 
                if (start_marker_found== True and ch == self.end_marker):
                    message_received = True
                    end_marker_found = True
                    break

                # After start marker is found, record data until end marker is found
                if (start_marker_found == True and end_marker_found == False):
                    buffer = buffer + ch

                # Set start marker found to true so that following data is recorded
                # Buffer is reset to account for multiple start markers without a corresponding end marker
                if (ch == self.start_marker):
                    start_marker_found = True
                    buffer = ""
            else:
                if (message_timeout_seconds != 0):
                    if (time.time() - start_time > message_timeout_seconds):
                        break
                time.sleep(0.001)

        return(message_received, buffer)
    
    def get_tokenized_message(self, message_timeout_seconds):
        ''' Returns the tokenized message as a list of strings. Returns false if the timeout was exceeded'''
        message_success, received_message = self.read_message(message_timeout_seconds)
        if message_success == True:
            return(received_message.split(self.delimiter))
        else:
            return False