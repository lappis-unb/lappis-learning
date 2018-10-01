import pandas as pd

from salicml.data_source.data_source_abc import DataSourceABC
from salicml.data_source.db_connector import DbConnector


class DataSourceDb(DataSourceABC):

    def __init__(self):
        self.db_connector = DbConnector()

    def get_planilha_orcamentaria(self, columns, pronac=''):
        DB_COLUMN = \
            {'PRONAC': 'a.PRONAC',
             'idPlanilhaAprovacao': 'a.idPlanilhaAprovacao',
             'idSegmento': 'p.Segmento AS idSegmento', }

        select = 'SELECT '
        select += ','.join([DB_COLUMN[key] for key in columns])
        select += '\n'
        from_db = 'FROM SAC.dbo.vwPlanilhaAprovada a\n' \
                  'LEFT JOIN SAC.dbo.Projetos p\n' \
                  'ON a.idPronac = p.IdPRONAC\n' \
                  'INNER JOIN SAC.dbo.tbPlanilhaItens i\n' \
                  'ON Item = i.Descricao\n' \
                  'INNER JOIN SAC.dbo.Segmento s\n' \
                  'ON P.Segmento = s.Codigo\n' \
                  'INNER JOIN SAC.dbo.Area area\n' \
                  'ON p.Area = area.Codigo'

        sql_query = select + from_db
        if pronac:
            where = '\n' + 'WHERE a.PRONAC = \'{0}\''.format(pronac)
            sql_query += where
        sql_query += ';'
        spreadsheet = self.db_connector.execute_query(sql_query)
        return spreadsheet


class DataSourceMock(DataSourceABC):
    def __init__(self, planilha_orcamentaria=None):
        self._planilha_orcamentaria = pd.DataFrame(planilha_orcamentaria)

    def get_planilha_orcamentaria(self, columns, pronac=''):
        df = self._planilha_orcamentaria
        print('df = {}'.format(df))
        spreadsheet = None
        if pronac:
            spreadsheet = df[df[0] == pronac]
        else:
            spreadsheet = df
        spreadsheet = spreadsheet.values.tolist()
        print('pronac = {}'.format(pronac))
        print('spreadsheet = {}'.format(spreadsheet))
        return spreadsheet
