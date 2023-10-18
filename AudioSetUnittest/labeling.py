import unittest
import AudioSet.labeling as labeling
import numpy as np


class MyTestCase(unittest.TestCase):

    def test_label_digits2one_zero_tensor(self):
        label = labeling.label_digits2one_zero_tensor([1, 2, 3], 5)
        self.assertTrue(np.all(label == np.array([0, 1, 1, 1, 0])))


if __name__ == '__main__':
    unittest.main()
