# src/inference_engine.py
class InferenceEngine:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.fired_rules_with_context = [] # Armazenará tuplas (rule_string, candidate_data_snapshot)

    def infer_decision(self, candidate_data):
        self.fired_rules_with_context = [] # Reset para cada nova inferência
        decision = "Undetermined"
        print(f"\n--- Iniciando Inferência para: {candidate_data} ---")

        # Garanta que todas as chaves esperadas pelas regras existam em candidate_data,
        # mesmo que com um valor padrão, para evitar NameError no eval.
        # Isso é uma boa prática para evitar falhas no eval().
        # Você pode listar aqui todas as chaves que suas regras esperam.
        default_candidate_data = {
            'experience': 0,
            'skill_level': 'unknown',
            'education': 'unknown',
            'projects': 0
        }
        # Atualiza os defaults com os dados reais do candidato
        eval_context = {**default_candidate_data, **candidate_data}


        for rule in self.kb.get_rules():
            print(f"Avaliando regra: '{rule}'")
            if "IF" in rule and "THEN" in rule:
                condition_part = rule.split("IF")[1].split("THEN")[0].strip()
                action_part = rule.split("THEN")[1].strip()

                try:
                    # Usamos o eval_context que já contém os dados do candidato
                    # A string da condição é avaliada diretamente contra as chaves em eval_context
                    condition_met = eval(condition_part, {}, eval_context)
                    print(f"  Condição met: {condition_met} (usando contexto: {eval_context})")

                    if condition_met:
                        if "decision =" in action_part:
                            decision = action_part.split("decision =")[1].strip().strip("'\"")
                            self.fired_rules_with_context.append((rule, eval_context.copy())) # Armazena a regra e o snapshot dos dados
                            print(f"  Regra acionada! Decisão: {decision}")
                            print(f"--- Inferência Concluída ---")
                            return decision
                except NameError as ne:
                    print(f"  ERRO (NameError): Variável '{ne}' não definida na regra ou nos dados de entrada. Verifique a correspondência de nomes.")
                    # Pode ocorrer se uma regra espera uma variável que não foi fornecida pelo usuário
                except Exception as e:
                    print(f"  ERRO (Genérico) ao avaliar regra '{rule}': {e}")
        print(f"--- Nenhuma regra acionada. Decisão final: {decision} ---")
        return decision

    def get_fired_rules_with_context(self):
        return self.fired_rules_with_context