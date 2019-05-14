#### Ziqi Chen 
#### CS344 Final Project

#### Multiclass Classification using SVM and NN on fMRI scans

##### Vision:
This project was inspired from the neuroscience principle that our visual cortex is a complex system that designates specialized area or group of areas for the processing of different types of visual stimuli. Based on this idea, the activation patterns in our brains should be unique when we are seeing an image of a human face versus a cat versus an inanimate object. 

##### Overview:
In this project, I'm using the Haxby et al (2001) dataset to perform a 3-way classification, trying to train the models to distinguish the fMRI brain scans that result from seeing a face, a cat, or a house. The dataset contains block-design fMRI data for 6 subjects who viewed 12 runs of repeated visual presentations of various stimuli. For the purpose of this project, only subjects 1 - 4 were included as they have complete fMRI data and the corresponding text labels, describing the stimuli type used in each trial.

##### Project Structure:
**loadingData.py:**  
- This module downloads a local copy of the Haxby dataset, and performs data preprocessing on the data, creating formatted X (transformed MRI scans) and Y (labels for what the subjects were seeing).  
- Subject count: 4  
- Each condition per subject: 108  
- Trials per subject: 324  
- Total trials: 1296  
- Uses NiftiMasker to transform the original 4D fMRI data (3D scans * time) into 2D vectors (numpy.ndarrays of shape (324, 39912)).      
- The transformed 2D arrays contain numerical representations of activation over time, computed as activation of brain voxel * time.  
- This module needs to be run before training the models.
  
**binaryClassification.py:**  
 - This module replicates the tutorial found here: https://nilearn.github.io/auto_examples/02_decoding/plot_haxby_anova_svm.html  
 - Two-way classification (face, house) on one subject.
  
**classification-SVM.py:**  
- A Support Vector Machine with a Linear kernel and Pipeline anova feature selection. 
- Uses the transformed 2D data as input.  
- Three-way classification (face, house, cat) on one subject (accuracy: 0.66)  
- Three-way classification (face, house, cat) on all four subjects (accuracy: 0.61)
  
**classification-NN.py:**  
- A simple Dense Neural Net  
- Uses the transformed 2D data as input.  
- Three-way classification on on all four subjects.   
- Training set is trials 1 ~ 800. Validation set 801-1296.  
  
 **classification-CNN.py:**  
 - A Convoluted Neural Net  
 - Creates a Numpy ndarray containing the fMRI scans loaded as NiBabel.Nifti.Nifti.Image objects.  
 - Data dimension per run: 40 * 64 * 64  
 - Total data dimension per subject: 324 * 40 * 64 * 64   
 - The CNN is trained on the 324 * 40 * 64 * 64 input vector of Nifti images for subject 1.  
 - Training set is trials 1 ~ 250. 
 - Three-way classification on subject 1. 
  
Examples of original fMRI scans: anatomical_subj2.png & functional_subj2.png
 
##### References:
 [Haxby, J., Gobbini, M., Furey, M., Ishai, A., Schouten, J., and Pietrini, P. (2001). Distributed and overlapping representations of faces and objects in ventral temporal cortex. Science 293, 2425-2430.](https://www.ncbi.nlm.nih.gov/pubmed/11577229)
 
 [Haxby et al. (2001) Dataset](https://zenodo.org/record/1203329#.XNpTO0MpBqs)
 
 [Haxby dataset reference](http://www.pymvpa.org/datadb/haxby2001.html#references)
 

