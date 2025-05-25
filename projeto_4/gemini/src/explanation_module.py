# src/explanation_module.py
class ExplanationModule:
    def __init__(self):
        pass

    def generate_explanation(self, decision, activated_rule_description, candidate_data):
        explanation = f"The candidate was **{decision}** because:\n"
        
        if not activated_rule_description:
            explanation += "* No specific criteria were met for this decision.\n"
        else:
            explanation += f"* The following condition was met: '{activated_rule_description}'.\n"
            explanation += f"  Based on the candidate's data:\n"
            for key, value in candidate_data.items():
                explanation += f"    - **{key.replace('_', ' ').capitalize()}**: {value}\n"
        return explanation