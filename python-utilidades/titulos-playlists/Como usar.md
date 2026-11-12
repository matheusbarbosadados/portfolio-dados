##### **GUIA DE USO - CAPTURA DE NOMES EM PLAYLISTS**



**Passo 1:**

Abra a pasta "Captura de Nomes em Playlists" no VS Code.



**Passo 2:**

Só na primeira vez, abra o terminal do VS Code e digite pip install yt-dlp.

Essa é a única biblioteca que precisa instalar.



**Passo 3:**

Abra titulos\_playlists.py e clique no ícone de executar.

Vai abrir uma janelinha para escolher um arquivo.



**Passo 4:**

Se você tem um .txt com links de playlists (um por linha), escolha ele na janelinha.

Se não tem, clique em Cancelar.



**Passo 5:**

Se você cancelou, cole os links no terminal, um por linha.

Quando terminar, aperte Enter em uma linha vazia.



**Passo 6:** 

Aguarde. O terminal mostra "Lendo playlist 1 de ...", depois "OK" com a quantidade de vídeos, e no final um RESUMO.



**Passo 7:** 

Quando terminar, abra a pasta Resultados.

Cada playlist gera um arquivo Titulos - NOME DA PLAYLIST.txt. Cada linha tem o número e o título do vídeo.





###### **ATENÇÃO:**



* Use links que tenham list= no endereço. Esse trecho indica que é uma playlist.
* Linhas com # no início do .txt são ignoradas.
* Se rodar de novo a mesma playlist, o arquivo dela é substituído. Se quiser guardar a versão anterior, copie o .txt antes.
* Se duas playlists tiverem o mesmo nome, a segunda ganha \_2 no final.
* Precisa de internet. Se aparecer "falhou" no RESUMO, confira a conexão e o link.
* Se parar de funcionar do nada, atualize a biblioteca no terminal com pip install -U yt-dlp.
* Vídeos privados ou apagados podem aparecer com título genérico.

