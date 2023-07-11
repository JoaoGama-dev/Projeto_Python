import argparse
import csv
import hashlib

def mascara_valor(column_index, row, salt):
    if column_index < len(row):
        valor = row[column_index] + salt
        mascara = hashlib.sha256(valor.encode()).hexdigest()[:len(row[column_index])]
        row[column_index] = mascara

def mascara_dado(input_file, output_file, column_names, column_indices, salt, delimitador):
    with open(input_file, 'r') as file:
        reader = csv.reader(file, delimiter=delimitador)
        rows = list(reader)

# Trecho que verifica se o usuario passou nome de coluna ou indice de coluna, assim será optado por manter o cabeçalho ou remover na leitura
    if column_names:
        header = rows[0]
        column_indices = [header.index(column_name) for column_name in column_names]
        rows = rows[1:]  # Remover o cabeçalho
    elif column_indices:
        pass  # Utilizar os índices de coluna fornecidos
    else:
        raise ValueError("Você deve fornecer os nomes das colunas ou o índice da coluna.")

# Verificação da existência de trailer no arquivo
    has_trailer = len(rows) > 1 and len(rows[-1]) != len(rows[-2])
    
    if has_trailer:
        print('Tem trailer')
        trailer = rows[-1]
        rows = rows[:-1]  # Remover o trailer
    else:
        print('Não tem trailer')

# Aplicação da função de mascaramento para os dados escolhidos
    for row in rows:
        for column_index in column_indices:
            mascara_valor(column_index, row, salt)

# Criação de um arquivo novo com os dados mascarados
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=delimitador)
        if column_names:
            writer.writerow(header)  # Escrever o cabeçalho novamente
        writer.writerows(rows)
        if has_trailer:
            writer.writerow(trailer)  # Escrever o trailer novamente

# Confirmação de que o arquivo novo foi gerado
    print(f"Dado mascarado com sucesso. O arquivo {output_file} foi criado.")

# Lista de argumentos a serem fornecidos
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Mascaramento de dados')
    parser.add_argument('-i', '--input_file', type=str, required=True, help='caminho do arquivo de entrada')
    parser.add_argument('-o', '--output_file', type=str, required=True, help='caminho do arquivo de saída')
    parser.add_argument('-n', '--column_names', nargs='+', type=str, help='nomes das colunas que deseja mascarar')
    parser.add_argument('-x', '--column_indices', nargs='+', type=int, help='índices das colunas que deseja mascarar')
    parser.add_argument('-s', '--salt', type=str, required=True, help='salt para mascarar os dados de forma consistente')
    parser.add_argument('-d', '--delimitador', type=str, required=True, help='delimitador do arquivo de origem')
    args = parser.parse_args()

    mascara_dado(args.input_file, args.output_file, args.column_names, args.column_indices, args.salt, args.delimitador)


#