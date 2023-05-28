import json

# Especifica la ruta del archivo JSON de entrada y de salida
input_file_path = 'data.json'
output_file_path = 'converted_data.json'

# Lista de posibles codificaciones
encodings = ['utf-8', 'utf-16', 'latin-1']

# Intenta leer el archivo utilizando diferentes codificaciones
for encoding in encodings:
    try:
        with open(input_file_path, 'r', encoding=encoding) as file:
            data = file.read()
        break
    except UnicodeDecodeError:
        pass

# Convierte el archivo JSON a UTF-8
decoded_data = data.encode('utf-8').decode('utf-8')

# Guarda el archivo convertido
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(decoded_data)

print("Archivo JSON convertido exitosamente a UTF-8.")
