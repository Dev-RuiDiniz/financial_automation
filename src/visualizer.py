import plotly.graph_objects as go
from pathlib import Path


def generate_plot(df, output_path: str):
    """
    Gera um gráfico de linha com Faturamento e Custos ao longo do tempo.
    O formato é decidido pela extensão do arquivo:
      - .png  → salva como imagem
      - .html → salva como arquivo interativo
    """

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    if "data" not in df.columns:
        raise ValueError("A coluna 'data' é obrigatória para gerar o gráfico.")

    if not {"faturamento", "custos"}.issubset(df.columns):
        raise ValueError("As colunas 'faturamento' e 'custos' são obrigatórias.")

    fig = go.Figure()

    # Linha de faturamento
    fig.add_trace(go.Scatter(
        x=df["data"],
        y=df["faturamento"],
        mode="lines",
        name="Faturamento"
    ))

    # Linha de custos
    fig.add_trace(go.Scatter(
        x=df["data"],
        y=df["custos"],
        mode="lines",
        name="Custos"
    ))

    fig.update_layout(
        title="Faturamento vs Custos",
        xaxis_title="Data",
        yaxis_title="Valor (R$)",
        template="plotly_white",
        hovermode="x unified"
    )

    # Escolhe formato
    if out.suffix == ".html":
        fig.write_html(str(out))
    elif out.suffix == ".png":
        fig.write_image(str(out))
    else:
        raise ValueError("Formato inválido. Use .png ou .html")

    return str(out)
