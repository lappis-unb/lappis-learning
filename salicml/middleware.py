import os

from salicml.features.number_of_items import FeatureNumberOfItems
from salicml.metrics.number_of_items import NumberOfItemsModel
from salicml.data.data_source import DataSource


class Middleware:
    FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    TRAIN_FOLDER = os.path.join(FILE_PATH, 'trainings')
    TRAIN_NUMBER_OF_METRICS_PATH = os.path.join(TRAIN_FOLDER,
                                                'number_of_metrics.pickle')
    COLUMNS = ['PRONAC', 'idSegmento', 'idPlanilhaAprovacao', ]

    def __init__(self):
        self._init_data_source()
        self.number_of_items = NumberOfItemsModel()

    def _init_data_source(self):
        self._data_source = DataSource()

    def train_all(self, save=True):
        self.train_number_of_items(save)

    def load_all(self):
        self.load_number_of_items()

    def load_number_of_items(self):
        self.number_of_items.load(Middleware.TRAIN_NUMBER_OF_METRICS_PATH,
                                  self.on_load_number_of_items_error)

    def on_load_number_of_items_error(self):
        self.train_number_of_items()

    def train_number_of_items(self, save=True):
        feature = FeatureNumberOfItems()

        planilha_orcamentaria = self._data_source.get_planilha_orcamentaria(
            columns=Middleware.COLUMNS)

        items_features = feature.get_projects_number_of_items(
            planilha_orcamentaria)

        self.number_of_items.train(items_features)

        if save:
            self.number_of_items.save(Middleware.TRAIN_NUMBER_OF_METRICS_PATH)

    def get_metric_number_of_items(self, pronac):
        feature = FeatureNumberOfItems()
        where = 'WHERE a.PRONAC = \'{0}\''.format(pronac)
        planilha_orcamentaria = self._data_source.get_planilha_orcamentaria(
            columns=Middleware.COLUMNS, where=where)
        items_features = feature.get_projects_number_of_items(
            planilha_orcamentaria)

        _, id_segment, number_of_items = items_features[0]

        result = self.number_of_items.is_outlier(number_of_items, id_segment)

        return result
