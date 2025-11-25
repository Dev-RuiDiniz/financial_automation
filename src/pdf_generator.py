import os
from datetime import datetime

# Removida a dependência do plotly aqui, pois o gráfico vem como imagem
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


def generate_pdf_report_advanced(
    metrics: dict,
    output_path: str,
    chart_path: str = None,
    logo_path: str = None
):
    """
    Gera um PDF profissional contendo:
    - Cabeçalho com logo (opcional)
    - Tabela de métricas
    - Imagem do gráfico (gerado previamente pelo visualizer)
    - Rodapé com data
    """
    logger.info("Iniciando geração do PDF avançado...")

    # Garante que o diretório de saída existe
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Documento PDF
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    # ------------------------------------------------------
    # 1) Cabeçalho com logo ou título
    # ------------------------------------------------------
    if logo_path and os.path.exists(logo_path):
        story.append(Image(logo_path, width=120, height=60))
    else:
        title_style = styles["Title"]
        title_style.alignment = 1  # Center
        story.append(Paragraph("<b>Relatório Financeiro Consolidado</b>", title_style))

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

    # Estilização da Tabela
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
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )

    story.append(table)
    story.append(Spacer(1, 25))

    # ------------------------------------------------------
    # 3) Gráfico (Inserção da Imagem)
    # ------------------------------------------------------
    story.append(Paragraph("<b>Desempenho Financeiro (Gráfico)</b>", styles["Heading2"]))
    story.append(Spacer(1, 10))

    if chart_path and os.path.exists(chart_path):
        # Ajusta tamanho da imagem proporcionalmente
        img = Image(chart_path, width=16 * cm, height=9 * cm)
        story.append(img)
    else:
        logger.warning(f"Gráfico não encontrado no caminho: {chart_path}")
        story.append(Paragraph("<i>Gráfico indisponível no momento.</i>", styles["Normal"]))

    story.append(Spacer(1, 20))

    # ------------------------------------------------------
    # 4) Rodapé com data e hora
    # ------------------------------------------------------
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    footer_style = styles["Normal"]
    footer_style.fontSize = 8
    footer_style.textColor = colors.gray
    
    story.append(Spacer(1, 30))
    story.append(Paragraph(f"Relatório gerado automaticamente em {data_atual}", footer_style))

    # ------------------------------------------------------
    # Finalização do PDF
    # ------------------------------------------------------
    try:
        doc.build(story)
        logger.info(f"PDF gerado com sucesso em: {output_path}")
    except Exception as e:
        logger.error(f"Erro ao gerar PDF: {e}")
        raise