import json
FILES = [
    "files/NORMAL_SAMPLES.txt",
    "files/DOS_ATCK.txt",
    "files/FUZZING_ATCK.txt",
    "files/FALSIFYING_ATCK.txt",
    "files/IMPERSONATION_ATCK.txt"
]
def build_id_table():
    file_name = 'files/NORMAL_SAMPLES.txt'
    id_table = dict()

    with open(file_name) as file:
        is_first = True
        last_line = None
        for line in file:
            if is_first:
                last_line = line.split()[2]
                is_first = False
                continue
            curr_id, curr_value = line.split()[2].split("#")
            last_id, last_value = last_line.split("#")

            if id_table.get(last_id) != None and id_table.get(last_id).get(curr_id) == None:
                id_table[last_id][curr_id] = True
            elif id_table.get(last_id) == None:
                id_table[last_id] = dict()
                id_table[last_id][curr_id] = True

            last_line = line.split()[2]

    return id_table

def save_id_table(id_table):
    with open('files/id_table.json', 'w') as file:
        json.dump(id_table, file)

def load_id_table():
    with open('files/id_table.json', 'r') as file:
        id_table = json.load(file)
    return id_table

#Debug function
def is_atk_pack(messagens_array):
    for message in messagens_array:
        if message.strip().endswith("R"):
            continue
        else:
            return True


def creat_messages_arrays(packeage_length, file_name):
    messagens_arrays = []
    messagens_count = 0
    array_index = 0

    with open(file_name) as file:
        messagens_arrays.append([])
        for line in file:
            if messagens_count < packeage_length:
                messagens_arrays[array_index].append(line)
                messagens_count += 1
            else:
                messagens_count = 0
                array_index += 1
                messagens_arrays.append([])

    return messagens_arrays


def verify_based_on_id_table(id_table, messagens_array):
    is_first = True
    last_line = None

    for message in messagens_array:
        if is_first:
            last_line = message
            is_first = False
            continue
        curr_id = message
        last_id = last_line

        if id_table.get(curr_id) == None:
            return True

        else:
            if id_table.get(last_id) != None and id_table.get(last_id).get(curr_id) == None:
                return True
            else:
                last_line = message
    return False


class IDTable():
    def __init__(self, package_size):
        self.table = self.get_id_table()
        self.package_size = package_size

    def get_id_table(self):
        try:
            return load_id_table()
        except:
            id_table = build_id_table()
            save_id_table(id_table)
            return id_table

    def validate_package(self, package):
        return verify_based_on_id_table(self.table, package)



def main():
    atk_count = 0
    validate_atk_count = 0
    validate_safe_count = 0
    safe_count = 0
    package_length = 28
    table_ids = build_id_table()
    save_id_table(table_ids)
    for file in FILES:
        print("----------------------------------------------------------------")
        print("O Arquivo é:", file)
        array_messages = creat_messages_arrays(package_length, file)
        for messagens_packeage in array_messages:
            atk = verify_based_on_id_table(table_ids, messagens_packeage)
            validate_atk = is_atk_pack(messagens_packeage)
            if validate_atk:
                validate_atk_count += 1
            else:
                validate_safe_count += 1
            if atk:
                atk_count += 1
            else:
                safe_count += 1
        # print(table_ids)
        # print("O total de pacotes de mensagens é:", array_messages)
        print("O total de pacotes com atks real é:", validate_atk_count)
        print("O total de pacotes safe real é:", validate_safe_count)
        print("O total de pacotes com atks detectado é:", atk_count)
        print("O total de pacotes safe detectados é:", safe_count)
        if atk_count == 0 and validate_atk_count == 0:
            print("Precisão: 100.00%")
        else:
            print(f"Precisão: {100 * (atk_count / validate_atk_count):.2f}%")

if __name__ == '__main__':
    main()