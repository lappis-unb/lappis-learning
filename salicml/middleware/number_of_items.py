import os

from salicml.features.number_of_items import FeatureNumberOfItems
from salicml.metrics.number_of_items import NumberOfItemsModel
from salicml.middleware.exceptions import TraningNotFound

from math import ceil


def str_int(n):
    return str(int(n))


class NumberOfItemsMiddleware:

    FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    TRAIN_FOLDER = os.path.join(FILE_PATH, 'trainings')
    TRAIN_NUMBER_OF_METRICS_PATH = os.path.join(TRAIN_FOLDER,
                                                'number_of_metrics.pickle')
    COLUMNS = ['PRONAC', 'idSegmento', 'idPlanilhaAprovacao', ]

    def __init__(self, data_source):
        self._data_source = data_source
        self.number_of_items = NumberOfItemsModel()

    def fill_json(self, metric_result):

        METRIC_GOOD = 'Metric-good'
        METRIC_BAD = 'Metric-bad'

        number_of_items = metric_result['number_of_items']
        max_expected = metric_result[NumberOfItemsModel.MAX_EXPECTED_KEY]

        json = dict()
        json["name"] = 'itens_orcamentarios'
        json["name_title"] = 'Itens orçamentários'
        json["helper_text"] = 'Compara a quantidade de itens deste projeto ' \
                              'com a quantidade mais comum de itens em ' \
                              'projetos do mesmo segmento'
        json["value"] = number_of_items
        json["value_is_valid"] = "True"
        json["outlier_check"] = METRIC_GOOD if metric_result['is_outlier'] \
            else METRIC_BAD
        json["type"] = "bar"
        json["bar"] = {
            "interval_start": 0,
            "interval_end": int(ceil(max_expected)),
            "interval": int(number_of_items),
            "max_value": int(2.0 * ceil(max(max_expected, number_of_items))),
        }
        json["reason"] = ''
        return json

    def load_number_of_items(self):
        self.number_of_items.load(
            NumberOfItemsMiddleware.TRAIN_NUMBER_OF_METRICS_PATH,
            self.on_load_number_of_items_error)

    def on_load_number_of_items_error(self):
        raise TraningNotFound('Number of Items training not found')

    def train_number_of_items(self, planilha_orcamentaria, save=True):
        feature = FeatureNumberOfItems()

        items_features = feature.get_projects_number_of_items(
            planilha_orcamentaria)

        self.number_of_items.train(items_features)

        if save:
            self.number_of_items.save(
                NumberOfItemsMiddleware.TRAIN_NUMBER_OF_METRICS_PATH)

    def get_metric_number_of_items(self, pronac):
        feature = FeatureNumberOfItems()
        where = 'WHERE a.PRONAC = \'{0}\''.format(pronac)
        planilha_orcamentaria = self._data_source.get_planilha_orcamentaria(
            columns=NumberOfItemsMiddleware.COLUMNS, where=where)
        items_features = feature.get_projects_number_of_items(
            planilha_orcamentaria)

        _, id_segment, number_of_items = items_features[0]

        result = self.number_of_items.is_outlier(number_of_items, id_segment)
        result['number_of_items'] = number_of_items
        result_json = self.fill_json(result)
        return result_json
