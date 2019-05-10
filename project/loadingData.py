from nilearn import datasets, image, plotting
import pandas as pd

haxby_dataset = datasets.fetch_haxby()
# 'func' is a list of filenames: one for each subject
fmri_filename = haxby_dataset.func[0]

# print basic information on the dataset
print('First subject functional nifti images (4D) are at: %s' %
      fmri_filename)  # 4D data

fig1 = plotting.plot_img("/home/zc23/CS344/anat.nii")
plotting.show()

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


from nilearn.input_data import NiftiMasker
mask_filename = haxby_dataset.mask
#with smothing and standardization
masker_smooth = NiftiMasker(mask_img=mask_filename, smoothing_fwhm=4,
                     standardize=True, memory="nilearn_cache", memory_level=1)
X = masker_smooth.fit_transform(fmri_filename)
# Apply our condition_mask
FC_smooth = X[facecat_mask]

FH_smooth = X[facehouse_mask]

FHC_smooth = X[threeway_mask]

#only standardization
masker = NiftiMasker(mask_img=mask_filename, smoothing_fwhm=4,
                     standardize=True, memory="nilearn_cache", memory_level=1)
X = masker.fit_transform(fmri_filename)
# Apply our condition_mask
FC = X[facecat_mask]

FH = X[facehouse_mask]

FHC = X[threeway_mask]

