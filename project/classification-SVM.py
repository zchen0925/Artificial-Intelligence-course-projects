# Ziqi Chen
# CS 344 Final Project
# Professor Vander Linden
# fMRI Data multicategory classification

# classification-SVM employs a Linear Support Vector Classification estimator on
# the transformed 2D voxel-time vectors and predicts the labels for the images that subjects were looking at.


from loadingData import *
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn import svm
from sklearn.svm import LinearSVC, SVC
from sklearn.pipeline import Pipeline
from nilearn import image
from nilearn.plotting import plot_stat_map, show
from sklearn.model_selection import LeaveOneGroupOut, cross_val_score
import numpy as np
import matplotlib.pyplot as plt

#cited from: https://nilearn.github.io/auto_examples/02_decoding/plot_haxby_anova_svm.html
    # Define the dimension reduction to be used.
    # Here we use a classical univariate feature selection based on F-test,
    # namely Anova. When doing full-brain analysis, it is better to use
    # SelectPercentile, keeping 5% of voxels
    # (because it is independent of the resolution of the data).
feature_selection = SelectPercentile(f_classif, percentile=5)

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
          # (classification_accuracy, 1. / len(conditions.unique())))
          (classification_accuracy, 1. / 3))

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

#one-vs-the-rest linear kernel
#cited from https://scikit-learn.org/stable/modules/svm.html#multi-class-classification
#Pipeline ANOVA SVM with anova F-value, percetile feature selection
lin_svc = LinearSVC()
facecathouse_svc = Pipeline([('anova', feature_selection), ('svc', lin_svc)])
facecathouse_svc.set_params(svc__C = 10, svc__max_iter = 2500)
facecathouse_svc.fit(FHC, conditions_threeway)

print("Pipelined SVM with linear kernel accuracy: ")
modelAccuracy(facecathouse_svc, FHC, conditions_threeway, session_threeway)

cross_validation = cross_val_score(facecathouse_svc, FHC, conditions_threeway, cv = 6, verbose = 1)
print("Pipelined SVM with linear kernel cross validation score: ", cross_validation.mean())

# fitting on all four subjects
lin_svc1 = LinearSVC()
allSubs_svc = Pipeline([('anova', feature_selection), ('svc', lin_svc1)])
allSubs_svc.set_params(anova__percentile = 3, svc__max_iter = 3000)
allSubs_svc.fit(X_all, Y_all)

print("Linear SVM with all subjects accuracy: ")
modelAccuracy(allSubs_svc, X_all, Y_all, session_all)

cross_validation = cross_val_score(allSubs_svc, X_all, Y_all, cv = 6, verbose = 1)
print("Linear SVM with all subjects cross validation score: ", cross_validation.mean())
#
# visualizeResults(lin_svc, masker)
