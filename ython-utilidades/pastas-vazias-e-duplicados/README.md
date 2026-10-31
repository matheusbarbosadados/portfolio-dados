# Pastas Vazias e Arquivos Duplicados

Script em Python com um menu de duas funções: listar pastas vazias e procurar arquivos duplicados dentro de uma pasta que você escolhe.

**O script não apaga nada.** Ele só mostra os resultados na tela e salva em arquivos de texto.

## O que ele faz

- **Opção 1 - Listar pastas vazias:** encontra as pastas que não têm nenhum arquivo, nem subpastas com conteúdo.
- **Opção 2 - Procurar arquivos duplicados:** encontra arquivos com o mesmo conteúdo, mesmo que tenham nomes diferentes, e mostra quanto espaço as cópias ocupam.
- Abre a janela do Windows para você escolher a pasta.
- Ignora pastas do sistema (Windows, Program Files, etc.) e itens ocultos.

## Arquivos

| Arquivo | Descrição |
|---|---|
| pastas_vazias_e_duplicados.py | Script principal, com menu |

O script cria dois arquivos de resultado, na pasta onde ele é executado: `pastas_vazias.txt` e `arquivos_duplicados.txt`.

## Como usar

1. Execute:

       python pastas_vazias_e_duplicados.py

2. Escolha uma opção no menu: 1 (pastas vazias), 2 (arquivos duplicados) ou 0 (sair).
3. Na janela que abrir, escolha a pasta que você quer analisar.
4. Veja o resultado na tela e no arquivo de texto.

## Como funciona

**Pastas vazias**

1. Percorre todas as subpastas da pasta escolhida.
2. Considera vazia a pasta sem arquivos e sem subpastas com conteúdo.
3. Pastas do sistema e ocultas contam como "com conteúdo", por segurança.
4. Mostra a lista e um resumo.

**Arquivos duplicados**

1. Percorre todos os arquivos da pasta escolhida.
2. Agrupa os arquivos pelo tamanho. Tamanhos diferentes não podem ser cópias.
3. Nos arquivos de mesmo tamanho, calcula o hash SHA-256, que é uma "impressão digital" do conteúdo.
4. Arquivos com a mesma impressão digital são duplicados.
5. Mostra os grupos, do que mais ocupa espaço extra para o que menos ocupa, e um resumo.
6. Arquivos vazios (0 byte) são ignorados.

## Bibliotecas usadas

os, stat, hashlib, tkinter (já vêm com o Python)

## Limitações

- Funciona só no Windows.
- Só lista os resultados. Apagar as pastas ou as cópias é um trabalho manual.
- Em pastas grandes, a busca de duplicados pode demorar.
- Pastas que só têm itens ocultos ou do sistema não aparecem como vazias.
