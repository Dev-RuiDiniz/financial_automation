import pandas as pd
from pathlib import Path

def load_excel(file_path: str) -> pd.DataFrame:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    if path.suffix not in [".xlsx", ".xls"]:
        raise ValueError("Arquivo precisa ser Excel (.xlsx/.xls)")

    df = pd.read_excel(path)
    
    if df.empty:
        raise ValueError("Arquivo Excel está vazio")
    
    return df
