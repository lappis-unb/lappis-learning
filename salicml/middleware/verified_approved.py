import os

from salicml.middleware.exceptions import TraningNotFound
from salicml.middleware import constants
from salicml.metrics.verified_approved import VerifiedApprovedModel
from salicml.data_source.data_source_db import VerifiedApprovedDataSource
from salicml.features.verified_approved import VerifiedApprovedFeature


TRAIN_FILE_NAME = 'verified_approved.pickle'
TRAIN_NUMBER_OF_METRICS_PATH = os.path.join(constants.TRAIN_FOLDER,
                            TRAIN_FILE_NAME)
ITEM_NAME_COLUMN = 'Item'


class VerifiedApprovedMiddleware:
    '''This class is a middleware specialist in the metric NumberOfItems.
    It gets all necessary raw data from DataSource, extracts the feature
    NumberOfItems, and makes inference on that feature'''

    def __init__(self):
        self._data_source = VerifiedApprovedDataSource()
        self.verified_approved_model = VerifiedApprovedModel()

    def train_number_of_items(self, planilha_orcamentaria, save=True):
        '''Extracts the feature, trains a model on the extracted feature and
        returns the trained model. If save=True, the trained model will also
         be saved as a .picke file'''
        feature = VerifiedApprovedFeature()

    def get_metric_verified_approved(self, pronac):
        '''Makes inference and calculate the metric number of items for the
        given pronac. The pronac's data will downloaded from the SALIC database
        so its guaranted to be up-to-date.'''
        feature = VerifiedApprovedFeature()

        planilha_aprovacao_comprovacao_pronac = \
            self._data_source.download_dataset(pronac=pronac)
        pronac_features = \
            feature.get_features(planilha_aprovacao_comprovacao_pronac)

        features_size = pronac_features.shape[0]
        outlier_items = list(pronac_features[ITEM_NAME_COLUMN])
        result = {
            'number_of_outliers': features_size,
            'outlier_items': outlier_items,
        }
        return result
