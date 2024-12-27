#Lucas Constante Mosquini - 11858258

#Fiz o Trabalho sozinho, professor.

import argparse
import math
class Image:
    # Inicialização com os parâmetros requeridos
    def __init__(self, magic_number, dimensions, maxval, pixels):
        self.magic_number = magic_number
        self.dimensions = dimensions
        self.maxval = maxval
        self.pixels = pixels

    # O método de Thresholding funcionando
    def thresholding(self, t=127):
        binary_pixels = [0 if pixel < t else 255 for pixel in self.pixels]
        return Image(self.magic_number, self.dimensions, self.maxval, binary_pixels)

    # O método de sgt funcionando
    def sgt(self, dt=1):
        T = sum(self.pixels) // len(self.pixels)
        prev_T = T - dt - 1
        while abs(T - prev_T) > dt:
            prev_T = T
            G1 = sum(pixel < T for pixel in self.pixels)
            G2 = sum(pixel >= T for pixel in self.pixels)
            m1 = sum(pixel for pixel in self.pixels if pixel < T) // G1 if G1 > 0 else 0
            m2 = sum(pixel for pixel in self.pixels if pixel >= T) // G2 if G2 > 0 else 0
            T = (m1 + m2) // 2
        binary_pixels = [0 if pixel < T else 255 for pixel in self.pixels]
        return Image(self.magic_number, self.dimensions, self.maxval, binary_pixels), T


    # Professor, os métodos mean e median estão com problemas. Fiz uma lambança e não consegui resolver a tempo de entregar o trabalho, então
    # deixei do jeito que está. Tentei fazer usando comprehension mas acabei me confundindo. 

# ----------------------------------------------------------------------------------------------------------------------------------------------
    def mean(self, k=3):
        new_pixels = []
        pad = k // 2
        for y in range(self.dimensions[1]):
            for x in range(self.dimensions[0]):
                vizinhos = [self.pixels[max(0, min(y_, self.dimensions[1] - 1)) * self.dimensions[0] + max(0, min(x_, self.dimensions[0] - 1))] for y_ in range(y - pad, y + pad + 1) for x_ in range(x - pad, x + pad + 1)]
                new_pixels.append(sum(vizinhos) // len(vizinhos))
        return Image(self.magic_number, self.dimensions, self.maxval, new_pixels)

    def median(self, k=3):
        new_pixels = []
        pad = k // 2
        for y in range(self.dimensions[1]):
            for x in range(self.dimensions[0]):
                vizinhos = [self.pixels[max(0, min(y_, self.dimensions[1] - 1)) * self.dimensions[0] + max(0, min(x_, self.dimensions[0] - 1))] for y_ in range(y - pad, y + pad + 1) for x_ in range(x - pad, x + pad + 1)]
                vizinhos.sort()
                median = vizinhos[len(vizinhos) // 2]
                new_pixels.append(median)
        return Image(self.magic_number, self.dimensions, self.maxval, new_pixels)

# ----------------------------------------------------------------------------------------------------------------------------------------------
    def sobel(self):
        #Matriz com o kernel pedido no pdf
        Gx = [-1, 0, 1, -2, 0, 2, -1, 0, 1]
        Gy = [-1, -2, -1, 0, 0, 0, 1, 2, 1]

        gradiente_x = self.aux(Gx)
        gradiente_y = self.aux(Gy)

        #equação 5 do pdf
        magnitude = [int(math.sqrt(gx ** 2 + gy ** 2)) for gx, gy in zip(gradiente_x.pixels, gradiente_y.pixels)]
        max_magnitude = max(magnitude)
        mag_fin = [int(pixel / max_magnitude * 255) for pixel in magnitude]

        return Image(self.magic_number, self.dimensions, self.maxval, mag_fin)

    #método auxiliar para o sobel
    def aux(self, kernel):
        new_pixels = []
        pad = int(math.sqrt(len(kernel))) // 2
        for y in range(self.dimensions[1]):
            for x in range(self.dimensions[0]):
                vizinhos = [self.pixels[max(0, min(y_, self.dimensions[1] - 1)) * self.dimensions[0] + max(0, min(x_, self.dimensions[0] - 1))] for y_ in range(y - pad, y + pad + 1) for x_ in range(x - pad, x + pad + 1)]
                pixel_novo = sum(neighbor * weight for neighbor, weight in zip(vizinhos, kernel))
                new_pixels.append(pixel_novo)
        return Image(self.magic_number, self.dimensions, self.maxval, new_pixels)

    # O módulo responsável por emitir o print requerido no pdf
    def display_info(self, T=None):
        mean_value = sum(self.pixels) // len(self.pixels)
        median_value = sorted(self.pixels)[len(self.pixels) // 2]
        print(f"magic_number {self.magic_number}")
        print(f"dimensions {self.dimensions}")
        print(f"maxval {self.maxval}")
        print(f"mean {mean_value}")
        print(f"median {median_value}")
        if T is not None:
            print(f"T {T}")

    # O módulo responsável por salvar a imagem, depois de processada, no arquivo com destino pedido.
    def save(self, output_path):
        with open(output_path, "w") as f:
            f.write(f"{self.magic_number}\n")
            f.write(f"{self.dimensions[0]} {self.dimensions[1]}\n")
            f.write(f"{self.maxval}\n")
            f.write("\n".join(str(pixel) for pixel in self.pixels))

# O módulo responsável por ler os parâmetros (dados no pdf) do arquivo da imagem e guardá-los em variáveis do programa.
def load_image(image_path):
    with open(image_path, "r") as f:
        magic_number = f.readline().strip()
        dimensions = tuple(map(int, f.readline().strip().split()))
        maxval = int(f.readline().strip())
        pixels = list(map(int, f.read().strip().split()))
        return Image(magic_number, dimensions, maxval, pixels)


# Aqui o módulo principal do programa, responsável por rodá-lo
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--imgpath", type=str, required=True)
    parser.add_argument("--op", nargs='+', required=True)
    parser.add_argument("--outputpath", type=str, default=None)

    args = parser.parse_args()

    img = load_image(args.imgpath)

    result_img = img
    for i in range(0, len(args.op), 2):
        operation = args.op[i]
        parameters = args.op[i+1]
        if operation == "thresholding":
            result_img = result_img.thresholding(t=int(parameters))
        elif operation == "sgt":
            result_img, T = result_img.sgt(dt=int(parameters))
        elif operation == "mean":
            result_img = result_img.mean(k=int(parameters))
        elif operation == "median":
            result_img = result_img.median(k=int(parameters))
        elif operation == "sobel":
            result_img = result_img.sobel()
        else:
            print("Operação não listada")
            return

    result_img.display_info(T=T)

    if args.outputpath:
        result_img.save(args.outputpath)

#Aqui, usei o conceito que o senhor falou nas últimas aulas, para que possa-se importar esse programa como módulo, sem rodá-lo e podendo alterá-lo
if __name__ == "__main__":
    main()