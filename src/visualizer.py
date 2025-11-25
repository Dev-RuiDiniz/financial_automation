import matplotlib.pyplot as plt
from pathlib import Path
from src.logger import get_logger

# Instancia o logger para manter o padrão dos logs
logger = get_logger()

def generate_plot(df, output_path: str):
    """
    Gera um gráfico de linha usando Matplotlib (faturamento x custos)
    e salva como imagem PNG.
    """
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    # Criar figura
    plt.figure(figsize=(10, 5))

    # Plota as linhas
    plt.plot(df["data"], df["faturamento"], marker="o", label="Faturamento")
    plt.plot(df["data"], df["custos"], marker="o", label="Custos")

    # Ajustes visuais
    plt.title("Faturamento x Custos")
    plt.xlabel("Data")
    plt.ylabel("Valores (R$)")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()

    # Rotacionar datas
    plt.xticks(rotation=45)

    # Salvar imagem
    plt.tight_layout()
    plt.savefig(out, format="png")
    plt.close()

    # CORREÇÃO: Usamos logger.info e removemos o emoji '✔' que quebrava no Windows
    logger.info(f"Grafico salvo em: {out}")