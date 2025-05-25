# main.py
import gradio as gr
from src.knowledge_base import KnowledgeBase
from src.inference_engine import InferenceEngine
from src.explanation_module import ExplanationModule
# from src.chatbot_interface import ChatbotInterface # Não precisamos mais do parser de entrada do chatbot aqui
from src.data_loader import DataLoader # Apenas para referência, não usado na interface Gradio
from src.utils import preprocess_candidate_data # Apenas para referência

# Inicialização dos componentes do sistema (feito uma vez na inicialização da aplicação)
print("Initializing AI Candidate Selection System components...")
kb = KnowledgeBase()

# --- REGRAS MAIS ABRANGENTES E COM 'projects' ---
kb.add_rule("IF experience >= 5 AND skill_level == 'expert' AND projects >= 10 THEN decision = 'Approved'")
kb.add_rule("IF experience >= 3 AND (skill_level == 'intermediate' OR skill_level == 'expert') AND education == 'bachelor' AND projects >= 5 THEN decision = 'Approved Partially'")
kb.add_rule("IF experience >= 1 AND education == 'high school' THEN decision = 'Approved Partially'") # Nova regra para menos experiência mas com escolaridade
kb.add_rule("IF experience < 1 OR skill_level == 'novice' OR projects < 2 THEN decision = 'Rejected'")
# Adicione uma regra padrão para cobrir casos não específicos (catch-all) se desejar,
# mas o "Undetermined" já faz isso.
print("Knowledge Base initialized.")

inference_engine = InferenceEngine(kb)
print("Inference Engine initialized.")

explanation_module = ExplanationModule()
print("Explanation Module initialized.")

print("AI Candidate Selection System Ready!")


def predict_candidate_selection(experience: int, skill_level: str, education: str, projects: int) -> str:
    """
    Função que será exposta pelo Gradio para prever a seleção do candidato.
    """
    candidate_data = {
        'experience': experience,
        'skill_level': skill_level,
        'education': education,
        'projects': projects
    }

    decision = inference_engine.infer_decision(candidate_data)
    # ATENÇÃO: Mudou de get_fired_rules() para get_fired_rules_with_context()
    fired_rules_with_context = inference_engine.get_fired_rules_with_context()
    explanation = explanation_module.generate_explanation(decision, fired_rules_with_context)

    return f"**Decisão:** {decision}\n\n**Justificativa:**\n{explanation}"

# Definição da interface Gradio
iface = gr.Interface(
    fn=predict_candidate_selection,
    inputs=[
        gr.Number(label="Anos de Experiência", value=0, interactive=True), # Adicione values iniciais para teste
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