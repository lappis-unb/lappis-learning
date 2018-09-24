import os

from salicml.features.number_of_items import FeatureNumberOfItems
from salicml.metrics.number_of_items import NumberOfItemsModel
from salicml.data.data_source import DataSource
from salicml.middleware.number_of_items import NumberOfItemsMiddleware


class Middleware:
    FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    TRAIN_FOLDER = os.path.join(FILE_PATH, 'trainings')
    TRAIN_NUMBER_OF_METRICS_PATH = os.path.join(TRAIN_FOLDER,
                                                'number_of_metrics.pickle')
    COLUMNS = ['PRONAC', 'idSegmento', 'idPlanilhaAprovacao', ]

    def __init__(self):
        self._init_data_source()
        self._init_number_of_items_middleware()


    def _init_data_source(self):
        self._data_source = DataSource()

    def train_all(self, save=True):
        planilha_orcamentaria = self._data_source.get_planilha_orcamentaria(columns=NumberOfItemsMiddleware.COLUMNS)
        self.number_of_items_middleware.train_number_of_items(planilha_orcamentaria, save)

    def load_all(self):
        self.number_of_items_middleware.load_number_of_items()

    def _init_number_of_items_middleware(self):
        self.number_of_items_middleware = NumberOfItemsMiddleware(self._data_source)

    def get_metric_number_of_items(self, pronac):
        return self.number_of_items_middleware.get_metric_number_of_items(pronac)
