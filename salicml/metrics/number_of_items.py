import pandas as pd
import numpy as np


class NumberOfItems:
    '''Trains a makes inferences about the nubmer of items from SALIC projects
    '''

    MEAN_KEY = 'mean'
    STD_KEY = 'std'


    def __init__(self):
        self.segments_trained = None


    def train(self, items_features):
        '''Receives features of SALIC projects in a matrix form. The matrix must be
        a python list of python lists, where each inner list represents a row in
        the matrix. The first row must be names of the columns.

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


    def make_inference(self, pronac, id_segment):
        pass


    def _train_segment(self, segment_features):
        '''Sets the mean and standard deviation from an array of features
        (number_of_items) and returns it as a dictionary'''

        mean = np.mean(segment_features)
        std = np.std(segment_features)

        result = {NumberOfItems.MEAN_KEY: mean,
                  NumberOfItems.STD_KEY: std}
        return result
