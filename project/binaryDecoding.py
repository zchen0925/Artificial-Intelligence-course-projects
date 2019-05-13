#replicated the tutorial at https://nilearn.github.io/auto_examples/02_decoding/plot_haxby_anova_svm.html

from loadingData import *
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from nilearn import image
from nilearn.plotting import plot_stat_map, show
# Define the dimension reduction to be used.
# Here we use a classical univariate feature selection based on F-test,
# namely Anova. When doing full-brain analysis, it is better to use
# SelectPercentile, keeping 5% of voxels
# (because it is independent of the resolution of the data).
feature_selection = SelectPercentile(f_classif, percentile=5)

# Output accuracy
from sklearn.model_selection import LeaveOneGroupOut, cross_val_score

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

svc_fc = SVC(kernel='linear')
model_fc = Pipeline([('anova', feature_selection), ('svc', svc_fc)])
model_fc.fit(FC, conditions_facecat)
fc_pred = model_fc.predict(FC)
print("Linear model on face vs cat: ")
modelAccuracy(model_fc, FC, conditions_facecat, session_facecat)
visualizeResults(svc_fc, masker)
#
svc_fh = SVC(kernel='linear')
model_fh = Pipeline([('anova', feature_selection), ('svc', svc_fh)])
model_fh.fit(FH, conditions_facehouse)
fh_pred = model_fh.predict(FH)
print("Linear model on face vs house: ")
modelAccuracy(model_fh, FH, conditions_facehouse, session_facehouse)
visualizeResults(svc_fh, masker)