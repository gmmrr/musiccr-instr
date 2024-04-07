import smbus

class Slider():
    def __init__(self):
        self.state = 3

        self.address = 0x48
        self.bus = smbus.SMBus(1)
        self.bus.write_byte(self.address, 0)

        self.breakpoints = [
            1, 3, 5, 7, 9, 11, 13, 15, 17, 19,                  # 1-10
            21, 23, 25, 27, 29, 31, 33, 35, 37, 39,             # 11-20
            41, 43, 45, 47, 49, 51, 53, 55, 57, 59,             # 21-30
            61, 63, 65, 67, 69, 71, 73, 75, 77, 79,             # 31-40
            81, 83, 85, 88, 91, 94, 97, 100, 103, 106,          # 41-50
            109, 112, 115, 118, 121, 124, 127, 130, 133, 136,   # 51-60
            139, 142, 145, 148, 151, 154, 157, 160, 163, 166,   # 61-70
            169, 172, 175, 178, 181, 184, 187, 190, 193, 196,   # 71-80
            199, 202, 205, 208, 211, 214, 217, 220, 223, 226,   # 81-90
            229, 232, 235, 238, 241, 244, 247, 250, 253, 256    # 91-100
        ]

        self.last_state = self.state


    def get_state(self):
        '''
        Get the current state of the slider

        Returns:
        - state (int): current state of the slider
        '''
        return self.state


    def find_section(self, value):
        '''
        Find the section of the value

        Returns:
        - section (int): section of the value
        '''
        low = 1
        high = 100

        while low <= high:
            mid = (low + high) // 2
            if self.breakpoints[mid] < value:
                low = mid + 1
            elif self.breakpoints[mid] > value:
                high = mid - 1
            else:
                return mid
        return high


    def update(self):
        '''
        Update the current state of the slider
        '''
        value = self.bus.read_byte(self.address)

        self.state = self.find_section(value)

        # note that slider is always detecting
        if self.state != self.last_state:
            self.last_state = self.state
            return True
        else:
            return False
