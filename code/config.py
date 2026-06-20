from pathlib import Path

# ==============================
# Project Root Directory
# ==============================

BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# Dataset Folder
# ==============================

DATASET_DIR = BASE_DIR / "dataset"

# ==============================
# CSV Files
# ==============================

CLAIMS_CSV = DATASET_DIR / "claims.csv"

SAMPLE_CLAIMS_CSV = DATASET_DIR / "sample_claims.csv"

USER_HISTORY_CSV = DATASET_DIR / "user_history.csv"

EVIDENCE_RULES_CSV = DATASET_DIR / "evidence_requirements.csv"

# ==============================
# Images
# ==============================

IMAGES_DIR = DATASET_DIR / "images"

# ==============================
# Output Folder
# ==============================

OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_CSV = OUTPUT_DIR / "output.csv"