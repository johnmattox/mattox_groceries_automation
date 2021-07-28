import pygsheets
import pandas as pd
import datetime
import json
import random
import numpy as np
from IPython.core import display as ICD
from IPython.display import clear_output
pd.set_option('display.max_rows', 100)

gc=pygsheets.authorize(service_file='camelotspreadsheets-5fdda9ce433a.json')

spreadsheet_name = "base_dishes"
sh = gc.open(spreadsheet_name)

def df_to_sheet(df,header=True):
    df_columns = [np.array(df.columns)]
    df_values = df.values.tolist()
    df_to_sheet = np.concatenate((df_columns, df_values)).tolist()
    if header: return df_to_sheet
    else: return df_values
    
sh = gc.open(spreadsheet_name)
wks = sh.worksheet('title','template_add_receita')
# Pega dados de cadastro da receita
dados_basicos = pd.DataFrame(wks.get_values("A1","B11")).T
dados_basicos.columns = dados_basicos.iloc[0]
dados_basicos=dados_basicos.iloc[1:].reset_index(drop=True)
# Pega receita propriamente dita
receita = pd.DataFrame(wks.get_values("A13","C100"))
receita.columns = receita.iloc[0]
receita=receita.iloc[1:].reset_index(drop=True)
# Monta string dos ingredientes
rcp_str="{"
for i in list(receita.index):
    rcp_str+=("'%s':'%s&%s',"%(receita.loc[i,'ingredientes'],
                               receita.loc[i,'Qtd'],
                               receita.loc[i,'Unid']
                              ))
rcp_str=rcp_str[:-1]+'}'
# Monta df com receita atual
df_recipe_now = pd.DataFrame({'nome':dados_basicos['nome'][0],
                              'tipos':dados_basicos['tipos'][0],
                              'porcoes':dados_basicos['porcoes'][0],
                              'durab_ingredientes':dados_basicos['durab_ingredientes'][0],
                              'durab_alimento':dados_basicos['durab_alimento'][0],
                              'congelavel':dados_basicos['congelavel'][0],
                              'complexidade':dados_basicos['complexidade'][0],
                              'clima':dados_basicos['clima'][0],
                              'ingredientes':rcp_str,
                              'link_receita':dados_basicos['link_receita'][0],
                              'dica':dados_basicos['dica'][0]
                             },index=[0])
# Carrega lista completa de receitas
wks_allrecipess = sh.worksheet('title',dados_basicos['aba'][0])
df_allrecipes = wks_allrecipess.get_as_df()

def atualiza_receitas(dados_basicos,df_allrecipes,wks_allrecipess):
    # Checa se é uma receita repetida
    if dados_basicos['nome'][0] in list(df_allrecipes['nome']):
        # Ve se usuario quer substituí-la
        resp = input("Essa receita já existe. Substituí-la (S/N)? ")
        while resp.lower() not in ["s","n"]:
            clear_output()
            resp = input("Essa receita já existe. Substituí-la (S/N)? ")
        if resp=='S':
            df_allrecipes=df_allrecipes.loc[df_allrecipes['nome']!=dados_basicos['nome'][0]]
            df_allrecipes=df_allrecipes.append(df_recipe_now)
        else:
            print("Interrompendo atualização")
            return 0
    else: df_allrecipes=df_allrecipes.append(df_recipe_now)
    # Salva lista de receitas
    df_allrecipes=df_allrecipes.sort_values(by='nome')
    wks_allrecipess.clear()
    wks_allrecipess.update_values("A1",df_to_sheet(df_allrecipes))
	print("Receitas atualizadas com sucesso!")
    
atualiza_receitas(dados_basicos,df_allrecipes,wks_allrecipess)