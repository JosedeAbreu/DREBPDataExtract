import pandas as pd
from datetime import date

class DREBPDataExtract:
    def __init__(self, df, time_start, time_end):
        """
        Classe para encontrar os últimos valores em um DataFrame com base nas contas indicadas.
        """
        self.time_start = time_start
        self.time_end = time_end
        self.df = df
        

    def get_hierarchy(self, hierarchy_level):
        #Encontrar a coluna com os valores numéricos das contas
        indice_coluna = 0
        for nivel1 in range(0,3):
            for nivel2 in range(1,3):
                valor_busca= str(nivel1) +"."+ str(nivel2)
                indice_coluna, _ = self.find_value_position(valor_busca)
                if indice_coluna is not None:
                    break

        conta_value = self.df.iloc[:, indice_coluna].tolist()

        hierarchy_contas = []
        for valor in conta_value:
            # Verifica se é string e não está vazio
            if isinstance(valor, str) and valor.strip():
                partes = valor.split('.')
                # Filtra pela hierarquia desejada
                if 0 < len(partes)-1 <= hierarchy_level:
                    hierarchy_contas.append(valor)    
        return hierarchy_contas
        
    def find_value_position(self, valor_busca):
        mascara = self.df.eq(valor_busca)
        if mascara.any().any():
            linha, coluna = mascara.stack().idxmax()
            indice_coluna = self.df.columns.get_loc(coluna)
            indice_linha = self.df.index.get_loc(linha)
            return indice_coluna, indice_linha
        return None, None
    
    def _find_rows(self):
        for idx, row in self.position_reference.iterrows():
            _, indice_linha = self.find_value_position(idx)
            self.position_reference.at[idx, 'Linha'] = indice_linha

    def _find_columns(self):
        datas = pd.date_range(start=self.time_start, end=self.time_end, freq='D')
        df_datas = pd.DataFrame(datas, columns=['Data'])
        for _, value in df_datas.iterrows():
            buscar = value.iloc[0]
            exist, _ = self.find_value_position(buscar)
            count_column = 0
            if exist != None:
                count_column += 1
                self.position_reference[buscar] = exist

    def get_values(self, contas_busca):
        self.position_reference = pd.DataFrame(index=contas_busca, columns=['Linha'])
        self._find_rows()
        self._find_columns()

        result = pd.DataFrame(columns=['Data','Conta','Valor'])
        for _, row in self.position_reference.iterrows():
            for data in self.position_reference.columns.difference(['Linha']):
                
                linha = row['Linha']
                coluna = row[data]
                
                if pd.notna(linha) and pd.notna(coluna):
                    valor = self.df.iloc[int(linha), int(coluna)]

                    if pd.notna(valor): 
                        novo_dado = pd.DataFrame({
                        'Data': [data],
                        'Conta': [_],
                        'Valor': [valor]
                        })

                        result = pd.concat([result, novo_dado],ignore_index=True)
                else:
                    valor = None
                
        return result
