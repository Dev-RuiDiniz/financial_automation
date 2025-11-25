## 📊 Automação de Relatórios Financeiros

Automação completa para leitura, validação e consolidação de planilhas financeiras, incluindo geração de métricas, gráficos, relatórios em PDF e exportação final em Excel.
---
## 📝 Descrição

Este projeto automatiza todo o fluxo de criação de relatórios financeiros, desde a ingestão de arquivos Excel até a produção final de gráficos e PDFs consolidados.
Ideal para operações repetitivas, rotinas contábeis, controle de vendas e auditorias internas.
---
## 🚀 Tecnologias Utilizadas

Python 3.10+

Pandas — Manipulação e validação de dados

OpenPyXL — Exportação de Excel formatado

Matplotlib — Geração de gráficos leves

ReportLab — Criação de relatórios PDF

Pytest — Testes automatizados
---
## 📂 Estrutura do Projeto
```.
├── data/
│   ├── raw/                   # Planilhas de entrada (.xlsx)
│   └── reports/               # Saídas geradas (PDF, Excel, gráficos)
│
├── src/
│   ├── reader.py              # Leitura e validação dos arquivos
│   ├── transformer.py         # Consolidação e cálculos financeiros
│   ├── visualizer.py          # Geração dos gráficos PNG
│   ├── pdf_generator.py       # Relatório PDF
│   ├── excel_generator.py     # Consolidação em Excel
│   └── main.py                # Pipeline principal
│
├── tests/
│   └── test_reader.py         # Testes do módulo reader
│
├── requirements.txt
└── README.md
```
---
## ▶ Como Rodar o Projeto

1️⃣ Instalar dependências
```
pip install -r requirements.txt
```
2️⃣ Colocar arquivos Excel no diretório:
```
data/raw/
```
3️⃣ Executar o pipeline
```
python src/main.py
```
---
## 📊 Exemplo de Saída
```
📥 Carregando arquivos Excel...
✔ 1 arquivos carregados.
🔍 Validando colunas essenciais...
✔ teste_financeiro.xlsx validado.
🧩 Consolidando DataFrames...
✔ Dados consolidados: 3 linhas.
📊 Calculando métricas...
✔ Métricas calculadas:
  - faturamento_total: 7500
  - custos_totais: 4700
  - lucro_total: 2800
  - lucro_percentual: 37.33
📈 Gerando gráfico financeiro...
✔ Gráfico salvo em: data/reports/grafico_financeiro.png
📄 Gerando PDF...
✔ PDF gerado em: data/reports/relatorio_financeiro.pdf

🎉 Pipeline concluído com sucesso!
```
---
## 🏗 Roadmap (Melhorias Futuras)

- Geração de PDF avançado com layout profissional
- Criar dashboard interativo (Plotly / Dash)
- Adicionar exportação para CSV
- Agendamento de rotinas (cron / Windows Task Scheduler)
- API REST com FastAPI para upload e processamento remoto
- Integração com bancos de dados (PostgreSQL / MongoDB)