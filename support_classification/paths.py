from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

RAW_CSV_PATH = RAW_DIR / "helpdesk_customer_tickets.csv"
TRAIN_DATASET_PATH = PROCESSED_DIR / "train_dataset.csv"
TEST_DATASET_PATH = PROCESSED_DIR / "test_dataset.csv"
