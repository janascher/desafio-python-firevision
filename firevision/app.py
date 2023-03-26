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

    def OpenFileDialog(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Selecionar Arquivo", "", "Arquivos de Imagem (*.jpg *jpeg);;Arquivos de Vídeo (.mp4)")

        if filename:
            new_filename = os.path.join(
                "..\\yolov5\\data\\images", os.path.basename(filename))  
    
            shutil.copy2(filename, new_filename)
            print(f'Cópia do arquivo salvo em {new_filename}')

        try:     
            # Muda de diretório
            os.chdir('../yolov5')
            # Executa um comando no terminal
            os.system('python detect.py --source data/images --weights best.pt')    
            print("Imagem detectada com sucesso")

        except Exception as e:
            print(f'O arquivo foi criado na pasta images do yolov, porém no windows pode apresentar o erro: {e}')

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())