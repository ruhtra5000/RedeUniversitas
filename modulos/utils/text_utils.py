def formata_primeiro_nome(nome_completo):
    return nome_completo.split()[0].capitalize()

def formata_nome_inicial(nome_completo):
    return f"{nome_completo.split()[0].capitalize()} {nome_completo.split()[1][0].capitalize()}."

def formata_nome_sobrenome(nome_completo):
    return f"{nome_completo.split()[0].capitalize()} {nome_completo.split()[1].capitalize()}"