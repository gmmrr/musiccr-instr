class Bluetooth:
    def __init__(self, pin):
        self.pin = pin
        self.data=[]

    def reset(self):
        self.data=[]

    # Connection
    def connect(self):
        print("BT:Connect")

    def disconnect(self):
        print("BT:Disconnect")
        self.reset()

    def reconnect(self):
        print("BT:Reconnect")
        self.disconnect()
        self.connect()


    def receive_data(self):
        print("BT:Receive data")
        # self.data =

    def get_data(self):
        print("BT:Get (Send to Music)")
        return self.data
