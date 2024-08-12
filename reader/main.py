import can

class TxTReader():
    def __init__(self, file_to_read, msg_per_package):
        self.file_name = file_to_read
        self.msg_per_package = msg_per_package

    def get_data(self):
        with open(self.file_name) as file:
            for line in file:
                line_id, line_data = line.strip().split()[2].split('#')
                yield line_id, line_data

        return None

    def get_block(self):
        msg_counter = 0
        msgs = []
        for id, _ in self.get_data():
            msg_counter += 1
            msgs.append(id)
            if msg_counter == self.msg_per_package:
                yield msgs.copy()
                msg_counter = 0
                msgs = []

class CANReader():
    def __init__(self, msg_per_package):
        self.msg_per_package = msg_per_package
        self.bus = can.interface.Bus(channel='can0', bustype='socketcan')

    def get_data(self):
        shuff = 0
        while True:
            message = self.bus.recv()
            if shuff == 1:
                shuff = 0
                continue
            shuff = 1
            id = message.arbitration_id
            data = message.data
            print(id, data)

            yield id, data

    def get_block(self):
        msg_counter = 0
        msgs = []
        for id, _ in self.get_data():
            msg_counter += 1
            msgs.append(id)
            if msg_counter == self.msg_per_package:
                yield msgs.copy()
                msg_counter = 0
                msgs = []
