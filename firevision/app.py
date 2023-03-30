"""
    Bibliotecas necessárias:
        - **`sys`** para acessar variáveis e funções específicas do sistema;
        - **`os`** para interagir com o sistema operacional;
        - **`shutil`** para integrar com o sistema operacional (por exemplo, criar e manipular arquivos e pastas);
        - **`PyQt5`** para criar janelas e widgets. `QApplication` é a classe principal para gerenciar a aplicação; `QWidget` é a classe base para todos os widgets em PyQt5; `QFileDialog` é usada para abrir caixas de diálogo para selecionar arquivos e pastas; `QPushButton` é um botão que pode ser clicado para executar uma ação; `QProgressBar` é uma barra de progresso que mostra o progresso de uma tarefa; `QLabel` é um rótulo que pode exibir texto e imagens;
        - **`PyQt5.QtGui`** importa a classe `QPixmap` do PyQt5, que é usada para carregar imagens.     
"""

import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QProgressBar, QLabel
from PyQt5.QtGui import QPixmap

class App(QWidget):
    """
        A classe `App` é uma subclasse da classe `QWidget` e é responsável por construir a interface gráfica do usuário para o programa FireVision 0.1.0.
    """

    def __init__(self):
        """
            O método `__init__()` é um método especial que é executado quando um objeto da classe `App` é criado. Neste caso, ele define as dimensões da janela e chama o método `LoadWindow()` para criar a interface gráfica.
        """
        super().__init__()
        self.title = "FireVision 0.1.0"
        self.left = 220
        self.top = 220
        self.width = 640
        self.height = 480
        self.LoadWindow()

        os.system('..\\.venv\\Scripts\\activate')
        os.system("pip install pyinstaller")
        os.system("pip install -r ../requirements.txt")

    def LoadWindow(self):
        """
            O método `LoadWindow()` define a janela, incluindo o título, dimensões e widgets. Ele cria um botão "Selecionar Arquivo" e uma barra de progresso que serão usados posteriormente.
        """
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
        self.label2 = QLabel('                                                        ', self)
        self.label2.setStyleSheet('color: blue; font-size: 12px')
        self.label2.move(200, 180)

        self.label = QLabel('                                               ', self)
        self.label.setStyleSheet('color: green; font-size: 16px')
        self.label.move(200, 300)

        self.show()

    def join_files(self, input_filename, output_filename):
        """
            O método `join_files()` recebe dois parâmetros: `input_filename` e `output_filename`. Ele é responsável por juntar os arquivos de saída gerados pelo modelo de detecção de objeto YOLOv5 em um único arquivo. Esse método é chamado pelo método `OpenFileDialog()`.
        """
        with open(output_filename, 'wb') as f:
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

        print(
            f'Os arquivos {input_filename}.* foram juntados em {output_filename}')

    def start_process(self):
        """
            O método `start_process()` é responsável por definir a barra de progresso com um valor máximo de 100 e atualizar o valor da barra de progresso enquanto o programa está executando.
        """
        self.progress.setMaximum(100)

        while self.progress_value < 100:
            self.progress_value += 1
            self.progress.setValue(self.progress_value)
            QApplication.processEvents()

    def progressLoad(self):
        """
            O método `progressLoad()` é responsável por atualizar o valor da barra de progresso.
        """
        self.step += 20
        self.progress.setValue(self.step)

    def setLabel(self):
        """
            O método `setLabel()` define o texto de uma label da interface gráfica como "Imagem detectada com sucesso".
        """
        self.label.setText("Imagem detectada com sucesso")

    def OpenFileDialog(self):
        """
            O método `OpenFileDialog()` é chamado quando o botão "Selecionar Arquivo" é clicado. Ele usa o método `join_files()` para juntar os arquivos de saída gerados pelo modelo YOLOv5. Em seguida, ele abre um diálogo de seleção de arquivo para que o usuário possa escolher um arquivo de imagem. Ele atualiza a barra de progresso usando o método `progressLoad()` e copia o arquivo selecionado para uma pasta específica. Ele, então, executa o modelo YOLOv5 no arquivo de imagem selecionado usando o método `os.system()`. Finalmente, ele atualiza a barra de progresso novamente e define o texto de uma label para indicar que a imagem foi detectada com sucesso.
        """
        self.join_files("../yolov5/best.pt", "../yolov5/best.pt")

        filename, _ = QFileDialog.getOpenFileName(
            self, "Selecionar Arquivo", "", "Arquivos de Imagem (*.jpg *jpeg);;Arquivos de Vídeo (.mp4)")

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
            ex.setLabel()

        except Exception as e:
            print(f"O arquivo foi criado na pasta images do yolov, porém no windows pode apresentar o erro: {e}")

if __name__ == "__main__":
    """
        O bloco de código `if __name__ == "__main__"`: é responsável por criar um objeto da classe `QApplication` e um objeto da classe `App`. Ele chama o método `exec_()` do objeto `app` para iniciar a execução do programa.
    """
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
