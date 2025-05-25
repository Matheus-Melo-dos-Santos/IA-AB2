class KnowledgeBase:
    def __init__(self):
        self.rules = []
        self.facts = {}

    def add_rule(self, rule_string):
        self.rules.append(rule_string)
        print(f"Rule added: {rule_string}")

    def get_rules(self):
        return self.rules

    def add_fact(self, fact_name, fact_value):
        self.facts[fact_name] = fact_value
        print(f"Fact added: {fact_name} = {fact_value}")

    def get_fact(self, fact_name):
        return self.facts.get(fact_name)
