from src.reader import load_excel
from src.transformer import compute_metrics

def run_pipeline():
    df = load_excel("data/raw/dados.xlsx")
    metrics = compute_metrics(df)
    print(metrics)

if __name__ == "__main__":
    run_pipeline()
