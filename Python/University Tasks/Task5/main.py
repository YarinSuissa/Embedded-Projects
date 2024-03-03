import numpy as np
from knn import KNN
from k_means import KMeans

# KNN
train = np.genfromtxt('mnist_train_min.csv', delimiter=',', skip_header=1, dtype=np.int_)
test = np.genfromtxt('mnist_test_min.csv', delimiter=',', skip_header=1, dtype=np.int_)
y_train = train[:, 0]
X_train = train[:, 1:]
y_test = test[:, 0]
X_test = test[:, 1:]
model = KNN(k=10)
model.fit(X_train, y_train)
pred = model.predict(X_test)

# KMeans
data = np.genfromtxt('iris.csv', delimiter=',', skip_header=1, dtype=np.float_)[:,1:4]
c1 = np.mean(data[:50],axis=0)
c2 = np.mean(data[50:100],axis=0)
c3 = np.mean(data[100:],axis=0)
rng = np.random.default_rng()
rng.shuffle(data, axis=0) # shuffle data rows
train = data[:100]
test = data[100:]
kmeans = KMeans(k=3, max_iter=100)
kmeans.initialize(np.array([c1,c2,c3]))
class_centers = kmeans.fit(train)
print(kmeans.wcss())
classification = kmeans.predict(test)
