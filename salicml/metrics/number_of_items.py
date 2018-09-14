import pandas as pd
import numpy as np

from salicml.models import gaussian_outlier


class NumberOfItemsModel:
    '''Trains a model and makes inferences on that model about the nubmer of
    items from SALIC projects'''

    MEAN_KEY = 'mean'
    STD_KEY = 'std'


    def __init__(self):
        self.segments_trained = None


    def train(self, items_features):
        '''Receives features of SALIC projects in a matrix form. The matrix must be
        a python list of python lists, where each inner list represents a row in
        the matrix.

        Matrix format:
        The order of the elements of the inner list must be:
        pronac (str), id_segmento (str), number_of_items (int)

        Example:

        [['012345', '1A', 123],
         ['012346', '2B', 124],
         ['012347', 'A8', 123],
         ['012348', '2A', 123],
         ['012349', '2A', 123], ]
        '''

        COLUMNS = ['PRONAC', 'id_segmento', 'number_of_items']
        items_df = pd.DataFrame(items_features, columns=COLUMNS)

        self.segments_trained = dict()

        segments_groups = items_df.groupby(['id_segmento'])
        for segment, segment_group in segments_groups:
            number_of_items_array = segment_group.number_of_items.values
            segment_trained = self._train_segment(number_of_items_array)

            self.segments_trained[segment] = segment_trained


    def make_inference(self, number_of_items, id_segment):
        segment_mean = \
            self.segments_trained[id_segment][NumberOfItemsModel.MEAN_KEY]
        segment_std = \
            self.segments_trained[id_segment][NumberOfItemsModel.STD_KEY]

        outlier = gaussian_outlier.is_outlier(number_of_items, segment_mean,
                                              segment_std)

        maximum_expected = \
            gaussian_outlier.maximum_expected_value(segment_mean, segment_std)

        result = {
            'is_outlier': outlier,
            'maximum_expetected':maximum_expected,
        }
        return result


    def _train_segment(self, segment_features):
        '''Sets the mean and standard deviation from an array of features
        (number_of_items) and returns it as a dictionary'''

        mean = np.mean(segment_features)
        std = np.std(segment_features)

        result = {NumberOfItemsModel.MEAN_KEY: mean,
                  NumberOfItemsModel.STD_KEY: std}
        return result
