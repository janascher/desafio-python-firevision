import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QProgressBar, QLabel
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtGui import QPixmap

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "FireVision 0.1.0"
        self.left = 220
        self.top = 220
        self.width = 640
        self.height = 480
        self.LoadWindow()

    def LoadWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.step = 0
        self.progress = QProgressBar(self)
        self.progress.setGeometry(200, 250, 250, 20)

        button = QPushButton("Selecionar Arquivo", self)

        button.setToolTip("Clique para selecionar um arquivo")
        button.move(200, 150)
        button.clicked.connect(self.OpenFileDialog)

        self.pixmap = QPixmap('fogo.jpeg')
        self.label2 = QLabel('                                                             ', self)
        self.label2.setStyleSheet('color: blue; font-size: 12px')
        self.label2.move(200, 180)  # Define a posição da label na janela

        self.label = QLabel('                                             ', self)
        self.label.setStyleSheet('color: green; font-size: 16px')
        self.label.move(200, 300)  # Define a posição da label na janela

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

    def start_process(self):
        # Define o valor máximo da barra de progresso
        self.progress.setMaximum(100)

        # Inicia o processo de atualização da barra de progresso
        while self.progress_value < 100:
            self.progress_value += 1
            self.progress.setValue(self.progress_value)

            # Força a interface gráfica a atualizar a barra de progresso
            QApplication.processEvents()

    def progressLoad(self):
        self.step += 20
        self.progress.setValue(self.step)

    def setLabel(self):
        self.label.setText("Imagem detectada com sucesso")

    # def setSelectText(self):
    #     # self.pixmap = QPixmap("caminho_da_imagem.png")
    #     self.label2.setText("../teste/fogo.jpg")

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
            ex.progressLoad()
            data_folder = os.path.join("..", "yolov5", "data")
            images_folder = os.path.join(data_folder, "images")
            if not os.path.exists(images_folder):
                os.makedirs(images_folder)
            new_filename = os.path.join(
                images_folder, os.path.basename(filename))
            
            string = str(new_filename)
            self.label2.setText(string)
        
            shutil.copy2(filename, new_filename)
            ex.progressLoad()
            print(f"Cópia do arquivo salvo em {new_filename}")

        try:
            # Muda de diretório
            os.chdir("../yolov5")
            ex.progressLoad()
            ex.progressLoad()
            # Executa um comando no terminal
            os.system("python detect.py --source data/images --weights best.pt")
            ex.progressLoad()
            # Executa o script "detect.py" indicando o caminho runs/train/exp2/weights/best.pt:
            # os.system("python detect.py --source data/images --weights runs/train/exp2/weights/best.pt")
            # ex.start_process()
            ex.setLabel()
            

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
