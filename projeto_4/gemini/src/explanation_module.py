# src/explanation_module.py
# Não precisamos mais de 'import ast' para esta abordagem mais simples
# import ast

class ExplanationModule:
    def __init__(self):
        pass

    def generate_explanation(self, decision, fired_rules_with_context):
        explanation = f"The candidate was **{decision}** because:\n"
        if not fired_rules_with_context:
            explanation += "* No specific rules were triggered for this decision (default decision or no matching criteria).\n"
        else:
            for rule_string, candidate_data_snapshot in fired_rules_with_context:
                explanation += f"- The following rule was applied: '{rule_string}'.\n"
                explanation += self._detail_rule_application(rule_string, candidate_data_snapshot)
        return explanation

    def _detail_rule_application(self, rule_string, candidate_data_snapshot):
        details = ""
        if "IF" in rule_string and "THEN" in rule_string:
            condition_part = rule_string.split("IF")[1].split("THEN")[0].strip()

            details += f"  This was met because, based on the candidate's data:\n"
            
            # Uma abordagem mais simples e robusta para explicar a condição:
            # Iterar sobre as chaves nos dados do candidato e verificar se elas estão na condição
            # e como seus valores se relacionam.
            
            # Quebra a condição em termos (simplificado para exemplo)
            # Isso é uma heurística, não um parser completo.
            terms = condition_part.replace('AND', '@@').replace('OR', '@@').split('@@')
            
            for term in terms:
                term = term.strip()
                if not term:
                    continue

                found_detail = False
                for key, value in candidate_data_snapshot.items():
                    # Verifica se a chave da variável está no termo (ex: 'experience >= 5' contém 'experience')
                    if key in term:
                        # Tenta dar mais detalhes sobre a comparação
                        if '>=' in term:
                            op = '>='
                        elif '<=' in term:
                            op = '<='
                        elif '>' in term:
                            op = '>'
                        elif '<' in term:
                            op = '<'
                        elif '==' in term:
                            op = '=='
                        elif '!=' in term:
                            op = '!='
                        else:
                            op = '' # Se não encontrar operador, apenas mostra a variável e valor

                        # Tenta extrair o valor de comparação da regra (se houver)
                        rule_comparison_value = None
                        try:
                            if op:
                                parts = term.split(op)
                                if len(parts) > 1:
                                    # Usa eval para tentar obter o valor literal da regra
                                    rule_comparison_value = eval(parts[1].strip())
                        except Exception:
                            rule_comparison_value = None # Não conseguiu extrair o valor

                        if op and rule_comparison_value is not None:
                            details += f"    - Candidate's '{key}' is **{value}**, which satisfies the condition `{key} {op} {rule_comparison_value}`.\n"
                        else:
                            details += f"    - Candidate's '{key}' is **{value}** (relevant for condition: `{term}`).\n"
                        found_detail = True
                        # Assume que uma variável só aparece uma vez por termo de comparação simples
                        break
                
                # Se o termo não for uma comparação de variável conhecida, mas ainda faz parte da regra
                if not found_detail:
                    details += f"    - Also considering the condition: `{term}`.\n"
        return details