from abc import ABC, abstractmethod


class DataSourceABC(ABC):
    '''This class defines the interface that is responsable for getting raw
    data about SALIC projects from different sources.'''

    @abstractmethod
    def get_planilha_orcamentaria(
            self,
            pronac='',
            columns=None,
            use_cache=False):
        '''Returns the budgetary spreadsheet about SALIC projects. The output
        is a matrix, represented as a python list of python lists.

        Input example:
            (('PRONAC', 'idSegmento', 'idPlanilhaAprovacao'), '123456')

        Output example:
            [['123456', '2A', 123],
             ['123456', '2A', 124],
             ['123457', 'AA', 323],
             ['123458', 'XY', 923], ]
        '''
        pass
