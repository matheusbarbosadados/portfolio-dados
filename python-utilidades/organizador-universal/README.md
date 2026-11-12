##### **ORGANIZADOR UNIVERSAL**



Organiza os arquivos de uma pasta em subpastas por categoria, classificando pelo nome e pela extensão. Mostra uma prévia completa e só move os arquivos depois da sua confirmação.



Exemplo: uma pasta com planilhas, imagens, vídeos e documentos soltos termina com as subpastas Planilhas, Imagens, Vídeos e Documentos, cada uma com os seus arquivos.



##### **ARQUIVOS**



1_organizador_universal.py - script principal

teste - pasta para testar com arquivos de vários formatos



##### **REQUISITOS**



- Python 3
- Biblioteca tkinter, que já vem com o Python e abre a janela de escolha da pasta
- Nenhuma instalação adicional



##### **COMO USAR**



1. Abra 1_organizador_universal.py no VS Code e clique no ícone de executar.
2. Na janela que abrir, escolha a pasta que será organizada.
3. Leia no terminal a análise, a prévia da organização e a verificação de conflitos.
4. Digite S ou SIM e aperte Enter para organizar. Qualquer outra resposta cancela.
5. Confira as pastas de categoria criadas dentro da pasta escolhida.



##### **COMO FUNCIONA**



1. Abre a janela e recebe a pasta escolhida.
2. Lista os arquivos da pasta e das subpastas, ignorando as pastas que já têm nome de categoria.
3. Conta os arquivos por extensão.
4. Classifica cada arquivo, nesta ordem de prioridade: regras específicas, palavras inteiras no nome, extensão e, por último, Não classificados.
5. Mostra a prévia de para onde cada arquivo vai e um resumo.
6. Verifica conflitos de nome. Se houver algum, cancela tudo.
7. Pede confirmação e move os arquivos para as pastas de categoria.
8. Mostra o total de arquivos movidos e de não classificados.



##### **REGRAS ESPECÍFICAS**



- Nome com backup e extensão .sql, .db ou .sqlite - Backups
- Nome com financeiro e extensão .xlsx, .xls, .csv ou .pdf - Financeiro
- Nome com curriculo e extensão .pdf, .docx ou .doc - Currículos



##### **CATEGORIAS POR PALAVRA NO NOME**



- Currículos - curriculo, cv
- Contratos - contrato, acordo
- Backups - backup, copia_seguranca
- Estudos - estudo, estudos, apostila, curso, cursos, gabarito, teste, testes
- Vagas - vaga, vagas, linkedin, emprego
- Projetos - projeto, projetos
- Financeiro - financeiro, fatura, boleto, nf, nota fiscal



##### **CATEGORIAS POR EXTENSÃO**



- Documentos - .pdf, .doc, .docx, .txt, .rtf, .odt, .md
- Planilhas - .xls, .xlsx, .csv, .ods
- Apresentações - .ppt, .pptx, .odp
- Imagens - .jpg, .jpeg, .png, .gif, .bmp, .webp
- Vídeos - .mp4, .avi, .mkv, .mov, .wmv
- Áudios - .mp3, .wav, .flac, .aac, .ogg
- Arquivos Compactados - .zip, .rar, .7z, .tar, .gz
- Programas - .exe, .msi, .bat, .cmd, .ps1
- Ícones - .ico
- Power BI - .pbix
- Códigos - .py, .sql, .html, .css, .js, .json
- Não classificados - qualquer outro tipo, ou arquivo sem extensão



##### **LIMITAÇÕES**



- Os arquivos são movidos, não copiados. Não há desfazer nem registro da posição original.
- A estrutura de subpastas se perde, e as subpastas vazias não são removidas.
- O nome tem prioridade sobre a extensão. Exemplo: teste.py vai para Estudos.
- A palavra do nome precisa estar inteira. Exemplo: cv vale em meu_cv.pdf, mas não em cvs.pdf.
- Se houver conflito de nome, nada é movido.
- Pastas com nome de categoria dentro da pasta escolhida são ignoradas.
- Não é indicado para pastas de projeto, de programas instalados ou a raiz do disco.
- As categorias e as palavras-chave ficam no código, e mudar exige editar o script.