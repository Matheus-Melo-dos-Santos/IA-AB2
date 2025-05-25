import pandas as pd

class DataLoader:
    @staticmethod
    def load_csv(filepath):
        try:
            df = pd.read_csv(filepath)
            print(f"Successfully loaded data from {filepath}")
            return df
        except FileNotFoundError:
            print(f"Error: File not found at {filepath}")
            return None
        except Exception as e:
            print(f"An error occurred while loading CSV: {e}")
            return None
