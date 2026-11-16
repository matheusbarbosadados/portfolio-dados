###### **FOTO ESTÚDIO**



Script que remove o fundo de fotos de pessoas e coloca um fundo preto com iluminação dramática, como em uma foto de estúdio.



###### **ARQUIVOS**



**estudio.py** - transforma as fotos escolhidas em fotos com fundo preto



###### **ANTES DE USAR**



1. Instale as bibliotecas: pip install rembg onnxruntime pillow numpy
2. Na primeira vez, o script baixa o modelo de recorte (u2net_human_seg). Por isso, é preciso estar conectado à internet.



###### **COMO USAR**



1. Abra o script e clique no ícone de executar.
2. Escolha uma ou várias fotos na janela que abre.
3. Acompanhe o progresso no terminal.
4. Abra a pasta "resultado", criada ao lado do script.



###### **COMO FUNCIONA**



1. Abre uma janela para escolher as fotos (JPG ou PNG).
2. Corrige a rotação da foto e reduz o tamanho para no máximo 1600 pixels.
3. Remove o fundo e deixa só a pessoa.
4. Simula a luz: clareia o lado esquerdo da pessoa e escurece o lado direito, com ajuste de brilho e contraste.
5. Suaviza a borda do recorte para não ficar contorno do fundo antigo.
6. Cria um fundo preto com um brilho suave do lado oposto à luz.
7. Junta a pessoa com o fundo e salva na pasta "resultado", com o final "_estudio_v2" no nome.
8. No final, mostra o tempo de cada foto no terminal.



###### **AJUSTES**



No começo do script, é possível mudar a luz da esquerda e da direita, o brilho geral, o contraste, o brilho do fundo e a suavização da borda.



###### **BIBLIOTECAS**



rembg, pillow, numpy, onnxruntime, tkinter, pathlib, time



###### **LIMITAÇÕES**



- O modelo foi feito para pessoas. Outros assuntos podem sair com recorte ruim.
- Cabelo, roupas e fundos parecidos com a pessoa podem gerar falhas na borda.
- A primeira execução é mais lenta, pois baixa o modelo.
- Cada foto demora alguns segundos, e muitas fotos de uma vez demoram mais.
- A imagem final tem no máximo 1600 pixels, menor que a original.
- A direção da luz (esquerda para direita) é fixa. Para mudar, é preciso ajustar os valores no código.
