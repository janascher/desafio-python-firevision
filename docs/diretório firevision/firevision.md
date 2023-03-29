# Arquivo main.py

O `main.py` é um script Python que lê arquivos de anotação no formato Pascal VOC (Visual Object Classes) e converte essas anotações em arquivos de texto no formato YOLO (You Only Look Once), que é um formato popular para treinamento de modelos de detecção de objetos em imagens.

O script lê arquivos de anotação xml e, para cada anotação, extrai informações sobre as caixas delimitadoras dos objetos na imagem, bem como os rótulos desses objetos. Ele então converte essas informações em um formato YOLO compatível e grava um arquivo de texto correspondente. Além disso, ele cria um arquivo de texto com a lista de classes presentes nas anotações, que é útil para treinar modelos de detecção de objetos.

O código depende de algumas bibliotecas Python, incluindo `os`, `xml.etree.ElementTree`, `lxml`, `cv2` e `glob`. Além disso, ele usa algumas variáveis globais, como o caminho para os arquivos de anotação XML, o caminho para as imagens, o caminho de saída para os arquivos de texto e o formato das imagens. O código também lida com a leitura de um arquivo de texto opcional que lista as classes presentes nas anotações.

::: firevision.main