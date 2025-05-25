class ChatbotInterface:
    def __init__(self, inference_engine, explanation_module):
        self.inference_engine = inference_engine
        self.explanation_module = explanation_module

    def start_chat(self):
        print("Hello! I am the AI Candidate Selection System. I can help you decide on job applicants.")
        print("Please provide candidate details (type 'exit' to quit).")

        while True:
            print("\nPlease enter candidate details in a comma-separated format (e.g., experience:5, skill_level:expert, education:master):")
            user_input = input("You: ")

            if user_input.lower() == 'exit':
                print("Goodbye!")
                break

            candidate_data = self._parse_input(user_input)
            if not candidate_data:
                print("Sorry, I couldn't understand the input. Please use the format 'key:value, key:value'.")
                continue

            decision = self.inference_engine.infer_decision(candidate_data)
            fired_rules = self.inference_engine.get_fired_rules()
            explanation = self.explanation_module.generate_explanation(decision, fired_rules, candidate_data)

            print(f"\nAI System: Based on the provided data, the candidate is: {decision}")
            print(f"Explanation:\n{explanation}")

    def _parse_input(self, input_string):
        candidate_data = {}
        parts = input_string.split(',')
        for part in parts:
            if ':' in part:
                key, value = part.split(':', 1)
                key = key.strip()
                value = value.strip()
                try:
                    candidate_data[key] = int(value)
                except ValueError:
                    try:
                        candidate_data[key] = float(value)
                    except ValueError:
                        candidate_data[key] = value
            else:
                return None
        return candidate_data
