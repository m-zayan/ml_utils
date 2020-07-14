from typing import Union

import numpy as np
import pandas as pd

from sklearn.datasets import load_boston, load_diabetes, load_breast_cancer, load_iris, load_digits
from sklearn.model_selection import train_test_split


class Load:
    """
    Parameters
    --------
    dtype (str): pandas or numpy, if numpy the return type is tuple (X, Y)
    """

    def __init__(self, dtype: str = 'numpy'):

        self.type = {'pandas': 0, 'numpy': 1}
        self.is_numpy = self.type[dtype]

        self.d = {'boston': load_boston,
                  'iris': load_iris,
                  'breast_cancer': load_breast_cancer,
                  'diabetes': load_diabetes,
                  'digits': load_digits}

    def __load__(self, dname: str):
        """
        Parameters
        --------
        dname (str): dataset name (available: boston, iris, breast_cancer, diabetes, digits)
        is_numpy (bool): if true return tuple contain (X, Y)

        Returns
        --------
        Union[pd.DataFrame, np.array, dict]: dataset with type numpy, pandas dataframe or dictionary in case of
        load train, test data
        """

        data: Union[pd.DataFrame, np.array, dict] = None

        if self.is_numpy:
            data = self.d[dname](True)

            print({'Name': dname.upper(), 'n_samples': data[0].shape[0], 'n_features': data[0].shape[1]})
        else:
            data_dict = self.d[dname]()
            data = pd.DataFrame(data=np.c_[data_dict['data'], data_dict['target']],
                                columns=list(data_dict['feature_names']) + ['target'])

            print({'Name': dname.upper(), 'n_samples': data.shape[0], 'n_features': data.shape[1] - 1})

        return data

    def load_data(self, dname: str):

        data = self.__load__(dname)

        return data

    def load_train_test(self, dname: str, test_size: float, ignore_type: bool = False, random_state: int = None):
        """
        Parameters
        ----------
        dname (str): dataset name

        test_size (int): test set size

        ignore_type (float): split pandas dataframe or numpy

        random_state (int): random_state of train, test split

        Returns
        -------
        dict: keys = ['train', 'test'], values are tuple (pairs) in which the first index is the feature values (x)
        and the second index is target values (y)

        Raises
        ------
        TypeError: If ignore_type = False, and Load object attribute, is_numpy = False
        """
        if not self.is_numpy and ignore_type is False:
            raise TypeError('is_numpy != True, data should be a numpy.array, '
                            'or set ignore_type=True')
        else:

            data = dict()
            x, y = (None, None)

            if not self.is_numpy:

                df = self.__load__(dname)
                x, y = df.iloc[:, :-1], df['target']

            else:
                x, y = self.__load__(dname)

            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state)

            y_train = y_train[:, np.newaxis]
            y_test = y_test[:, np.newaxis]

            data['train'] = (x_train, y_train)
            data['test'] = (x_test, y_test)

            return data
