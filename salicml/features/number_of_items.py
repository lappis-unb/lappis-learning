import pyodbc
import os
from salicml.data.data_source import DataSource


class FeatureNumberOfItems:


    def __init__(self):
        pass

    def get_number_of_items(self, pronac = ""):
        query = (
            "SELECT DISTINCT CONCAT(p.AnoProjeto, p.Sequencial) as PRONAC, \
             p.Segmento as idSegmento, \
             COUNT(a.Item) OVER (PARTITION BY a.idPronac) as number_of_items \
             FROM SAC.dbo.Projetos as p \
             LEFT JOIN SAC.dbo.vwPlanilhaAprovada a \
             ON p.IdPRONAC = a.idPronac"
        )

        if pronac:
            query += " WHERE a.PRONAC = '{0}'".format(pronac)
            return self.execute_query(query)[0]

        else:
            return self.execute_query(query)

