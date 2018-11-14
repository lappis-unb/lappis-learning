import pandas as pd
import sys

from flask import current_app as app


COLUMNS = ['PRONAC', 'idPlanilhaAprovacao', 'Item', 'idSegmento', 'vlAprovado',
           'vlComprovacao']
VERIFIED_COLUMN = 'vlComprovacao'
APPROVED_COLUMN = 'vlAprovado'

def log(message):
    with app.app_context():
        app.logger.info(message)

class VerifiedApprovedFeature:

    def __init__(self):
        pass

    def get_features(self, items_dataset):
        '''Receives budgetary items of SALIC projects in a matrix form as input
        The matrix must be a python list of python lists, where each inner list
        represents a row in the matrix. For each distinct pronac on the input,
        there will be exactly one row in the output matrix, containing the
        feature.

        Input format:
        The order of the elements of the inner list must be:
        pronac (str), id_segmento (str), id_planilha_aprovacao (int)

        Input example:

        [['012345', 123, 'A1'],
         ['012345', 124, 'A1'],
         ['012345', 125, 'A1'],
         ['012348', 126, 'A2'],
         ['012348', 127, 'A2'],
         ['012350', 128, 'A3'], ]


        Output example:

        [['012345', '2A', 3],
         ['012348', '3A', 2],
         ['012350', '4D', 1],
         ]
        '''

        items_df = pd.DataFrame(items_dataset)
        items_df.columns = items_df.iloc[0].values
        items_df = items_df[1:]
        items_df = items_df[COLUMNS]
        items_df[[APPROVED_COLUMN, VERIFIED_COLUMN]] = \
            items_df[[APPROVED_COLUMN, VERIFIED_COLUMN]].astype(float)

        THRESHOLD = 1.5
        bigger_than_approved = items_df[VERIFIED_COLUMN] > \
                               (items_df[APPROVED_COLUMN] * THRESHOLD)
        features = items_df[bigger_than_approved]
        return features

    def get_pronac_features(self, items):
        '''Receives budgetary items of a SALIC project in a matrix form as input
        The matrix must be a python list of python lists, where each inner list
        represents a row in the matrix. An exception will be raise if there's
        more than one distinct pronac in the input. The behavior is undefined
        if the same pronac has more than one segment.

        Input format:
        The order of the elements of the inner list must be:
        pronac (str), id_segmento (str), id_planilha_aprovacao (int)

        Input example:

        [['012345', '2A', 123],
         ['012345', '2A', 124],
         ['012345', '2A', 125],
        ]

        Output example:

        ['012345', '2A', 3]
        '''

        res = self.get_projects_number_of_items(items)
        if len(res) == 1:
            return res[0]
        else:
            raise ValueError('More than one distinct pronac were given.')
