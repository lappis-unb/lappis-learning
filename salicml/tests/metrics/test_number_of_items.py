import unittest

from salicml.metrics.number_of_items import NumberOfItems


class TestNumberOfItems(unittest.TestCase):


    def test_train(self):
        items_features = [['000001', 'A', 1], ['000002', 'A', 11],
                          ['000003', 'B', 2], ['000004', 'B', 20],
                          ['000005', 'C', 3],]

        number_of_items = NumberOfItems()
        number_of_items.train(items_features)

        self.assertEqual(3, len(number_of_items.segments_trained))

        self.assertEqual(6, number_of_items.segments_trained['A']['mean'])
        self.assertEqual(11, number_of_items.segments_trained['B']['mean'])
        self.assertEqual(3, number_of_items.segments_trained['C']['mean'])

        self.assertEqual(5, number_of_items.segments_trained['A']['std'])
        self.assertEqual(9, number_of_items.segments_trained['B']['std'])
        self.assertEqual(0, number_of_items.segments_trained['C']['std'])
