import sys

if len(sys.argv) != 3:
    print("Erro: número de argumentos inválido.")
    sys.exit()

imagem = sys.argv[1]
bins = int(sys.argv[2])

# Abre o arquivo e caso não ache, identifica o erro e sai
try:
    arquivo = open(imagem, "r")
except FileNotFoundError:
    print("Erro: arquivo de imagem não encontrado.")
    sys.exit()

#Lê as linhas do arquivo
linhas = arquivo.readlines()
#Fecha o arquivo uma vez que todas as informações foram extraídas, para poupar memória e processamento.
arquivo.close()

# Trata as linhas, separando-as e ignorando quando temos o comentário referido no trabalho como o nome do arquivo pgm
linhas = [linha.strip() for linha in linhas if linha[0] != "#"]

# Com as linhas tratadas, separa e armazena as informações relevantes
tipo_arquivo = linhas[0]
largura, altura = map(int, linhas[1].split())
maxval = int(linhas[2])

# No trabalho tem a garantia de sempre usar-se P2, mas aqui uma extensão para avaliar o tipo do pgm
if tipo_arquivo != "P2":
    print("Erro: tipo de arquivo inválido. Apenas arquivos P2 são aceitos.")
    sys.exit()

# Verificar se o valor de bins é valido, como descrito no trabalho
if bins > maxval:
  print(f"Erro: número de bins pedido {bins}, mas {maxval} é o valor máximo de intensidade na imagem.")
  sys.exit()

if bins <= 0 :
  print(f"Erro: não é possível gerar {bins} bins.")
  sys.exit()

# mapeia a matriz de pixels fornecida no arquivo
pixels = []
for linha in linhas[3:]:
    pixels.extend(map(int, linha.split()))

# Calcula o tamanho da divisão de cada Bin
tamanho_bin = (maxval + 1) / bins
bins_lista = [0] * bins

for pixel in pixels:
    # Calcular o índice do bin correspondente ao pixel
    indice_bin = int(pixel // tamanho_bin)
    # Incrementa o contador do bin
    bins_lista[indice_bin] += 1

# Calcula a frequência de cada bin
frequencias = [bin / len(pixels) for bin in bins_lista]

# Imprime o output especificado no trabalho
for i in range(bins):    
    limite_inferior = i * tamanho_bin
    limite_superior = (i + 1) * tamanho_bin
    # Formatar os valores com a precisão desejada
    numero_pixels = str(bins_lista[i])
    # Imprimir a linha correspondente ao bin
    print(f"[{limite_inferior:.2f}, {limite_superior:.2f}) {numero_pixels} {frequencias[i]:.5f}")