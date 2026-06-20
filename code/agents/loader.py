import pandas as pd
from config import (
    CLAIMS_CSV,
    USER_HISTORY_CSV,
    EVIDENCE_RULES_CSV
)


class DataLoader:

    def __init__(self):
        self.claims = None
        self.user_history = None
        self.evidence_rules = None

    def load_all(self):

        self.claims = pd.read_csv(CLAIMS_CSV)
        self.user_history = pd.read_csv(USER_HISTORY_CSV)
        self.evidence_rules = pd.read_csv(EVIDENCE_RULES_CSV)

        print("✅ Claims Loaded :", len(self.claims))
        print("✅ User History :", len(self.user_history))
        print("✅ Evidence Rules :", len(self.evidence_rules))