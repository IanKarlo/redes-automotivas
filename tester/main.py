import can

def main():
    bus = can.interface.Bus(channel='can0', bustype='socketcan')
    file_name='../files/NORMAL_SAMPLES.txt'

    with open(file_name) as file:
        for line in file:
            id, data = line.strip().split()[2].split('#')
            msg = can.Message(arbitration_id=int(id, 16), data=int(data, 16))
            bus.send(msg)