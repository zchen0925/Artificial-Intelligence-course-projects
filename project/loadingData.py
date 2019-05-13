from nilearn import datasets, image, plotting
from nilearn.input_data import NiftiMasker
from nilearn.image.image import mean_img
from nilearn.image import index_img
import numpy as np
import pandas as pd

#import Haxby et al.(2001): Faces and Objects in Ventral Temporal Cortex (fMRI)
# Subjects 5 and 6 don't have complete label or anatomical information, only included subjects 1-4
haxby_dataset = datasets.fetch_haxby(subjects=4)

#load nifti images for the given subjects. Range 0-3
#defaults to subject 2
def loadSubject(subjectNum = 1):
    # 'func' is a list of filenames: one for each subject
    fmri_filename = haxby_dataset.func[subjectNum]
    # print basic information on the dataset
    print('First subject functional nifti images (4D) are at: %s' %
          fmri_filename)  # 4D data
    return fmri_filename

#plotting subject's anatomical brain
def plotAnat(subjectNum = 1):
    path = haxby_dataset.anat[subjectNum]
    plotting.plot_stat_map(path, threshold=3)
    plotting.show()

#plotting mean functionam MRI
def plotMeanFunc(subjectNum = 1):
    mean_haxby = mean_img(haxby_dataset.func[subjectNum])
    plotting.plot_stat_map(mean_haxby, threshold=3)
    plotting.show()

#plotting one random scan of fMRI
def plotRandomFunc(subjectNum = 1):
    rand_func = index_img(haxby_dataset.func[subjectNum], 30)
    plotting.plot_stat_map(rand_func, threshold=3)
    plotting.show()

fmri_filename = loadSubject(0)
# plotAnat(subjectNum = 2)
# plotMeanFunc(2)
# plotRandomFunc(2)

behavioral = pd.read_csv(haxby_dataset.session_target[0], sep=" ")
conditions = behavioral['labels']

facecat_mask = conditions.isin(['face', 'cat'])
conditions_facecat = conditions[facecat_mask]
session_facecat = behavioral[facecat_mask].to_records(index = False)

facehouse_mask = conditions.isin(['face', 'house'])
conditions_facehouse = conditions[facehouse_mask]
session_facehouse = behavioral[facehouse_mask].to_records(index = False)

threeway_mask = conditions.isin(['face', 'house', 'cat'])
conditions_threeway = conditions[threeway_mask]
session_threeway = behavioral[threeway_mask].to_records(index = False)
print("Number of trials: ", len(conditions_threeway))
mask_filename = haxby_dataset.mask
#masking the data from 4D image to 2D array: voxel x time
#with smothing and standardization
masker = NiftiMasker(mask_img=mask_filename, smoothing_fwhm=4, standardize=True, memory="nilearn_cache", memory_level=1)
print(haxby_dataset.mask)
X = masker.fit_transform(fmri_filename)

# Apply our condition_mask
FC = X[facecat_mask]

FH = X[facehouse_mask]

FHC = X[threeway_mask]

#three-way classification with NN
FHC_train = FHC[:250]
conditions_train = conditions_threeway[1:250]
FHC_val = FHC[250:]
Y_val = conditions_threeway[250:]
# print("Length of training data: ", len(FHC_train))
# print("Lenth of validation data: ", len(FHC_val))


#type : numpy.ndarry
print("Shape of transformed fMRI data:", FHC.shape)
print(FHC[0])


# References
# Haxby, J., Gobbini, M., Furey, M., Ishai, A., Schouten, J., and Pietrini, P. (2001). Distributed and overlapping representations of faces and objects in ventral temporal cortex. Science 293, 2425-2430.


def processSubject(sub):
    mask_filename = haxby_dataset.mask
    # masking the data from 4D image to 2D array: voxel x time
    # with smothing and standardization
    masker = NiftiMasker(mask_img=mask_filename, smoothing_fwhm=4, standardize=True, memory="nilearn_cache",
                         memory_level=1)
    X = masker.fit_transform(loadSubject(sub))
    behavioral = pd.read_csv(haxby_dataset.session_target[sub], sep=" ")
    conditions = behavioral['labels']
    threeway_mask = conditions.isin(['face', 'house', 'cat'])
    conditions_threeway = conditions[threeway_mask]
    session_threeway = behavioral[threeway_mask].to_records(index = False)
    FHC = X[threeway_mask]
    return FHC, conditions_threeway, session_threeway

X_all = np.empty(shape = (0, 39912))
Y_all = []
session_all = np.empty(shape = (324, ))
# for sub in range(0, 4):
#     x, y, session = processSubject(sub)
#     print(y)
#     print(session)
#     X_all = np.concatenate((X_all, x), axis = 0)
#     # session_all = np.concatenate((session_all, session), axis = 0)
#
# print("Shape of concatenated transformed fMRI data:", X_all.shape)
# print(X_all[0])
# print("Length of concatenated labels:", Y_all.shape)
# print(Y_all)