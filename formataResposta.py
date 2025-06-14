import re

def formatar_resposta(resposta):
    # Extrair o texto do conteúdo
    texto = resposta['content']['0']

    # Separar as turmas com regex
    turmas = re.findall(
        r'(\d+\.\sDisciplina:.*?)(?=\n\d+\. Disciplina:|\nEssas turmas|$)',
        texto,
        flags=re.DOTALL
    )

    # Processar e armazenar como texto formatado
    resposta_formatada = []
    for i, turma in enumerate(turmas, 1):
        linha = f"{i}."
        for campo in ['Disciplina', 'Unidade responsável', 'Ementa']:
            match = re.search(rf'{campo}:\s*(.*?)(?=\n\S|$)', turma, flags=re.DOTALL)
            if match:
                valor = match.group(1).strip().replace('\n', ' ')
                linha += f"\n{campo}: {valor}"
        resposta_formatada.append(linha)

    # Adicionar comentário final (se houver)
    if "Essas turmas" in texto:
        observacao = texto.split("Essas turmas")[-1].strip()
        resposta_formatada.append("Observação final: " + observacao)

    # Junta tudo como uma única string
    return "\n\n".join(resposta_formatada)
