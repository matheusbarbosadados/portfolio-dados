# Limpeza de Cache e Backup (Windows)

Script em Python que faz um backup das pastas de projetos para o OneDrive e, em seguida, limpa arquivos temporários e caches que apenas ocupam espaço.

**Aviso:** o script apaga arquivos. Leia a lista "O que é limpo" antes de usar.

## O que o script faz

1. **Backup:** copia as pastas de projetos do disco C: para `OneDrive\Backup_C`, usando o robocopy. A cópia só adiciona e atualiza arquivos, nunca apaga nada no destino.
2. **Simulação:** mostra cada pasta de cache, o tamanho e o total que pode ser liberado. Nada é apagado nesta etapa.
3. **Confirmação:** só apaga se for digitado **SIM**. Qualquer outra resposta cancela.
4. **Limpeza:** apaga apenas o conteúdo das pastas da lista, pula arquivos em uso e informa quanto foi liberado.

## Arquivos

| Arquivo | Descrição |
|---|---|
| limpar_cache.py | Script principal |

## O que é limpo

- **Temp do usuário e Temp do Windows:** arquivos temporários
- **pip:** cache de pacotes Python
- **Chrome:** Cache, Code Cache e GPUCache
- **VS Code:** Cache, CachedData, VSIX baixados, Code Cache, GPUCache e Crashpad
- **Notion:** Cache
- **CrashDumps:** relatórios de falhas
- **Explorer:** miniaturas (thumbcache_*.db)

O VSIX baixado é a cópia do instalador de cada extensão do VS Code. As extensões já instaladas ficam em outra pasta e não são afetadas.

## O que NÃO é tocado

- Senhas, cookies, histórico, favoritos e extensões dos navegadores
- Configurações e extensões do VS Code
- Arquivos de recuperação do Power BI (TempSaves)
- Logs do OneDrive, Edge, Playwright e Windows Update
- Qualquer arquivo pessoal ou de projeto

## Regras de segurança

- Lista fixa de pastas: o script não aceita outros caminhos.
- Simulação antes de qualquer exclusão.
- Confirmação manual com **SIM**.
- Links simbólicos são ignorados.
- Arquivos em uso são pulados, sem forçar.
- Aviso para fechar Chrome, VS Code e Notion antes de apagar.

## Como usar

1. Abra o script e altere a linha `pastas = [...]` para as pastas que você quer copiar no backup.
2. Feche Chrome, VS Code e Notion.
3. Abra o PowerShell fora do VS Code, como administrador, para limpar também `C:\Windows\Temp`.
4. Execute:

       python limpar_cache.py

   Se `python` não for reconhecido, use `py`.

Para usar só o backup, rode o script e responda qualquer coisa diferente de SIM na confirmação.

## Resultado do primeiro teste

- Simulação: cerca de 2,5 GB liberáveis.
- Depois da limpeza, os caches ficaram com poucos MB. O navegador recria um pouco ao abrir.

## Observações

- Na primeira abertura depois da limpeza, Chrome e VS Code podem ficar um pouco mais lentos enquanto recriam o cache.
- Pular alguns arquivos é normal (estão em uso ou exigem permissão de administrador).
- Frequência sugerida: uma vez por semana.

## Bibliotecas usadas

os, subprocess (já vêm com o Python)

## Limitações

- Funciona só no Windows.
- Os caminhos do backup e da limpeza estão fixos no código.
