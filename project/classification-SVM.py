#select a three-way classification model


# https://scikit-learn.org/stable/modules/svm.html#svm

from loadingData import *
from sklearn.svm import SVC
from sklearn.feature_selection import SelectPercentile, f_classif, SelectKBest
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from nilearn import image
from nilearn.plotting import plot_stat_map, show
from sklearn.model_selection import LeaveOneGroupOut, cross_val_score
from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier

# Define the dimension reduction to be used.
# Here we use a classical univariate feature selection based on F-test,
# namely Anova. When doing full-brain analysis, it is better to use
# SelectPercentile, keeping 5% of voxels
# (because it is independent of the resolution of the data).
feature_selection = SelectPercentile(f_classif, percentile=5)

#one-vs-the-rest
#cited from https://scikit-learn.org/stable/modules/svm.html#multi-class-classification
lin_svc = LinearSVC()
facecathouse_svc = Pipeline([('anova', feature_selection), ('svc', lin_svc)])
facecathouse_svc.fit(FHC, conditions_threeway)

another_svc = OneVsRestClassifier(Pipeline([('anova', SelectKBest(f_classif, k=500)), ('svc', SVC(kernel = 'linear'))]))
another_svc.fit(FHC, conditions_threeway)

# Output accuracy
# Define the cross-validation scheme used for validation.
# Here we use a LeaveOneGroupOut cross-validation on the session group
# which corresponds to a leave-one-session-out
def modelAccuracy(model, X, conditions, groups):
    cv = LeaveOneGroupOut()

    # Compute the prediction accuracy for the different folds (i.e. session)
    cv_scores = cross_val_score(model, X, conditions, cv=cv, groups=groups)

    # Return the corresponding mean prediction accuracy
    classification_accuracy = cv_scores.mean()

    # Print the results
    print("Classification accuracy: %.4f / Chance level: %f" %
          (classification_accuracy, 1. / len(conditions.unique())))

print("Linear model on face vs cat vs house: ")
modelAccuracy(facecathouse_svc, FHC, conditions_threeway, session_threeway)

print("The second model on face vs cat vs house: ")
modelAccuracy(another_svc, FHC, conditions_threeway, session_threeway)

for cv in range(2, 10, 1):
    cross_validation = cross_val_score(facecathouse_svc, FHC, conditions_threeway, cv = cv, verbose = 1)
    print("Linear kernel model cross validation score: ", cross_validation.mean())

for cv in range(2, 10, 1):
    cross_validation = cross_val_score(facecathouse_svc, FHC, conditions_threeway, cv = cv, verbose = 1)
    print("The other one-vs-rest validation score: ", cross_validation.mean())


def visualizeResults(kernel, masker, func_filename = haxby_dataset.func[0]):
    coef = kernel.coef_
    # reverse feature selection
    coef = feature_selection.inverse_transform(coef)
    # reverse masking
    weight_img = masker.inverse_transform(coef)

    # Use the mean image as a background to avoid relying on anatomical data
    mean_img = image.mean_img(func_filename)

    # Create the figure
    plot_stat_map(weight_img, mean_img, title='SVM weights')

    # Saving the results as a Nifti file may also be important
#    weight_img.to_filename('haxby_face_vs_house.nii')
    show()

#visualizeResults(lin_svc, masker)

#TO DO: improve current accuracy of 0.6265.