import pandas as pd
import os

class AppState:
    def __init__(self):
        self.df: pd.DataFrame = None
        self.preprocessed_df: pd.DataFrame = None
        # Try to load persistent state if it exists
        if os.path.exists("temp_state.pkl"):
            try:
                self.df = pd.read_pickle("temp_state.pkl")
            except:
                pass

state = AppState()
