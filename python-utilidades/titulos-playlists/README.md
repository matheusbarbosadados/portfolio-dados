##### **TÍTULOS DE PLAYLISTS DO YOUTUBE**



Script em Python que lê os títulos dos vídeos de playlists do YouTube e salva em arquivos de texto.

Uso para montar índices de estudo das aulas do curso de Python que estou fazendo.

O script não baixa vídeos. Ele só lê os títulos.



##### **ARQUIVOS**



titulos\_playlists.py - script principal

playlists.txt - lista de links de playlists, um por linha (opcional, você escolhe o arquivo ao abrir o script)

Resultados - pasta criada pelo script, com um .txt para cada playlist

Como usar.md - guia de uso rápido



##### **COMO USAR**



1. Instale a biblioteca yt-dlp, só na primeira vez, no terminal do VS Code: pip install yt-dlp (o tkinter já vem com o Python)
2. Abra o titulos\_playlists.py no VS Code e clique no ícone de executar
3. Na janelinha que abrir, escolha um .txt com links de playlists (um por linha) ou clique em Cancelar
4. Se cancelou, cole os links no terminal, um por linha, e aperte Enter em uma linha vazia para começar
5. Abra a pasta Resultados e confira os arquivos criados



##### **COMO FUNCIONA**



1. Pega os links do arquivo escolhido ou colados no terminal
2. Para cada link, usa a biblioteca yt-dlp para ler a lista de vídeos, sem baixar nada
3. Pega o nome da playlist e o título de cada vídeo
4. Salva os títulos na pasta Resultados, em um arquivo chamado Titulos - NOME DA PLAYLIST.txt, com um título por linha, numerado (exemplo: 01 - Título do vídeo)
5. Se uma playlist der erro, mostra a mensagem e segue para a próxima
6. No final, mostra um resumo com a quantidade de vídeos de cada playlist



##### **LIMITAÇÕES**

* Use links de playlist (com list= no endereço)
* Só funciona com playlists públicas
* Linhas com # no início do .txt são ignoradas
* Se rodar de novo a mesma playlist, o arquivo dela é substituído
* Se duas playlists tiverem o mesmo nome, a segunda recebe \_2 no final
* Se o YouTube mudar, a biblioteca yt-dlp pode precisar de atualização (pip install -U yt-dlp)
* Salva apenas os títulos, sem links, durações ou descrições

