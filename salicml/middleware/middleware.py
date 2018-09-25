import logging
import os

from salicml.data.data_source import DataSource
from salicml.middleware.number_of_items import NumberOfItemsMiddleware
from salicml.middleware.exceptions import TraningNotFound
from salicml.middleware import constants
from salicml.utils import storage


log = logging.getLogger('flask.app.middleware').debug


class Middleware:
    '''This class is responsable for getting raw data from DataSource, calling
    feature extraction processes on that raw data and training or making
    inferences on the extracted features. The training or inference processes
    are expected to be used on an external service, e.g Flask or Django web
    servers or CLI.'''

    def __init__(self):
        self._init_data_source()
        self._init_number_of_items_middleware()
        log('Initing Middleware\n')

    def _init_data_source(self):
        self._data_source = DataSource()

    def train_all(self, save=True):
        '''Trains the models for all implemented feature-middlewares. It will
        try to load the stored training models. If there's no training stored,
        it will train the model and store it if save=True. '''
        planilha_orcamentaria = self._get_planilha_orcamentaria()

        self.number_of_items_middleware.train_number_of_items(
            planilha_orcamentaria, save)

    def load_all(self):
        '''Tries to load the training model from disk. If the training model is
        not foundon disk, it will be trained and saved.'''
        try:
            self.number_of_items_middleware.load_number_of_items()
        except TraningNotFound:
            planilha_orcamentaria = self._get_planilha_orcamentaria()
            self.number_of_items_middleware.train_number_of_items(
                planilha_orcamentaria, True)

    def _init_number_of_items_middleware(self):
        self.number_of_items_middleware = NumberOfItemsMiddleware(
            self._data_source)

    def get_metric_number_of_items(self, pronac):
        return self.number_of_items_middleware.get_metric_number_of_items(
            pronac)

    def _get_planilha_orcamentaria(self, use_cache=True):
        '''Singleton implementation of planilha orcamentaria. '''
        name = 'planilha_orcamentaria'
        PLANILHA_ORCAMENTARIA = \
            os.path.join(constants.TRAIN_FOLDER, name + '.pickle')

        download = True
        use_attr = False
        use_file = False

        if use_cache:
            use_attr = hasattr(self, name)
            if not use_attr:
                use_file = os.path.exists(PLANILHA_ORCAMENTARIA)

            if use_attr or use_file:
                download = False

        planilha_orcamentaria = None

        if download:
            log('Downloading {}.'.format(name))
            planilha_orcamentaria = self._data_source. \
                get_planilha_orcamentaria(
                    columns=NumberOfItemsMiddleware.COLUMNS)

            storage.save(PLANILHA_ORCAMENTARIA, planilha_orcamentaria)
        elif use_attr:
            log('Loading {} from attr.'.format(name))
            planilha_orcamentaria = self.planilha_orcamentaria
        elif use_file:
            log('Loading {} from pickle.'.format(name))
            planilha_orcamentaria = storage.load(PLANILHA_ORCAMENTARIA)

        self.planilha_orcamentaria = planilha_orcamentaria
        return planilha_orcamentaria
