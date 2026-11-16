for i in range(1, 31):
    nome_arquivo = f"{i}.py"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(f"# Arquivo {i}.py\n")
print("30 arquivos criados com sucesso!")
