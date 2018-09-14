import pyodbc
import os
from salicml.data.data_source import DataSource


class FeatureNumberOfItems:


    def __init__(self):
        self.data_source = DataSource()


    def get_number_of_items(self, pronac = ""):
        return self.data_source.get_pronac_segmento_number_of_items(pronac)

