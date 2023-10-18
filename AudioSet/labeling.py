import numpy as np
from typing import Iterable

label_digits_t = Iterable[int]


def label_digits2one_zero_tensor(label_digits: label_digits_t,
                                 n_classes: int,
                                 d_type=np.int32) -> np.ndarray:
    ret = np.zeros(n_classes, dtype=d_type)
    label_digits = np.array([i for i in label_digits])
    ret[label_digits] = 1
    return ret
