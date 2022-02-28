import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
from myConvexHull import MyConvexHull

# Dataset iris
# data = datasets.load_iris()

# Dataset diabetes
data = datasets.load_diabetes()

#create a DataFrame
df = pd.DataFrame(data.data, columns=data.feature_names)
df['Target'] = pd.DataFrame(data.target)
print(df.head())

#visualisasi hasil ConvexHull
plt.figure(figsize = (10, 6))
colors = ['b','r','g', 'c', 'm', 'y']

# iris: Petal Width vs Petal Length
# plt.title('Petal Width vs Petal Length')
# plt.xlabel(data.feature_names[2])
# plt.ylabel(data.feature_names[3])

# iris: Sepal Width vs Sepal Length
# plt.title('Sepal Width vs Sepal Length')
# plt.xlabel(data.feature_names[0])
# plt.ylabel(data.feature_names[1])

# diabetes: Sex vs BMI
plt.title('Sex vs BMI')
plt.xlabel(data.feature_names[2])
plt.ylabel(data.feature_names[3])

try:
    for i in range(len(data.target_names)):
        bucket = df[df['Target'] == i]

        # iris: Petal Width vs Petal Length
        # bucket = bucket.iloc[:,[0,1]].values

        # iris: Sepal Width vs Sepal Length
        # bucket = bucket.iloc[:,[2,3]].values

        hull = MyConvexHull(bucket) #bagian ini diganti dengan hasil implementasi ConvexHull Divide & Conquer

        plt.scatter(bucket[:, 0], bucket[:, 1], label=data.target_names[i])

        for simplex in hull.simplices:
            plt.plot(bucket[simplex, 0], bucket[simplex, 1], colors[i])
    plt.legend()
except:
    #diabetes: Sex VS BMI
    bucket = df

    bucket = bucket.iloc[:,[2,3]].values
    hull = MyConvexHull(bucket)

    # plt.scatter(bucket[:, 0], bucket[:, 1],color =colors[0])

    plt.scatter(bucket[:, 0], bucket[:, 1],color =colors[0])

    lengthOfHull = len(hull.simplices)
    for simplex in hull.simplices:
            plt.plot(bucket[simplex, 0], bucket[simplex, 1], colors[0])
plt.show()