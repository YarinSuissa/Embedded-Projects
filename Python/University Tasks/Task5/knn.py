import numpy as np


class KNN:
    def __init__(self, k) -> None:
        if not self.input_valid(k, int):
            raise ValueError()
        self.num_of_neighbors = k
        self.trained_data = np.zeros(1)

    def fit(self, x_train, y_train) -> None:
        if not self.input_valid(x_train, np.ndarray) or not self.input_valid(y_train, np.ndarray):
            raise ValueError()
        self.trained_data = np.zeros((x_train.shape[0], x_train.shape[1] + 1), dtype=int)
        for row in range(x_train.shape[0]):
            self.trained_data[row, 0] = y_train[row]
            self.trained_data[row, 1:] = x_train[row]
    def predict(self, x_test) -> np.ndarray:
        if self.default_matrices(self.trained_data):
            raise IOError()
        output_labels = np.zeros(x_test.shape[0], dtype=int)
        for point in range(x_test.shape[0]):
            '''
            Make the euclidean calculation across the matrix at once
            1. tile "Distances" so they'll be the same dimensions as the trained data
            2. make element-wise subtraction between the matrices
            3. power by 2 (as the euclidian distance is sqrt[ (x1-x2)^2 + (y1-y2)^2 + ... ]
            4. take sqrt. at this point we have an array of distances for a given point in x_test
            '''
            distances = np.tile(x_test[point, :], (self.trained_data.shape[0], 1))
            distances = np.subtract(self.trained_data[:, 1:], distances)
            distances = np.power(distances, 2)
            sums = np.sum(distances, axis=1)
            distances = np.sqrt(sums)
            distances = distances.argsort()
            votes = {}
            for i in range(self.num_of_neighbors):
                category = int(self.trained_data[distances[i], 0])
                if category not in votes.keys():
                    votes.update({category: 1})
                else:
                    votes.update({category: int(votes.get(category) + 1)})
            keys = list(votes.keys())
            values = list(votes.values())
            final_category = keys[values.index(max(values))]
            output_labels[point] = final_category
            #concatenated_array = np.insert(x_test[point],0,final_category)
            #self.trained_data = np.insert(self.trained_data,self.trained_data.shape[0],concatenated_array, axis=0)

        return output_labels

    @staticmethod
    def input_valid(k, instance) -> bool:
        if not isinstance(k, instance):
            return False
        if (isinstance(k, int) or isinstance(k, float)) and k <= 0:
            return False
        return True

    @staticmethod
    def default_matrices(*matrices) -> bool:
        for matrix in matrices:
            if not np.any(matrix):
                return True
        return False
