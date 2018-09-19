import os

from salicml.metrics.number_of_items import NumberOfItemsModel
from salicml.features.number_of_items import FeatureNumberOfItems


class Middleware:

    FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    TRAIN_FOLDER = os.path.join(FILE_PATH, 'trainings')
    TRAIN_NUMBER_OF_METRICS_PATH = os.path.join(TRAIN_FOLDER,
                                                'number_of_metrics.pickle')


    def __init__(self):
        self.number_of_items = NumberOfItemsModel()


    def train_all(self, save=True):
        self.train_number_of_items(save)


    def load_all(self):
        self.load_number_of_items()


    def load_number_of_items(self):
        self.number_of_items.load(Middleware.TRAIN_NUMBER_OF_METRICS_PATH)


    def train_number_of_items(self, save=True):
        feature = FeatureNumberOfItems()
        items_features = feature.get_number_of_items()

        self.number_of_items.train(items_features)

        if save:
            self.number_of_items.save(Middleware.TRAIN_NUMBER_OF_METRICS_PATH)


    def get_metric_number_of_items(self, pronac):
        feature = FeatureNumberOfItems()
        _, id_segment, number_of_items = feature.get_number_of_items(pronac)

        result = self.number_of_items.is_outlier(number_of_items, id_segment)

        return result
