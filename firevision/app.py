import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QProgressBar
from PyQt5.QtCore import QBasicTimer


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "FireVision 0.1.0"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.LoadWindow()

    def LoadWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(200, 250, 250, 20)

        button = QPushButton("Selecionar Arquivo", self)
        button.setToolTip("Clique para selecionar um arquivo")
        button.move(200, 200)
        button.clicked.connect(self.OpenFileDialog)

        self.show()
    def join_files(self,input_filename, output_filename):
    # Abre o arquivo de saída para escrita
        with open(output_filename, 'wb') as f:
            # Lê e grava o conteúdo de cada arquivo de entrada
            i = 0
            while True:
                chunk_filename = f'{input_filename}.{i}'
                if os.path.exists(chunk_filename):
                    with open(chunk_filename, 'rb') as chunk_file:
                        chunk = chunk_file.read()
                        f.write(chunk)
                    i += 1
                else:
                    break
                
        print(f'Os arquivos {input_filename}.* foram juntados em {output_filename}')


    def OpenFileDialog(self):
        self.join_files("../yolov5/best.pt", "../yolov5/best.pt")



        filename, _ = QFileDialog.getOpenFileName(
            self, "Selecionar Arquivo", "", "Arquivos de Imagem (*.jpg *jpeg);;Arquivos de Vídeo (.mp4)")

        """
            Para Windows
        """
    #    if filename:
    #        new_filename = os.path.join(
    #            "..\\yolov5\\data\\images", os.path.basename(filename))

        """                
            >>>> TESTAR NO WINDOWS <<<<
            Desta forma, o código funcionará tanto para Linux quanto para Windows.
            Verificar se foi selecionado um arquivo de imagem pelo usuário. Se sim, cria uma nova pasta "images" dentro da pasta "data" do projeto, caso ela ainda não exista. Em seguida, copia o arquivo de imagem selecionado para a nova pasta "images" e imprime a mensagem informando o local onde o arquivo foi salvo.
        """
        if filename:
            data_folder = os.path.join("..", "yolov5", "data")
            images_folder = os.path.join(data_folder, "images")
            if not os.path.exists(images_folder):
                os.makedirs(images_folder)
            new_filename = os.path.join(
                images_folder, os.path.basename(filename))
            shutil.copy2(filename, new_filename)
            print(f"Cópia do arquivo salvo em {new_filename}")

        try:
            # Muda de diretório
            os.chdir("../yolov5")
            # Executa um comando no terminal
            os.system("python detect.py --source data/images --weights best.pt")
            # Executa o script "detect.py" indicando o caminho runs/train/exp2/weights/best.pt:
            # os.system("python detect.py --source data/images --weights runs/train/exp2/weights/best.pt")
            print("Imagem detectada com sucesso")

        except Exception as e:
            print(
                f"O arquivo foi criado na pasta images do yolov, porém no windows pode apresentar o erro: {e}")

    # def run(self, filename):
    #     self.timer = QBasicTimer()
    #     self.step = 0

    #     if self.timer.isActive():
    #         return

    #     self.timer.start(100, self)

    #     # código para processar o arquivo selecionado

    # def timerEvent(self, e):
    #     if self.step >= 100:
    #         self.timer.stop()
    #         return

    #     self.step += 1
    #     self.progress.setValue(self.step)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
