import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# Define o caminho onde será salvo o arquivo .txt com os resultados do projeto.
resultadostxt = '../TRAININGS/PROJETO_01_pix/files/resultados.txt'

# Lê o arquivo .csv com os dados usados nas análises e armazena eles num Dataframe
df = pd.read_csv('../TRAININGS/PROJETO_01_pix/brazilian_payment_methods.csv')

# Removendo colunas de meios de pagamento que não serão usados no projeto.
df.drop(df.columns[[5, 6, 11, 12]], axis=1, inplace=True)
''' Explicação da linha acima:
    a função drop recebe os indíces por meio do método columns com uma lista aninhada (2d por conta do Dataframe ser um conjunto com duas dimensões)
    atributo "axis" dita se a função drop deve remover linhas (axis=0) ou colunas (axis=1)
    atributo "inplace" dita se o df será modificado ou se a função drop vai criar um novo df.'''

# Função de análise do volume do Pix em relação a outros meios de pagamento
def fun_1_volume_pix_vs_outros(dados):

    # Soma do total do valor e da quantidade. Também é feita uma divisão para adequar as casas decimais (milhões para a quantidade e bilhões para o valor) 
    Q_pix = round(sum(dados['quantityPix']/1_000_000))
    V_pix = round(sum(dados['valuePix'])/1_000_000, 2)

    Q_ted = round(sum(dados['quantityTED']/1_000_000))
    V_ted = round(sum(dados['valueTED']/1_000_000), 2)

    Q_cheque = round(sum(dados['quantityBankCheck']/1_000_000))
    V_cheque = round(sum(dados['valueBankCheck']/1_000_000), 2)

    Q_boleto = round(sum(dados['quantityBrazilianBoletoPayment']/1_000_000))
    V_boleto = round(sum(dados['valueBrazilianBoletoPayment']/1_000_000), 2)

    # Dataframe é criado com os dados da análise, depois esse Dataframe é salvo em um arquivo .csv
    colunas = ['QTD_PIX (Milhões)', 'VLR_PIX (Bilhões)', 'QTD_TED (Milhões)', 'VLR_TED (Bilhões)', 'QTD_CHEQUE (Milhões)', 'VLR_CHEQUE (Bilhões)', 'QTD_BOLETO (Milhões)', 'VLR_BOLETO (Bilhões)']
    output_dados = [[Q_pix, V_pix, Q_ted, V_ted, Q_cheque, V_cheque, Q_boleto, V_boleto]]

    analise_01_volumes = pd.DataFrame(output_dados, columns = colunas)
    analise_01_volumes.to_csv('../TRAININGS/PROJETO_01_pix/files/func01_pix_vs_outros.csv')

    # Gráfico de barras com dados de quantidade: Pix vs Outros meios de pagamento
    grafico_caminho = '../TRAININGS/PROJETO_01_pix/img/plot_func01_pix_vs_outros.png'
    
    plot_dados = [Q_pix, Q_ted, Q_cheque, Q_boleto]
    plot_colunas = ['QTD_PIX (Milhões)', 'QTD_TED (Milhões)', 'QTD_CHEQUE (Milhões)', 'QTD_BOLETO (Milhões)']

    plt.figure(figsize=(10,10)) # Tamanho da figura (espaço onde fica o/os gráfico)
    plt.bar(plot_colunas, plot_dados) # Define dados usados nas barras do gráfico
    plt.scatter(plot_colunas, plot_dados) # Define dados usados na linha do gráfico
    plt.plot(plot_colunas, plot_dados) # Define dados usados nos eixos X e Y do gráfico
    plt.suptitle('PIX vs OUTROS MEIOS DE PAGAMENTO') # Define o título do gráfico
    plt.savefig(grafico_caminho) # Gráfico é salvo numa imagem

# Função que cria séries temporais de quantidade e valor do Pix entre 2020 e 2024 
def fun_2_timeseries_pix(dados):

    # Quantidade e valor são convertidos para um formato de melhor visulização
    dados['valuePix'] = round(dados['valuePix']/1_000_000, 2)
    dados['quantityPix'] = round(dados['quantityPix']/1_000_000)

    # Define variável contendo o recorte de ano das data presentes no Dataframe
    data_ano = pd.to_datetime(dados['YearMonth'].astype(int), format='%Y%m').dt.year
    
    '''A função groupby() é usada para agrupar o total de Quantidade e Valor pelo ano,
    # depois os resultados são armazenados em varíaveis para usar na Série temporal.'''
    ano_valor = dados.groupby(pd.to_datetime(dados['YearMonth'].astype(int), format='%Y%m').dt.year)['valuePix'].sum()
    ano_quantidade = dados.groupby(pd.to_datetime(dados['YearMonth'].astype(int), format='%Y%m').dt.year)['quantityPix'].sum()
    
    # Define variáveis de Quantidade e Valor, e faz o fatiamento do mês no campo de data delas.
    mes_valor = dados[['YearMonth', 'valuePix']]
    mes_valor['YearMonth'] = pd.to_datetime(dados['YearMonth'].astype(int), format='%Y%m').dt.month
    
    mes_quantidade = dados[['YearMonth', 'quantityPix']]
    mes_quantidade['YearMonth'] = pd.to_datetime(dados['YearMonth'].astype(int), format='%Y%m').dt.month

    '''São criadas as séries temporais para Quantidade e Valor,
    # elas são ordenadas de forma descrescente pelo campo quantitativo
    # e é feita a soma desses campos agrupada pelo campo de data contendo os meses.''' 
    vlr_serieT_mes = mes_valor.set_index('YearMonth')['valuePix'].sort_values(ascending=False)
    vlr_serieT_mes = vlr_serieT_mes.groupby(vlr_serieT_mes.index).sum()

    qtd_serieT_mes = mes_quantidade.set_index('YearMonth')['quantityPix'].sort_values(ascending=False)
    qtd_serieT_mes = qtd_serieT_mes.groupby(qtd_serieT_mes.index).sum()

    # Remove anos duplicados das séries temporais anuais
    vlr_serieT_ano = pd.Series(data=ano_valor, index=data_ano, name='Ano').drop_duplicates()
    qtd_serieT_ano = pd.Series(data=ano_quantidade, index=data_ano, name='Ano').drop_duplicates()
    
    # As séries temporais finalizadas são salvas em arquivos .csv
    qtd_serieT_ano.to_csv('../TRAININGS/PROJETO_01_pix/files/func_02_Ano_QTD.csv')
    qtd_serieT_mes.to_csv('../TRAININGS/PROJETO_01_pix/files/func_02_Mes_QTD.csv')

    vlr_serieT_ano.to_csv('../TRAININGS/PROJETO_01_pix/files/func_02_Ano_VLR.csv')
    vlr_serieT_mes.to_csv('../TRAININGS/PROJETO_01_pix/files/func_02_Mes_VLR.csv')

    # Visualização da série temporal por Ano

    # Define o caminho onde a visualização será salva
    grafico_ano_caminho = '../TRAININGS/PROJETO_01_pix/img/ano_func_02_plot_QTD_VLR.png'

    '''Define duas variáveis (figura e gráfico) que recebem a função subplot()
    # com parâmetros para gerar uma visualização na escala 16:9 com dois gráficos.'''
    figura, grafico = plt.subplots(2, figsize=(16,9))
    figura.suptitle('Séries temporais de Quantidade e Valor de Pix por Ano')

    # Gráfico de quantidade (Milhões) de pix por Ano
    grafico[0].plot(qtd_serieT_ano) # Define a série temporal como fonte do gráfico
    grafico[0].set_title('Quantidade (Milhões) de Pix por Ano') # Define o título do gráfico
    grafico[0].xaxis.set_major_locator(MultipleLocator(1)) # Uso a função MultipleLocator do matplotlib para fazer o eixo X avançar de 1 em 1 ao invés de 2 em 2

    # Gráfico de valor (Bilhões) de pix por Ano
    grafico[1].plot(vlr_serieT_ano) # Define a série temporal como fonte do gráfico
    grafico[1].set_title('Valor (Bilhões) de Pix por Ano') # Define o título do gráfico
    grafico[1].xaxis.set_major_locator(MultipleLocator(1)) # Uso a função MultipleLocator do matplotlib para fazer o eixo X avançar de 1 em 1 ao invés de 2 em 2

    # Gráfico é salvo no caminho definido anteriormente
    plt.savefig(grafico_ano_caminho)

    # Visualização da série temporal por Mês

    # Define o caminho onde a visualização será salva
    grafico_mes_caminho = '../TRAININGS/PROJETO_01_pix/img/mes_func_02_plot_QTD_VLR.png'

    '''Define duas variáveis (figura e gráfico) que recebem a função subplot()
    # com parâmetros para gerar uma visualização na escala 20:9 com dois gráficos.'''
    figura, grafico = plt.subplots(2, figsize=(20,9))
    figura.suptitle('Séries temporais de Quantidade e Valor de Pix por Mês')

    # Gráfico de quantidade (Milhões) de pix por Mês
    grafico[0].plot(qtd_serieT_mes) # Define a série temporal como fonte do gráfico
    grafico[0].set_title('Quantidade de Pix por Mês') # Define o título do gráfico
    grafico[0].xaxis.set_major_locator(MultipleLocator(1)) # Uso a função MultipleLocator do matplotlib para fazer o eixo X avançar de 1 em 1 ao invés de 2 em 2

    # Gráfico de valor (Bilhões) de pix por Mês
    grafico[1].plot(vlr_serieT_mes) # Define a série temporal como fonte do gráfico
    grafico[1].set_title('Valor de Pix por Mês') # Define o título do gráfico
    grafico[1].xaxis.set_major_locator(MultipleLocator(1)) # Uso a função MultipleLocator do matplotlib para fazer o eixo X avançar de 1 em 1 ao invés de 2 em 2

    # Gráfico é salvo no caminho definido anteriormente
    plt.savefig(grafico_mes_caminho)

# Função que calcula percentual de quantidade do Pix e outros meios de pagamento entre 2020 e 2024
def fun_3_percentaul_pix_ano(dados, caminho):

    # Define variável com o caminho do arquivo .txt com os resultados
    arquivo_texto_resultados = caminho

    # Define variável contendo o recorte de ano das data presentes no Dataframe
    data_ano = pd.to_datetime(dados['YearMonth'].astype(str), format="%Y%m").dt.year

    '''Define as variáveis Dataframe para Pix, TED e Boleto. Elas contém
    # a soma das quantidade agrupada pelo recorte de ano do Dataframe base.'''
    pix_ano_quantidade = dados.groupby(pd.to_datetime(dados['YearMonth'].astype(str), format="%Y%m").dt.year)['quantityPix'].sum()
    ted_ano_quantidade = dados.groupby(pd.to_datetime(dados['YearMonth'].astype(str), format="%Y%m").dt.year)['quantityTED'].sum()
    boleto_ano_quantidade = dados.groupby(pd.to_datetime(dados['YearMonth'].astype(str), format="%Y%m").dt.year)['quantityBrazilianBoletoPayment'].sum()

    '''Define as séries temporais para Pix, TED e Boleto. Elas recebendo as
    # variáveis Dataframe, definindo os campos corretos para dados e indíce.
    # O indíce é ordenado de forma descrescente e por fim é usada a função drop_duplicates()'''
    pix_qtd_serieT_ano = pd.Series(data=pix_ano_quantidade, index=data_ano.sort_values(ascending=False), name='Ano').drop_duplicates()
    ted_qtd_serieT_ano = pd.Series(data=ted_ano_quantidade, index=data_ano.sort_values(ascending=False), name='Ano').drop_duplicates()
    boleto_qtd_serieT_ano = pd.Series(data=boleto_ano_quantidade, index=data_ano.sort_values(ascending=False), name='Ano').drop_duplicates()

    # Define variáveis contendo o cálculo do percentual de crescimento (ou decréscimo) do Pix, TED e Boleto.
    pix_percentual = round((100 * pix_qtd_serieT_ano[2024] / pix_qtd_serieT_ano[2020]) - 100, 2)
    ted_percentual = round((100 * ted_qtd_serieT_ano[2024] / ted_qtd_serieT_ano[2020]) - 100, 2)
    boleto_percentual = round((100 * boleto_qtd_serieT_ano[2024] / boleto_qtd_serieT_ano[2020]) - 100, 2)
    
    # Resultado é salvo no arquivo .txt
    with open(arquivo_texto_resultados, 'a', encoding='utf-8') as w:
        w.write(f'\n\n\nNum período de quatro anos (2020 até 2024), o pix aumentou suas ocorrências em: {pix_percentual}%\nEnquanto os meios de pagamento TED e Boleto, tiveram respectivamente, {ted_percentual}% e {boleto_percentual}%\n\nPIX: {pix_percentual}%\nTED: {ted_percentual}%\nBOLETO: {boleto_percentual}%\n\n\n')

    # Resultado exibido no terminal
    print(f'\nNum período de quatro anos (2020 até 2024), o pix aumentou suas ocorrências em: {pix_percentual}%\nEnquanto os meios de pagamento TED e Boleto, tiveram respectivamente, {ted_percentual}% e {boleto_percentual}%')
    
# Função que retorna os meses com pico nas quantidades de Pix
def fun_4_picos_datas(dados, caminho):

    # Define variável com o caminho do arquivo .txt com os resultados
    arquivo_texto_resultados = caminho

    # Converte o campo de quantidade do Dataframe base para um formato de melhor visualização
    dados['quantityPix'] = round(dados['quantityPix']/1_000_000)

    # Define uma variável que recebe de data e de quantidade de Pix do Dataframe base 
    pix_mes = dados[['YearMonth', 'quantityPix']]

    # Define uma série temporal com os valores da quantidade de Pix e indexada pela data
    series_pix_mes = pix_mes.set_index('YearMonth')['quantityPix'].sort_values(ascending=False)

    # Define o indíce da série temporal como um recorte do mês do indíce anterior
    series_pix_mes.index = series_pix_mes.index.astype(str).str[-2:].astype(int)  # fatia a data com str e pega os últimos 2 dígitos como int

    # Define uma variável com a soma das quantidades agrupada pelos meses
    total_por_mes = series_pix_mes.groupby(series_pix_mes.index).sum()

    # Ordena a variável pela quantidade, da maior para a menor
    total_por_mes = total_por_mes.sort_values(ascending=False)

    # Separa os 6 meses com mais quantidade dos 6 meses com menos quantidade, os armazenando em suas respectivas variáveis
    mais_qtd = total_por_mes.iloc[0:6]
    menos_qtd = total_por_mes.iloc[6:12]
    
    # Salva as séries temporais em arquivos .csv
    total_por_mes.to_csv('../TRAININGS/PROJETO_01_pix/files/fun_04_picos_sazonais_pix.csv')
    menos_qtd.to_csv('../TRAININGS/PROJETO_01_pix/files/fun_04_meses_menosQTD_pix.csv')
    mais_qtd.to_csv('../TRAININGS/PROJETO_01_pix/files/fun_04_meses_maisQTD_pix.csv')

    # Resultado é salvo no arquivo .txt
    with open(arquivo_texto_resultados, 'a', encoding='utf-8') as w:
        w.write(f'MESES COM MAIS QUANTIDADE DE PIX:\n\n')
        for ind, qtd in mais_qtd.items():
            if ind < 10:
                w.write(f'Mês 0{ind}: {qtd}\n')
            else:
                w.write(f'Mês {ind}: {qtd}\n')

    with open(arquivo_texto_resultados, 'a', encoding='utf-8') as w:
        w.write(f'\n\n\nMESES COM MENOS QUANTIDADE DE PIX:\n\n')
        for ind, qtd in menos_qtd.items():
            if ind < 10:
                w.write(f'Mês 0{ind}: {qtd}\n')
            else:
                w.write(f'Mês {ind}: {qtd}\n')

    # Resultado exibido no terminal
    print(f'Meses com mais quantidade de Pix:\n\n{mais_qtd.index}\n\n\n')
    print(f'Meses com menos quantidade de Pix:\n\n{menos_qtd.index}\n\n\n')



# Chamada das funções
fun_1_volume_pix_vs_outros(df)
fun_2_timeseries_pix(df)
fun_3_percentaul_pix_ano(df, resultadostxt)
fun_4_picos_datas(df, resultadostxt)


