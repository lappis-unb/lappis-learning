import pandas as pd


class NumberOfItems:
    '''Trains a makes inferences about the nubmer of items from SALIC projects
    '''

    def __init__(self):
        pass

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
        print(items_df)

        items_df.groupby(['id_segmento'], )

    def infer(self, pronac, segment_id):
        pass
