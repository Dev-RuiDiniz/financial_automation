import os
from datetime import datetime

import pandas as pd
import plotly.express as px

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import cm

from src.logger import get_logger

logger = get_logger()


# -------------------------------------------------------------------
# Função auxiliar: gera o gráfico financeiro automaticamente
# -------------------------------------------------------------------
def generate_financial_chart(df: pd.DataFrame, output_path: str) -> str:
    """
    Gera um gráfico PNG com base no DataFrame fornecido.
    X: data
    Y: faturamento

    Retorna o caminho do PNG gerado.
    """
    logger.info("Gerando gráfico financeiro (Plotly)...")

    if "data" not in df.columns or "faturamento" not in df.columns:
        raise ValueError("Colunas 'data' e 'faturamento' são necessárias para o gráfico.")

    fig = px.line(df, x="data", y="faturamento", title="Faturamento ao longo do tempo")

    chart_path = os.path.join(output_path, "grafico_financeiro.png")
    fig.write_image(chart_path)

    logger.info(f"Gráfico gerado em: {chart_path}")
    return chart_path


# -------------------------------------------------------------------
# Função principal: PDF avançado
# -------------------------------------------------------------------
def generate_pdf_report_advanced(
    df: pd.DataFrame,
    metrics: dict,
    output_path: str,
    logo_path: str = None
):
    """
    Gera um PDF profissional contendo:
    - Cabeçalho com logo (opcional)
    - Tabela de métricas
    - Gráfico centralizado
    - Rodapé com data

    df: DataFrame consolidado
    metrics: dicionário com indicadores financeiros
    output_path: pasta destino
    """
    logger.info("Iniciando geração do PDF avançado...")

    os.makedirs(output_path, exist_ok=True)
    pdf_path = os.path.join(output_path, "relatorio_financeiro.pdf")

    # Gera o gráfico automaticamente
    chart_path = generate_financial_chart(df, output_path)

    # Documento PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    # ------------------------------------------------------
    # 1) Cabeçalho com logo ou título
    # ------------------------------------------------------
    if logo_path and os.path.exists(logo_path):
        story.append(Image(logo_path, width=120, height=60))
    else:
        story.append(Paragraph("<b>Relatório Financeiro Consolidado</b>", styles["Title"]))

    story.append(Spacer(1, 20))

    # ------------------------------------------------------
    # 2) Tabela de métricas
    # ------------------------------------------------------
    data = [
        ["Métrica", "Valor"],
        ["Faturamento Total", f"R$ {metrics['faturamento_total']:.2f}"],
        ["Custos Totais", f"R$ {metrics['custos_totais']:.2f}"],
        ["Lucro Total", f"R$ {metrics['lucro_total']:.2f}"],
        ["Lucro Percentual", f"{metrics['lucro_percentual']}%"],
    ]

    table = Table(data, colWidths=[7 * cm, 7 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#004c99")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.gray),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
            ]
        )
    )

    story.append(table)
    story.append(Spacer(1, 20))

    # ------------------------------------------------------
    # 3) Gráfico centralizado
    # ------------------------------------------------------
    story.append(Paragraph("<b>Desempenho Financeiro</b>", styles["Heading2"]))
    story.append(Spacer(1, 10))

    if os.path.exists(chart_path):
        story.append(Image(chart_path, width=15 * cm, height=9 * cm))
    else:
        logger.warning(f"Gráfico não encontrado: {chart_path}")

    story.append(Spacer(1, 20))

    # ------------------------------------------------------
    # 4) Rodapé com data e hora
    # ------------------------------------------------------
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    story.append(Paragraph(f"<i>Relatório gerado em {data_atual}</i>", styles["Normal"]))

    # ------------------------------------------------------
    # Finalização do PDF
    # ------------------------------------------------------
    try:
        doc.build(story)
        logger.info(f"PDF avançado gerado com sucesso em: {pdf_path}")
    except Exception as e:
        logger.error(f"Erro ao gerar PDF: {e}")
        raise

    return pdf_path
