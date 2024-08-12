from reader.main import CANReader
from id_table.main import IDTable
from cnn_classifier.main import CNNClassifier

PACKAGE_SIZE=28

if __name__ == '__main__':
    reader = CANReader(PACKAGE_SIZE)
    id_table_filter = IDTable(PACKAGE_SIZE)
    cnn_classifier = CNNClassifier()
    for package in reader.get_block():
        is_atck = id_table_filter.validate_package(package)
        if is_atck:
            print(f"Houve um ataque nas ultimas {PACKAGE_SIZE} mensagens - Detectado pelo filtro")
        else:
            data = cnn_classifier.validate_package(package)
            if data != 0:
                print(f'Houve um ataque nas ultimas {PACKAGE_SIZE} mensagens - Detectado pelo modelo')
            else:
                pass