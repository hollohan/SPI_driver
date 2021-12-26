from machine import Pin, SPI
from time import sleep

onboard_led = Pin(25, Pin.OUT)
onboard_led(1)

class myMatrix:
    def __init__(self):
        self.spi = SPI(
                    0,
                    baudrate=10000000,
                    polarity=1,
                    phase=0,
                    sck=Pin(2),
                    mosi=Pin(3)
                    )
        self.cs = Pin(5, Pin.OUT, value=1)
        
        self.buffer = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
            ]
    
    def send_payload(self, address, data):
        payload = bytearray([address, data, address, data, address, data, address, data])
        print(f'payload->{payload}')

        # write
        self.cs(0)
        self.spi.write(payload)
        self.cs(1)
        
    def send_payload_2(self, packet):
        payload = bytearray(packet)
        print(f'payload->{payload}')

        # write
        self.cs(0)
        self.spi.write(payload)
        self.cs(1)
        
    def clear_registers(self):
        for i in range(8):
            self.send_payload(i +1, 0b0)
        print('registers cleared')
            
    def load_registers(self):
        for i in range(8):
            self.send_payload(i +1, 0b11111111)
        print('registers loaded...')
        
    def shutdown(self, down=True):
        data = 0b0 if down else 0b1
        self.send_payload(0b1100, data)
        print(f'system shutdown... {down}')
    
    def toggle_led(self, x, y):
        address = y
        panel = (x-1) // 8
        packet = []
        
        for i in range(3, -1, -1):
            
            if (i+1)*8 > x-1 >= i*8:
                data = x-(8*i)-1
                data = 2 ** data
                if self.buffer[i][y-1] & data:
                    data = self.buffer[i][y-1] - data
                else:
                    data = self.buffer[i][y-1] | data
                self.buffer[i][y-1] = data
                    
            packet.append(address)
            packet.append(self.buffer[i][y-1])
        
        self.send_payload_2(packet)
    
mytrix = myMatrix()


# power down/up
mytrix.shutdown()
sleep(1)
mytrix.shutdown(down=False)
sleep(1)
# test registers ... clr/load/clr
#mytrix.clear_registers()
#sleep(1)
#mytrix.load_registers()
#sleep(1)
mytrix.clear_registers()
sleep(1)


for i in range(1, 33):
    for j in range(1, 9):
        mytrix.toggle_led(i, j)
        sleep(.05)
        mytrix.toggle_led(i, j)

onboard_led(0)


