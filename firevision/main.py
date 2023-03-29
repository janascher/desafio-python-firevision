"""
    Bibliotecas necessárias:
        - **`os`** para interagir com o sistema operacional;
        - **`xml.etree.ElementTree`** para ler e analisar arquivos XML;
        - **`lxml.etree`** para processar e analisar XMLs de forma mais eficiente;
        - **`cv2`** para manipular imagens usando OpenCV;
        - **`glob`** para encontrar arquivos em um diretório.
        - **`typing`** fornece recursos para trabalhar com tipos de dados, anotações de tipo e geração de classes genéricas.
"""
import os
from xml.etree import ElementTree
from lxml import etree
import cv2
from glob import glob

XML_EXT = ".xml"
ENCODE_METHOD = "utf-8"


class PascalVocReader:
    """
        A classe `PascalVocReader` é responsável pela leitura de arquivos no formato Pascal VOC.
    """

    def __init__(self, filepath):
        """
            O método `__init__()` é o construtor da classe e inicializa as variáveis necessárias, como a lista de formas (`shapes`), o caminho do arquivo (`filepath`) e uma variável booleana para verificar se o arquivo foi verificado (verified). Também chama a função `parseXML()` para fazer a análise do arquivo xml.
        """
        self.shapes = []
        self.filepath = filepath
        self.verified = False

        try:
            self.parseXML()
        except:
            pass

    def getShapes(self):
        """
            O método `getShapes()` retorna a lista de formas (`shapes`) encontradas no arquivo xml.
        """
        return self.shapes

    def addShape(self, label, bndbox, filename, difficult):
        """
            O método `addShape()` é responsável por extrair informações sobre uma forma, como rótulo (`label`), coordenadas do retângulo delimitador (`bndbox`), nome do arquivo (`filename`) e se a forma é difícil de ser detectada (`difficult`), e adicioná-las à lista de formas. A partir das coordenadas do retângulo delimitador, o método calcula os pontos dos quatro vértices do retângulo e adiciona-os à lista de formas.
        """
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)
        points = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
        self.shapes.append((label, points, filename, difficult))

    def parseXML(self):
        """
            O método `parseXML()` é responsável por analisar o arquivo XML e extrair informações sobre cada objeto (anotação de objeto) encontrado no arquivo. Ele usa a biblioteca `ElementTree` para analisar o arquivo XML e extrair o caminho da imagem e a variável de verificação. Em seguida, itera sobre cada objeto encontrado no arquivo, extrai informações sobre a forma e chama o método addShape para adicioná-la à lista de formas.
        """
        assert self.filepath.endswith(XML_EXT), "Unsupport file format"
        parser = etree.XMLParser(encoding=ENCODE_METHOD)
        xmltree = ElementTree.parse(self.filepath, parser=parser).getroot()
        path = xmltree.find("path").text

        try:
            verified = xmltree.attrib["verified"]
            if verified == "yes":
                self.verified = True
        except KeyError:
            self.verified = False

        for object_iter in xmltree.findall("object"):
            bndbox = object_iter.find("bndbox")
            label = object_iter.find("name").text

            difficult = False
            if object_iter.find("difficult") is not None:
                difficult = bool(int(object_iter.find("difficult").text))
            self.addShape(label, bndbox, path, difficult)
        return True


class PascalVocConverter:
    """
        A classe `PascalVocConverter` converte anotações de objetos em imagens do formato Pascal VOC para um formato de anotação de detecção de objetos diferente. Para isso, a classe recebe o caminho dos arquivos xml com as anotações, o caminho das imagens correspondentes, o caminho de saída para os arquivos de anotação convertidos, um arquivo de texto com a lista de classes e uma extensão de arquivo (default ".jpg").
    """

    def __init__(self, parentpath, addxmlpath, addimgpath, outputpath, classes_txt, ext=".jpg"):
        """
            O método `__init__()` é o construtor da classe e inicializa o objeto com os caminhos dos diretórios dos arquivos XML, das imagens, a pasta de saída para salvar os arquivos txt gerados, um arquivo de texto que contém os nomes das classes e uma extensão padrão .jpg.
        """
        self.parentpath = parentpath
        self.addxmlpath = addxmlpath
        self.addimgpath = addimgpath
        self.outputpath = outputpath
        self.classes_txt = classes_txt
        self.classes = dict()
        self.num_classes = 0
        self.ext = ext

    def run(self):
        """
            O método `run()` realiza a conversão para o novo formato de anotação e grava os resultados em arquivos de texto separados. Cada arquivo de anotação de detecção de objeto possui uma linha para cada objeto anotado, indicando a classe do objeto e as coordenadas normalizadas do retângulo delimitador que contém o objeto na imagem. Além disso, a classe cria um arquivo de texto classes.txt contendo a lista de todas as classes detectadas nas anotações de entrada.
        """

        if os.path.isfile(self.classes_txt):
            with open(self.classes_txt, "r") as f:
                class_list = f.read().strip().split()
                self.classes = {k: v for (v, k) in enumerate(class_list)}

        xmlPaths = glob(self.addxmlpath + "/*.xml")

        for xmlPath in xmlPaths:
            tVocParseReader = PascalVocReader(xmlPath)
            shapes = tVocParseReader.getShapes()

            with open(self.outputpath + "/" + os.path.basename(xmlPath)[:-4] + ".txt", "w") as f:
                for shape in shapes:
                    class_name = shape[0]
                    box = shape[1]
                    filename = os.path.splitext(
                        self.addimgpath + "/" + os.path.basename(xmlPath)[:-4])[0] + self.ext

                    if class_name not in self.classes.keys():
                        self.classes[class_name] = self.num_classes
                        self.num_classes += 1
                    class_idx = self.classes[class_name]

                    (height, width, _) = cv2.imread(filename).shape

                    coord_min = box[0]
                    coord_max = box[2]

                    xcen = float((coord_min[0] + coord_max[0])) / 2 / width
                    ycen = float((coord_min[1] + coord_max[1])) / 2 / height
                    w = float((coord_max[0] - coord_min[0])) / width
                    h = float((coord_max[1] - coord_min[1])) / height

                    f.write("%d %.06f %.06f %.06f %.06f\n" %
                            (class_idx, xcen, ycen, w, h))
                    print(class_idx, xcen, ycen, w, h)

        with open(self.parentpath + "classes.txt", "w") as f:
            for key in self.classes.keys():
                f.write("%s\n" % key)
                print(key)


def main():
    """
        A função `main()` é o construtor da classe e inicializa o objeto com o caminho do arquivo xml a ser lido e cria algumas variáveis como uma lista vazia de formas (`shapes`) encontradas no arquivo, o caminho do arquivo e uma variável de verificação de integridade do arquivo.
    """
    parent_path = "./"
    addxmlpath = parent_path + "data/training/annotations"
    addimgpath = parent_path + "data/training/images"
    output_path = parent_path + "labels"
    classes_txt = "./fire_classes.txt"

    converter = PascalVocConverter(
        parent_path, addxmlpath, addimgpath, output_path, classes_txt)
    converter.run()


if __name__ == "__main__":
    main()
