###### **CORTAR VÍDEO**



Script que corta um trecho de um vídeo, escolhendo o início e o fim, e salva o resultado como um arquivo novo.



###### **ARQUIVOS**



**1_editor_video.py** - corta o trecho escolhido do vídeo

**sons.py** - toca um aviso sonoro quando o corte termina (opcional)



###### **ANTES DE USAR**



1. Instale as bibliotecas: pip install imageio-ffmpeg pygame
2. Se já tiver o FFmpeg instalado no Windows, o script usa ele automaticamente.
3. Para o aviso sonoro, deixe o sons.py na mesma pasta do cortar_video.py.



###### **COMO USAR**



1. Abra o script e clique no ícone de executar.
2. Escolha o vídeo na janela que abre.
3. Informe o início e o fim do corte no terminal. Se apertar Enter sem escolher nada, o corte começa no início ou vai até o final do vídeo.
4. Escolha o modo: 1 (rápido) ou 2 (preciso).
5. Aguarde a mensagem de conclusão e abra o arquivo gerado.



###### **COMO FUNCIONA**



1. Procura o FFmpeg instalado ou o que vem com o imageio-ffmpeg.
2. Abre uma janela para escolher o vídeo.
3. Aceita o tempo em minutos e segundos (5:01), só em segundos (301) ou em horas, minutos e segundos (1:01:00).
4. Confere se o fim é maior que o início.
5. No modo rápido, copia o trecho sem refazer o vídeo, sem perda de qualidade.
6. No modo preciso, refaz o vídeo e corta no ponto exato, mas demora mais.
7. Salva o resultado na mesma pasta do vídeo, com o final "_corte" no nome. Se o nome já existir, cria "_corte2", "_corte3" e assim por diante, sem apagar nada.
8. No final, mostra o tempo total de execução e toca o aviso sonoro.



###### **BIBLIOTECAS**



imageio-ffmpeg, pygame (opcional), tkinter, subprocess, shutil, pathlib, time, os



###### **LIMITAÇÕES**



- Depende do FFmpeg.
- No modo rápido, o corte pode variar alguns segundos em relação ao tempo informado.
- O modo preciso é mais lento, pois refaz o vídeo.
- Corta apenas um trecho por vez.
- Sem o pygame, o aviso sonoro usa um beep simples do Windows.
