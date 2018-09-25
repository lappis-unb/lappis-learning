import logging
from math import ceil
import os


from salicml.features.number_of_items import FeatureNumberOfItems
from salicml.metrics.number_of_items import NumberOfItemsModel
from salicml.middleware.exceptions import TraningNotFound
from salicml.middleware import constants


class NumberOfItemsMiddleware:
    '''This class is a middleware specialist in the metric NumberOfItems.
    It gets all necessary raw data from DataSource, extracts the feature
    NumberOfItems, and makes inference on that feature'''

    TRAIN_NUMBER_OF_METRICS_PATH = os.path.join(constants.TRAIN_FOLDER,
                                                'number_of_metrics.pickle')
    COLUMNS = ['PRONAC', 'idSegmento', 'idPlanilhaAprovacao', ]

    def __init__(self, data_source):
        self._data_source = data_source
        self.number_of_items = NumberOfItemsModel()

    def fill_json(self, metric_result):
        '''Add keys on the metric inference result json so the new json is
        ready to be consumed by a front-end'''

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
        '''Tries to load the training model for the feature'''
        self.number_of_items.load(
            NumberOfItemsMiddleware.TRAIN_NUMBER_OF_METRICS_PATH,
            self.on_load_number_of_items_error)

    def on_load_number_of_items_error(self):
        '''Callback function on the case of there is no trained stored to be
        loaded'''
        raise TraningNotFound('Number of Items training not found')

    def train_number_of_items(self, planilha_orcamentaria, save=True):
        '''Extracts the feature, trains a model on the extracted feature and
        returns the trained model. If save=True, the trained model will also
         be saved as a .picke file'''
        feature = FeatureNumberOfItems()

        items_features = feature.get_projects_number_of_items(
            planilha_orcamentaria)

        self.number_of_items.train(items_features)

        if save:
            self.number_of_items.save(
                NumberOfItemsMiddleware.TRAIN_NUMBER_OF_METRICS_PATH)

    def get_metric_number_of_items(self, pronac):
        '''Makes inference and calculate the metric number of items for the
        given pronac. The pronac's data will downloaded from the SALIC database
        so its guaranted to be up-to-date.'''
        feature = FeatureNumberOfItems()
        where = 'WHERE a.PRONAC = \'{0}\''.format(pronac)
        planilha_orcamentaria = self._data_source.get_planilha_orcamentaria(
            columns=NumberOfItemsMiddleware.COLUMNS, where=where)
        items_features = feature.get_projects_number_of_items(
            planilha_orcamentaria)

        _, id_segment, number_of_items = items_features[0]

        result = self.number_of_items.is_outlier(number_of_items, id_segment)
        result['number_of_items'] = number_of_items
        return result


def str_int(n):
    return str(int(n))
