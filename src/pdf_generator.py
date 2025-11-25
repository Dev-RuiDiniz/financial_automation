from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from pathlib import Path


def generate_pdf(metrics: dict, chart_path: str, output_path: str):
    """
    Gera um PDF básico contendo:
    - Título
    - Métricas financeiras formatadas
    - Gráfico (PNG)
    
    Este é apenas um esqueleto inicial.
    """
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    # Estilos básicos
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    text_style = styles["BodyText"]

    # Documento
    doc = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        title="Relatório Financeiro"
    )

    elements = []

    # Título
    elements.append(Paragraph("Relatório Financeiro Consolidado", title_style))
    elements.append(Spacer(1, 0.5 * cm))

    # Texto de métricas
    metrics_text = f"""
    <b>Faturamento Total:</b> R$ {metrics['faturamento_total']:.2f}<br/>
    <b>Custos Totais:</b> R$ {metrics['custos_totais']:.2f}<br/>
    <b>Lucro Total:</b> R$ {metrics['lucro_total']:.2f}<br/>
    <b>Lucro Percentual:</b> {metrics['lucro_percentual']}%
    """

    elements.append(Paragraph(metrics_text, text_style))
    elements.append(Spacer(1, 1 * cm))

    # Gráfico
    chart_path = Path(chart_path)

    if chart_path.exists() and chart_path.suffix == ".png":
        img = Image(str(chart_path), width=16*cm, height=9*cm)
        elements.append(img)
    else:
        elements.append(Paragraph("O gráfico não pôde ser carregado.", text_style))

    # Conclui PDF
    doc.build(elements)

    return str(output)
