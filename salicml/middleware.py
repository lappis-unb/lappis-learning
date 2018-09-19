from salicml.metrics.number_of_items import NumberOfItemsModel
from salicml.features.number_of_items import FeatureNumberOfItems


class Middleware:

    def __init__(self):
        self.number_of_items = NumberOfItemsModel()


    def train_all(self):
        self.train_number_of_items()


    def train_number_of_items(self):
        feature = FeatureNumberOfItems()
        items_features = feature.get_number_of_items()

        self.number_of_items.train(items_features)


    def get_metric_number_of_items(self, pronac):
        feature = FeatureNumberOfItems()
        _, id_segment, number_of_items = feature.get_number_of_items(pronac)

        result = self.number_of_items.is_outlier(number_of_items, id_segment)

        return result
