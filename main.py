import os
from src.reader import load_excel_files, validate_columns
from src.transformer import consolidate_data, calculate_metrics
from src.visualizer import generate_plot
from src.pdf_generator import generate_pdf
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding='utf-8')

def run_pipeline():
    print("📥 Carregando arquivos Excel...")

    raw_path = "data/raw"
    dfs = load_excel_files(raw_path)

    print(f"✔ {len(dfs)} arquivos carregados.")

    print("🔍 Validando colunas essenciais...")

    required = ["data", "faturamento", "custos"]
    for name, df in dfs.items():
        validate_columns(df, required)
        print(f"✔ {name} validado.")

    print("🧩 Consolidando DataFrames...")

    df_final = consolidate_data(dfs)
    print(f"✔ Dados consolidados: {len(df_final)} linhas.")

    print("📊 Calculando métricas...")

    metrics = calculate_metrics(df_final)
    print("✔ Métricas calculadas:")
    for k, v in metrics.items():
        print(f"  - {k}: {v}")

    print("📈 Gerando gráfico financeiro...")

    reports_dir = Path("data/reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    chart_path = reports_dir / "grafico_financeiro.png"
    generate_plot(df_final, str(chart_path))
    print(f"✔ Gráfico salvo em: {chart_path}")

    print("📄 Gerando PDF...")

    pdf_path = reports_dir / "relatorio_financeiro.pdf"
    generate_pdf(metrics, str(chart_path), str(pdf_path))
    print(f"✔ PDF gerado em: {pdf_path}")

    print("\n🎉 Pipeline concluído com sucesso!")


if __name__ == "__main__":
    run_pipeline()
