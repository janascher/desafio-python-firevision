"""
    Importa bibliotecas necessária:
        - **os** para interagir com o sistema operacional;
        - **xml.etree.ElementTree** para ler e analisar arquivos XML;
        - **lxml.etree** para processar e analisar XMLs de forma mais eficiente;
        - **cv2** para manipular imagens usando OpenCV;
        - **glob** para encontrar arquivos em um diretório.
        - **typing** fornece recursos para trabalhar com tipos de dados, anotações de tipo e geração de classes genéricas.
"""
import os
from xml.etree import ElementTree
from lxml import etree
import cv2
from glob import glob

XML_EXT = ".xml"
ENCODE_METHOD = "utf-8"


class PascalVocReader:
    def __init__(self, filepath):
        self.shapes = []
        self.filepath = filepath
        self.verified = False

        try:
            self.parseXML()
        except:
            pass

    def getShapes(self):
        return self.shapes

    def addShape(self, label, bndbox, filename, difficult):
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)
        points = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
        self.shapes.append((label, points, filename, difficult))

    def parseXML(self):
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
    def __init__(self, parentpath, addxmlpath, addimgpath, outputpath, classes_txt, ext=".jpg"):
        self.parentpath = parentpath
        self.addxmlpath = addxmlpath
        self.addimgpath = addimgpath
        self.outputpath = outputpath
        self.classes_txt = classes_txt
        self.classes = dict()
        self.num_classes = 0
        self.ext = ext

    def run(self):

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
