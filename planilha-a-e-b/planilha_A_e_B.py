from openpyxl import load_workbook
from copy import copy

# 1. Abrir as duas planilhas
wb_a = load_workbook("Vendas de Informática 30.xlsx")
wb_b = load_workbook("Vendas de Informática 45.xlsx")
ws_a = wb_a.active
ws_b = wb_b.active

# 2. Pegar os IDs que já existem na A
ids_a = {linha[0] for linha in ws_a.iter_rows(min_row=2, values_only=True)}

# 3. Copiar para a A as linhas da B que não existem nela
adicionadas = 0
for linha in ws_b.iter_rows(min_row=2):
    if linha[0].value not in ids_a:
        nova_linha = ws_a.max_row + 1
        for celula in linha:
            destino = ws_a.cell(row=nova_linha, column=celula.column, value=celula.value)
            destino.number_format = celula.number_format
            destino.font = copy(celula.font)
            destino.fill = copy(celula.fill)
            destino.border = copy(celula.border)
            destino.alignment = copy(celula.alignment)
        adicionadas += 1

# 4. Salvar em um arquivo novo
wb_a.save("planilha_a_atualizada.xlsx")
print(f"{adicionadas} vendas adicionadas")