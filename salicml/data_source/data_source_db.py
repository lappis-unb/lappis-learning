import pandas as pd

import os

from salicml.data_source.data_source_abc import DataSourceABC
from salicml.data_source.db_connector import DbConnector
from salicml.middleware import constants
from salicml.utils import storage
from salicml.utils.utils import debug


class DataSourceDb(DataSourceABC):
    PATH = os.path.join(constants.TRAIN_FOLDER, 'planilha_orcamentaria.pickle')

    def __init__(self):
        self.db_connector = DbConnector()

    def _read_cache(self):
        spreadsheet = storage.load(
            DataSourceDb.PATH,
            on_error_callback=self.no_cache_callback)
        return spreadsheet

    def no_cache_callback(self):
        raise FileNotFoundError('No file {}'.format(DataSourceDb.PATH))

    def download_planilha_orcamentaria(self, columns=None, pronac=''):
        ''''Returns [[PRONAC, id_planilha_aprovacao, id_segmento]]'''
        DB_COLUMN = \
            {'PRONAC': 'a.PRONAC',
             'idSegmento': 'p.Segmento AS idSegmento',
             'idPlanilhaAprovacao': 'a.idPlanilhaAprovacao', }

        if columns is None:
            columns = DB_COLUMN.keys()

        column_order = ['PRONAC', 'idPlanilhaAprovacao', 'idSegmento']

        select = 'SELECT '
        select += ','.join([DB_COLUMN[key]
                            for key in column_order if key in columns])
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

        debug('Downloading query:\n{}\n'.format(sql_query))
        spreadsheet = self.db_connector.execute_query(sql_query)
        debug('Download finished')
        return spreadsheet

    def get_planilha_orcamentaria(
            self,
            columns=None,
            pronac='',
            use_cache=False):
        download = True

        if use_cache and not pronac:
            try:
                spreadsheet = self._read_cache()
                download = False
                debug('Cache was read')
            except FileNotFoundError:
                debug('Cache was not found on {}'.format(DataSourceDb.PATH))

        if download:
            debug('Downloading planilha')
            spreadsheet = self.download_planilha_orcamentaria(
                columns=columns, pronac=pronac)
            storage.save(DataSourceDb.PATH, spreadsheet)

        return spreadsheet


class DataSourceMock(DataSourceABC):
    def __init__(self, planilha_orcamentaria=None):
        self._planilha_orcamentaria = pd.DataFrame(planilha_orcamentaria)

    def get_planilha_orcamentaria(
            self,
            columns=None,
            pronac='',
            use_cache=False):
        df = self._planilha_orcamentaria
        spreadsheet = None
        if pronac:
            spreadsheet = df[df[0] == pronac]
        else:
            spreadsheet = df
        spreadsheet = spreadsheet.values.tolist()
        return spreadsheet
