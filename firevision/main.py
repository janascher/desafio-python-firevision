"""
    Importar bibliotecas necessária:
        - **os** para interagir com o sistema operacional;
        - **xml.etree.ElementTree** para ler e analisar arquivos XML;
        - **lxml.etree** para processar e analisar XMLs de forma mais eficiente;
        - **cv2** para manipular imagens usando OpenCV;
        - **glob** para encontrar arquivos em um diretório.
        - **typing** fornece recursos para trabalhar com tipos de dados, anotações de tipo e geração de classes genéricas.
"""
import os
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from lxml import etree
import cv2
from glob import glob
from typing import List, Tuple, Dict, Any

XML_EXT: str = '.xml'
ENCODE_METHOD: str = 'utf-8'


class PascalVocReader:
    def __init__(self, filepath: str) -> None:
        # shapes type:
        # [labbel, [(x1,y1), (x2,y2), (x3,y3), (x4,y4)], color, color, difficult]
        self.shapes: List[Tuple[str, List[Tuple[int, int]], str, bool]] = []
        self.filepath: str = filepath
        self.verified: bool = False
        try:
            self.parseXML()
        except:
            pass

    def getShapes(self) -> List[Tuple[str, List[Tuple[int, int]], str, bool]]:
        return self.shapes

    def addShape(self, label: str, bndbox: Any, filename: str, difficult: bool) -> None:
        """Adiciona uma nova forma à lista de formas existentes.

        Args:
            label (str): O rótulo da forma a ser adicionada.
            bndbox (Any): Um objeto Any que contém as coordenadas da caixa delimitadora da forma a ser adicionada.
            filename (str): O nome do arquivo ao qual a forma pertence.
            difficult (bool): Um valor booleano que indica se a forma é difícil ou não.

        Returns:
            None

        Raises:
            Nenhuma exceção é gerada por esta função.

        Exemplos:
            # criando uma instância da classe e adicionando uma nova forma
            instance = MyClass()
            bndbox = Element('bndbox')
            xmin = SubElement(bndbox, 'xmin')
            xmin.text = '10'
            ymin = SubElement(bndbox, 'ymin')
            ymin.text = '20'
            xmax = SubElement(bndbox, 'xmax')
            xmax.text = '100'
            ymax = SubElement(bndbox, 'ymax')
            ymax.text = '200'
            instance.addShape('retângulo', bndbox, 'imagem1.jpg', False)
        """
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)
        points = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
        self.shapes.append((label, points, filename, difficult))

    """
        Analisar o arquivo XML. O método verifica se o arquivo tem a extensão correta e analisa o arquivo XML usando a biblioteca ElementTree. Ele extrai as informações necessárias do arquivo XML e as adiciona à lista de shapes.
    """
    def parseXML(self) -> bool:
        assert self.filepath.endswith(XML_EXT), "Unsupport file format"
        parser = etree.XMLParser(encoding=ENCODE_METHOD)
        xmltree = ElementTree.parse(self.filepath, parser=parser).getroot()
        filename = xmltree.find('filename').text
        path = xmltree.find('path').text
        try:
            verified = xmltree.attrib['verified']
            if verified == 'yes':
                self.verified = True
        except KeyError:
            self.verified = False

        for object_iter in xmltree.findall('object'):
            bndbox = object_iter.find("bndbox")
            label = object_iter.find('name').text
            # Add chris

            difficult = False
            if object_iter.find('difficult') is not None:
                difficult = bool(int(object_iter.find('difficult').text))
            self.addShape(label, bndbox, path, difficult)
        return True

classes: Dict[str, int] = {}
num_classes: int = 0

# TODO Deixar assim este try ou tirar?
"""
    Definir a função input como raw_input, que é uma função que lê uma string do usuário da linha de comando em Python 2.x. A declaração try é usada para verificar se raw_input está disponível. Se o nome raw_input não estiver definido, o bloco except é executado, que não faz nada. Isso é necessário porque, em Python 3.x, a função raw_input foi renomeada para input, e portanto não é necessário definir input = raw_input. Esse bloco de código permite que o mesmo código possa ser executado tanto em Python 2.x quanto em Python 3.x sem a necessidade de alterar o código.
"""
try:
    input = raw_input
except NameError:
    pass

"""
    Caminho do diretório pai onde se encontram as pastas com as imagens e anotações.
"""
parentpath: str = './' 

"""
    Caminho completo para a pasta com os arquivos XML de anotação.
"""
addxmlpath: str = parentpath + 'data/training/annotations'

"""
    Caminho completo para a pasta com as imagens.
"""
addimgpath: str = parentpath + 'data/training/images'

"""
    Caminho para a pasta onde serão gerados os arquivos no formato YOLO, que contém as informações de anotação das imagens.
"""
outputpath: str = parentpath + 'labels'

"""
    Caminho completo para o arquivo que contém a lista de classes (cada linha representa uma classe).
"""
classes_txt: str = './fire_classes.txt'

"""
    Extensão dos arquivos de imagem a serem processados (somente imagens com a extensão definida serão usadas). Nesse caso, apenas imagens com extensão .jpg serão utilizadas.
"""
ext: str = '.jpg'

"""
    Verificar se o arquivo classes_txt existe. Se existir, ele abre o arquivo, lê seu conteúdo, remove os espaços em branco no início e no final, e divide o conteúdo em uma lista de strings utilizando o método split(). Em seguida, ele cria um dicionário onde as chaves são as strings de classe na lista e os valores são os índices dessas strings na lista. O código utiliza um dicionário para mapear cada classe para um índice numérico, que será utilizado posteriormente para criar os arquivos de anotação no formato YOLO.
"""

if os.path.isfile(classes_txt):
    with open(classes_txt, "r") as f:
        class_list = f.read().strip().split()
        classes = {k : v for (v, k) in enumerate(class_list)}

"""
    Encontrar todos os arquivos com a extensão .xml no diretório especificado.
"""
xmlPaths: List[str] = glob(addxmlpath + "/*.xml")

"""
    Processar cada arquivo XML na lista xmlPaths. Para cada arquivo XML, ele cria uma instância de PascalVocReader usando o caminho do arquivo XML e chama o método getShapes() para obter uma lista de formas (caixas delimitadoras e seus rótulos correspondentes) presentes no arquivo XML.

    Para cada forma na lista de formas, o laço extrai o rótulo da classe e as coordenadas da caixa delimitadora correspondente. Em seguida, o código verifica se o rótulo da classe está presente no dicionário de classes (inicialmente vazio) ou não. Se não estiver presente, ele adiciona a classe ao dicionário com um índice inteiro exclusivo. Em seguida, ele extrai as dimensões da imagem correspondente usando o arquivo de imagem cujo caminho é gerado a partir do caminho do arquivo XML e a extensão do arquivo de imagem.

    Depois disso, o código normaliza as coordenadas da caixa delimitadora, convertendo-as em coordenadas relativas ao tamanho da imagem. Em seguida, ele escreve as informações de rótulo de classe e caixa delimitadora normalizada em um arquivo de texto, cujo caminho é gerado a partir do caminho do arquivo XML e o diretório de saída fornecido. Finalmente, o código imprime as informações de rótulo de classe e caixa delimitadora normalizada na saída padrão.
"""

for xmlPath in xmlPaths:
    tVocParseReader = PascalVocReader(xmlPath)
    shapes = tVocParseReader.getShapes()

    with open(outputpath + "/" + os.path.basename(xmlPath)[:-4] + ".txt", "w") as f:
        for shape in shapes:
            class_name: str = shape[0]
            box: List[Tuple[int, int]] = shape[1]
            filename: str = os.path.splitext(
                addimgpath + "/" + os.path.basename(xmlPath)[:-4])[0] + ext

            if class_name not in classes.keys():
                classes[class_name] = num_classes
                num_classes += 1
            class_idx: int = classes[class_name]

            (height, width, _) = cv2.imread(filename).shape

            coord_min: Tuple[int, int] = box[0]
            coord_max: Tuple[int, int] = box[2]

            xcen: float = float((coord_min[0] + coord_max[0])) / 2 / width
            ycen: float = float((coord_min[1] + coord_max[1])) / 2 / height
            w: float = float((coord_max[0] - coord_min[0])) / width
            h: float = float((coord_max[1] - coord_min[1])) / height

            f.write("%d %.06f %.06f %.06f %.06f\n" %
                    (class_idx, xcen, ycen, w, h))
            print(class_idx, xcen, ycen, w, h)

"""
    Criar um arquivo chamado classes.txt na pasta definida pela variável parentpath e escrever nele as classes identificadas durante o processo de conversão dos arquivos XML em arquivos YOLO.
"""

with open(parentpath + "classes.txt", "w") as f:
    for key in classes.keys():
        f.write("%s\n" % key)
        print(key)
