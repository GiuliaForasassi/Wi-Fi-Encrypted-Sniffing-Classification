from sklearn.model_selection import cross_validate
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import accuracy_score
from sklearn.manifold import TSNE
import numpy as np
import matplotlib
from utils import plot_tsne

# READ DATASET
with open('dataset.npy', 'rb') as f:
    X = np.load(f)
    y = np.load(f)

# # DECISION TREE TRAINING
# # k-fold cross validation
# clf = DecisionTreeClassifier(random_state=0)
# cv_results = cross_validate(clf, X, y, cv=5)
# print(cv_results)
# print('Accuracy:', cv_results['test_score'].mean())

# leave one out
accuracies = []
cf_matrix = np.zeros([4, 4])
loo = LeaveOneOut()
for train_index, test_index in loo.split(X):
    #clf = DecisionTreeClassifier(random_state=0)
    clf = RandomForestClassifier(random_state=0)
    clf.fit(X[train_index], y[train_index]) # per allenare l'albero
    y_pred = clf.predict(X[test_index]) # predizione
    y_true = y[test_index]
    accuracy = accuracy_score(y_true, y_pred)
    accuracies.append(accuracy)
    cf_matrix = cf_matrix + confusion_matrix(y_true, y_pred, labels=range(4))


np_accuracies = np.array(accuracies) # trasformo lista accuracies in array numpy
print(accuracies)
print('Accuracy:', np_accuracies.mean())
print(cf_matrix)

plot_tsne(X, y)
