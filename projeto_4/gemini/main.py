import gradio as gr
from src.explanation_module import ExplanationModule # Agora só precisamos disso

# Inicialização do módulo de explicação
print("Initializing Explanation Module...")
explanation_module = ExplanationModule()
print("Explanation Module initialized.")

print("AI Candidate Selection System Ready!")

def predict_candidate_selection(experience: int, skill_level: str, education: str, projects: int) -> str:
    """
    Função que será exposta pelo Gradio para prever a seleção do candidato,
    com regras implementadas diretamente via if/elif/else.
    """
    candidate_data = {
        'experience': experience,
        'skill_level': skill_level,
        'education': education,
        'projects': projects
    }

    decision = "Undetermined"
    activated_rule_description = "" # Armazenará a descrição da regra ativada para justificativa

    # --- IMPLEMENTAÇÃO DIRETA DAS REGRAS COM IF/ELIF/ELSE ---
    # As regras são verificadas em ordem de prioridade (da mais específica para a mais geral, ou por aprovação/rejeição)

    # Regra 1: Aprovado (critérios altos)
    if experience >= 5 and skill_level == 'expert' and projects >= 10:
        decision = 'Approved'
        activated_rule_description = "Experience is 5 or more, skill level is 'expert', AND 10 or more relevant projects."
    
    # Regra 2: Reprovado (critérios baixos) - geralmente bom verificar reprovações cedo
    elif experience < 1 or skill_level == 'novice' or projects < 2:
        decision = 'Rejected'
        activated_rule_description = "Experience is less than 1 year, OR skill level is 'novice', OR less than 2 relevant projects."

    # Regra 3: Aprovado Parcialmente (critérios intermediários ou específicos)
    elif experience >= 3 and (skill_level == 'intermediate' or skill_level == 'expert') and education == 'bachelor' and projects >= 5:
        decision = 'Approved Partially'
        activated_rule_description = "Experience is 3 or more, skill level is 'intermediate' or 'expert', education is 'bachelor', AND 5 or more relevant projects."
    
    # Regra 4: Aprovado Parcialmente (experiência menor, mas com escolaridade básica)
    elif experience >= 1 and education == 'high school':
        decision = 'Approved Partially'
        activated_rule_description = "Experience is 1 or more year, AND education is 'high school'."
    
    # Caso nenhuma regra específica seja ativada (permanece "Undetermined")
    else:
        decision = "Undetermined"
        activated_rule_description = "" # Nenhuma regra específica ativada

    # Gerar a justificativa
    explanation = explanation_module.generate_explanation(decision, activated_rule_description, candidate_data)

    return f"**Decisão:** {decision}\n\n**Justificativa:**\n{explanation}"

# Definição da interface Gradio
iface = gr.Interface(
    fn=predict_candidate_selection,
    inputs=[
        gr.Number(label="Anos de Experiência", value=0, interactive=True),
        gr.Dropdown(label="Nível de Habilidade", choices=['novice', 'intermediate', 'expert'], value='novice', interactive=True),
        gr.Dropdown(label="Escolaridade", choices=['high school', 'bachelor', 'master', 'phd'], value='high school', interactive=True),
        gr.Number(label="Número de Projetos Relevantes", value=0, interactive=True)
    ],
    outputs=gr.Markdown(label="Resultado da Seleção e Justificativa"),
    title="Sistema de Seleção de Candidatos por IA",
    description="Insira os detalhes do candidato para obter uma decisão de seleção e sua justificativa."
)

if __name__ == "__main__":
    iface.launch()