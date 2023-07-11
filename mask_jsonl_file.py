import json
import argparse 
import hashlib 

def ler_json(arq_json):
    with open(arq_json, 'r', encoding='utf8') as file:
        for linha in file:
            linha = linha.strip()
            if linha:
                try:
                    json_dict = json.loads(linha)
                    yield json_dict
                except json.JSONDecodeError:
                    print('Erro ao decodificar linha:', linha)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Mascaramento de dados')
    parser.add_argument('-i', '--input_file', type=str, required=True, help='caminho do arquivo de entrada')
    parser.add_argument('-o', '--output_file', type=str, required=True, help='caminho do arquivo de saída')
    parser.add_argument('-n', '--key_names', nargs='+', type=str, required=True, help='nomes das colunas que deseja mascarar')
    parser.add_argument('-s', '--salt', type=str, required=True, help='salt para mascarar os dados de forma consistente')
    args = parser.parse_args()

    json_dicts = ler_json(args.input_file)
    key_names = args.key_names
    salt = args.salt


    with open(args.output_file, 'w', newline="") as file:
        for json_dict in json_dicts:
            for key in json_dict.keys():
                if key in key_names:
                    valor = json_dict[key] + salt
                    mascara = hashlib.sha256(valor.encode()).hexdigest()[:len(json_dict[key])]
                    json_dict[key] = mascara

            linha_mascarada = json.dumps(json_dict)
            file.write(linha_mascarada + '\n')
    
        print(f"Dado mascarado com sucesso. O arquivo {args.output_file} foi criado.")


