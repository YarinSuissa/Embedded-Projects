import numpy as np


class KMeans:
    def __init__(self, k, max_iter):
        if not self.input_valid(k, int) or not self.input_valid(max_iter, int):
            raise ValueError()
        self.num_of_clusters = k
        self.max_iter = max_iter
        self.clusters = {}
        self.kmeans_wcss = 0

    def initialize(self, centroids):
        if self.num_of_clusters != len(centroids) or not self.input_valid(centroids, np.ndarray):
            raise ValueError()
        self.centroids_dict = {}
        for index in range(self.num_of_clusters):
            self.centroids_dict.update({index: centroids[index]})

    def stack_centroids(self) -> np.ndarray:
        return np.stack(self.centroids_dict.values(), axis=0)

    def concatenate_cluster(self, cluster) -> np.ndarray:
        return np.stack(list(cluster))

    def wcss(self):
        return self.kmeans_wcss

    def fit(self, X_train) -> dict:
        while self.max_iter > 0:
            self.clusters = {}
            self.kmeans_wcss = 0
            stacked_centroids = self.stack_centroids()
            for point in range(X_train.shape[0]):
                distances = np.tile(X_train[point, :], (stacked_centroids.shape[0], 1))
                distances = np.subtract(stacked_centroids, distances)
                distances = np.power(distances, 2)
                sums = np.sum(distances, axis=1)
                distances = np.sqrt(sums)
                core_index = np.argmin(distances)
                closest_distance = float(np.min(distances))
                if core_index not in self.clusters.keys():
                    self.clusters.update({core_index: [X_train[point, :]]})
                else:
                    self.clusters.get(core_index).append(X_train[point, :])
                self.kmeans_wcss = self.kmeans_wcss + closest_distance * closest_distance
            for key in self.clusters.keys():
                key_cluster = self.concatenate_cluster(self.clusters.get(key))
                key_cluster = np.sum(key_cluster, axis=0) / key_cluster.shape[0]
                self.centroids_dict.update({key: key_cluster})
            self.max_iter -= 1
        return self.centroids_dict

    def get_centroids(self):
        return self.centroids_dict

    def predict(self, X):
        centroid_matrix = np.stack(list(self.centroids_dict.values()))
        output_cluster = np.zeros(X.shape[0])
        for point in range(X.shape[0]):
            point_matrix = np.tile(X[point], (centroid_matrix.shape[0], 1))
            distances = np.subtract(centroid_matrix, point_matrix)
            distances = np.power(distances, 2)
            distances = np.sum(distances, axis=1)
            distances = np.sqrt(distances)
            output_cluster[point] = np.argmin(distances)
            centroid_id = np.min(distances)
        return output_cluster

    @staticmethod
    def input_valid(k, instance) -> bool:
        if not isinstance(k, instance):
            return False
        if (isinstance(k, int) or isinstance(k, float)) and k <= 0:
            return False
        return True
