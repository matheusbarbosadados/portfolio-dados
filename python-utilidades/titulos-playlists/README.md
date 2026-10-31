# Títulos de Playlists do YouTube

Script em Python que lê os títulos dos vídeos de playlists do YouTube e salva em arquivos de texto. Eu uso para montar um índice de estudo das aulas do curso de Python que estou fazendo (Mundos 1 a 4).

**O script não baixa vídeos.** Ele só lê os títulos.

## O que ele faz

- Lê os títulos de cada playlist da lista.
- Salva um arquivo `.txt` para cada playlist, com um título por linha, numerado (exemplo: `01 - Título do vídeo`).
- Pede os títulos em português do Brasil.
- Mostra na tela quantos vídeos foram salvos e avisa se alguma playlist falhou.

## Arquivos

| Arquivo | Descrição |
|---|---|
| titulos_playlists.py | Script principal |

Os arquivos de texto são criados na pasta `playlists_txt`, ao lado do script.

## Como usar

1. Instale a biblioteca:

       pip install yt-dlp

2. Abra o script e, na lista `PLAYLISTS`, coloque o nome do arquivo e o link de cada playlist.
3. Execute:

       python titulos_playlists.py

4. Abra os arquivos na pasta `playlists_txt`.

## Como funciona

1. Percorre a lista de playlists.
2. Para cada uma, usa a biblioteca yt-dlp para ler a lista de vídeos, sem baixar nada.
3. Pega o título de cada vídeo.
4. Salva os títulos em um arquivo `.txt`, um por linha.
5. Se uma playlist der erro, mostra a mensagem e segue para a próxima.
6. No final, mostra um resumo.

## Bibliotecas usadas

yt-dlp, pathlib (já vem com o Python)

## Limitações

- As playlists ficam fixas na lista dentro do código.
- Só funciona com playlists públicas.
- Se o YouTube mudar, a biblioteca yt-dlp pode precisar de atualização (`pip install -U yt-dlp`).
- Salva apenas os títulos, sem links, durações ou descrições.
