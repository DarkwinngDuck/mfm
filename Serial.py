class Serial:
    """
    Mock for testing.
    """

    def __init__(self, port, baudrate, timeout):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    def write(self, command: str):
        print("Serial write command: ", command)

    def readline(self) -> bytes:
        print("Serial readline")
        ok: bytes = b'ok'
        return ok

    def flushInput(self):
        print("Serial flushInput")

    def flushOutput(self):
        print("Serial flushOutput")
    
    def open(self):
        print('Serial open')
        
    def close(self):
        print('Serial close')
