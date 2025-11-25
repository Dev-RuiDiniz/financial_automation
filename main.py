import os
import sys
import yaml
from pathlib import Path

from src.reader import load_excel_files, validate_columns
from src.transformer import consolidate_data, calculate_metrics
from src.visualizer import generate_plot
from src.pdf_generator import generate_pdf
from src.excel_generator import generate_excel

sys.stdout.reconfigure(encoding="utf-8")


def load_config():
    """Carrega o arquivo config.yaml com validação."""
    config_path = Path("config.yaml")

    if not config_path.exists():
        raise FileNotFoundError("Arquivo config.yaml não encontrado na raiz do projeto.")

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_pipeline():
    print("⚙️ Carregando configuração...")
    config = load_config()

    raw_path = Path(config["paths"]["raw"])
    reports_path = Path(config["paths"]["reports"])
    required_columns = config["columns"]["required"]

    reports_path.mkdir(parents=True, exist_ok=True)

    print("📥 Carregando arquivos Excel...")
    dfs = load_excel_files(raw_path)
    print(f"✔ {len(dfs)} arquivos carregados.")

    print("🔍 Validando colunas essenciais...")
    for name, df in dfs.items():
        validate_columns(df, required_columns)
        print(f"✔ {name} validado.")

    print("🧩 Consolidando DataFrames...")
    df_final = consolidate_data(dfs)
    print(f"✔ Dados consolidados: {len(df_final)} linhas.")

    print("📊 Calculando métricas...")
    metrics = calculate_metrics(df_final)

    for k, v in metrics.items():
        print(f"  - {k}: {v}")

    print("📈 Gerando gráfico...")
    chart_path = reports_path / "grafico_financeiro.png"
    generate_plot(df_final, str(chart_path))
    print(f"✔ Gráfico salvo em: {chart_path}")

    print("📄 Gerando PDF...")
    pdf_path = reports_path / "relatorio_financeiro.pdf"
    generate_pdf(metrics, str(chart_path), str(pdf_path))
    print(f"✔ PDF gerado em: {pdf_path}")

    print("📊 Salvando Excel consolidado...")
    excel_path = reports_path / "relatorio.xlsx"
    generate_excel(df_final, str(excel_path))
    print(f"✔ Excel salvo em: {excel_path}")

    print("\n🎉 Pipeline concluído com sucesso!")


if __name__ == "__main__":
    run_pipeline()
