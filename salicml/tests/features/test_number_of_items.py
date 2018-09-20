import unittest

from salicml.features.number_of_items import FeatureNumberOfItems


class TestFeatureNumberOfItems(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.projects_items = [['012345', '2A', 123],
                              ['012345', '2A', 124],
                              ['012345', '2A', 125],
                              ['012348', '3A', 126],
                              ['012348', '3A', 127], ]

        cls.pronac_items = [['012345', '2A', 123],
                            ['012345', '2A', 124],
                            ['012345', '2A', 125], ]


    def test_get_one_pronac_number_of_items(self):
        feature = FeatureNumberOfItems()
        number_of_items = feature.get_pronac_number_of_items(self.pronac_items)
        self.assertEqual(len(number_of_items), 3)
        self.assertEqual(number_of_items[2], 3)

    def test_get_pronacs_number_of_items(self):
        feature = FeatureNumberOfItems()
        pronacs_features = \
            feature.get_projects_number_of_items(self.projects_items)

        self.assertEqual(len(pronacs_features), 2)

        expected_result = [['012345', '2A', 3], ['012348', '3A', 2], ]
        self.assertEquals(pronacs_features, expected_result)
