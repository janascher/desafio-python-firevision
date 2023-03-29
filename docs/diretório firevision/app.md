# Arquivo app.py

O `app.py` é uma aplicação gráfica baseada na biblioteca PyQt5 que permite selecionar um arquivo de imagem ou vídeo e executar a detecção de objetos nele. O algoritmo de detecção de objetos utilizado é o YOLOv5, que é executado por meio da chamada do arquivo `detect.py` na pasta `yolov5`.

A aplicação gráfica apresenta uma barra de progresso e duas labels que são atualizadas durante a execução do processo. A primeira label informa o nome do arquivo selecionado e a segunda informa quando a imagem é detectada com sucesso. O código também inclui funções que realizam a cópia do arquivo selecionado para a pasta de entrada do algoritmo de detecção de objetos, a junção dos arquivos de saída do YOLOv5 (caso o processamento tenha gerado arquivos divididos), bem como a função de iniciar o processo de detecção.

::: firevision.app