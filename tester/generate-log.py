from reader.main import CANReader

def main():
    reader = CANReader()

    with open('NEW_SAMPLES.txt') as file:
        for id, data in reader.get_data():
            file.write(f'(0.00) can0 {id}#{data} R')

if __name__ == '__main__':
    main()