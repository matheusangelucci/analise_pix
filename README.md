# 📊 Projeto — Análise do Pix no Brasil (2020–2024)

## 📌 Descrição
Este projeto tem como objetivo analisar a evolução do **Pix** no Brasil entre 2020 e 2024, comparando-o a outros meios de pagamento (TED, Cheque e Boleto).  
Foram aplicadas técnicas de **manipulação de dados com Pandas** e **visualização com Matplotlib**, resultando em insights sobre crescimento, participação relativa e sazonalidade do Pix.

---

## 📂 Estrutura do Projeto
- **`PROJETO_01_combustiveisBR.py`** → script principal com todo o fluxo de análise.  
- **`/files/`** → arquivos exportados (CSV e TXT) com resultados das análises.  
- **`/img/`** → gráficos gerados durante a execução.  

---

## ⚙️ Tecnologias Utilizadas
- Python 3.x  
- Pandas  
- Matplotlib  

---

## 📑 Etapas da Análise
### 1. Comparativo Pix x Outros meios
Função `fun_1_volume_pix_vs_outros`  
- Quantidade e Valor totais de Pix, TED, Cheque e Boleto.  
- Gráfico comparativo salvo em `/img/plot_func01_pix_vs_outros.png`.  

### 2. Séries temporais do Pix
Função `fun_2_timeseries_pix`  
- Evolução **anual e mensal** de quantidade e valor do Pix.  
- Gráficos salvos em:  
  - `/img/ano_func_02_plot_QTD_VLR.png`  
  - `/img/mes_func_02_plot_QTD_VLR.png`  

### 3. Crescimento percentual (2020 → 2024)
Função `fun_3_percentaul_pix_ano`  
- Calcula a variação percentual do Pix, TED e Boleto em quatro anos.  
- Resultados exportados em `/files/resultados.txt`.  

### 4. Picos sazonais
Função `fun_4_picos_datas`  
- Identifica meses com maior e menor volume de Pix.  
- Exporta CSVs com top 6 meses de maior/menor movimento.  
- Resultados também registrados em `/files/resultados.txt`.  

---

## 📊 Resultados Principais
- O **Pix** teve crescimento de mais de **+13.000%** entre 2020 e 2024.  
- Métodos tradicionais como **TED (-81%)** e **Boleto (-52%)** apresentaram forte queda.  
- Os meses de maior movimentação foram **maio, março, abril e dezembro**.  

---


## 🚀 Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/matheusangelucci/analise_pix.git
   cd seu-repo

2. Instale as dependências:
   ```bash
   pip install pandas matplotlib

3. Execute o script principal:
   ```bash
   python PROJETO_01_combustiveisBR.py


## 📌 Autor
Projeto desenvolvido por **Matheus Alexandre** 💻  
📎 [LinkedIn](https://www.linkedin.com/in/matheus-alexandre-788848294/) | [GitHub](https://github.com/matheusangelucci)


