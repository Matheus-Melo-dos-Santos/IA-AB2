def avaliar_candidato(dados):
    experiencia = dados.get("experiencia", 0)
    formacao = dados.get("formacao", "").lower()
    habilidades = dados.get("habilidades", "").lower()

    if experiencia >= 3 and "python" in habilidades:
        return "Aprovado"
    elif experiencia >= 1:
        return "Aprovado parcialmente"
    else:
        return "Reprovado"

