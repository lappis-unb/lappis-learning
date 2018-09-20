import unittest

from salicml.features.number_of_items import FeatureNumberOfItems


class TestFeatureNumberOfItems(unittest.TestCase):


    def test_get_one_pronac_number_of_items(self):
        pronac = '164274'
        feature = FeatureNumberOfItems()
        number_of_items = feature.get_number_of_items(pronac)


        self.assertEqual(3, len(number_of_items))
        self.assertEqual(pronac, number_of_items[0])

