# MIDRC mRALE Mastermind Challenge; Get Data 

We encourage you to use the annotated data made available by MIDRC to train your model(s). **If you are unfamiliar with downloading data from our data portal, please check out the “Tutorials” page on this Challenge Platform**. You can also use your own data for model development and training. The type of training data, whether public or private, needs to be disclosed and briefly described to accompany submissions in the test phase. 

## The Annotated Training Cohort provided by MIDRC 
We provide material on the [MIDRC mRALE Mastermind Challenge GitHub repo](https://github.com/MIDRC/COVID19_Challenges/tree/main/Challenge_2023_mRALE%20Mastermind) to help you download a training cohort from our data portal (data.midrc.org) 

1. A file manifest (json file) for downloading preselected imaging studies from data.midrc.org and corresponding metadata such as demographics.  

2. An annotation file (csv file) with the annotations corresponding to the imaging studies in the JSON file manifest. Note that your AI/ML model will need to predict only the mRALE score (the last column in the annotation csv). 

3. A README with instructions. 

> **Note:** Cohort building/downloading within the data portal is performed on the **imaging study** level. Each imaging study may contain multiple CXRs. Thus, the training cohort that you will download may contain images not useful for your model training (such as, e.g., post-processing images), and we strongly encourage you to curate your training cohort locally after downloading. The provided reference standard mRALE score applies to all CXRs of an imaging study.  

## Docker Practice Data 

A few practice images (AP view portable chest radiographs in DICOM format) without annotations are provided directly on this platform as practice data (see “Practice Data” under the "Files" link on the left). These images will be connected to the platform during the training phase for you to run inference on as practice and to troubleshoot Docker submissions in general. You should expect the same output (within the expected precision) of your AI/ML model on the platform as you obtain locally for these practice images. 

## Validation and Test Cohorts 

The images in the validation and test sets (not available to you for download)are unpublished (i.e., not yet available on the public-facing side of data.midrc.org) portable anteroposterior chest radiographs with a single radiograph per patient. Some radiographs have a variety of medical devices present (e.g., EKG leads or endotracheal tubes). The presence or absence of such devices is not necessarily indicative of COVID severity. No post-processed images are included. There is no overlap in patients among training, validation, and test cohorts.  

## Getting Started with Docker 

To test your submission template locally, you will first need to download and install Docker on your local machine. Go to [https://docs.docker.com/](https://docs.docker.com/) to learn more and check out the "Tutorials" link under the "Learn the Details" tab.  

Docker Images will be run with docker version *20.10.13* and above, so, if possible, a local install of Docker should be that version or higher.

## Starting Kit 
Example (dummy) submission archives and accompanying instructions are provided for PyTorch and TensorFlow (made in Ubuntu with bash, but they should be compatible in MacOS and Windows environments) in the "Starting Kit" under the "Files" link (see left). 

> Note that any instructions on how to build Docker Images in the tutorial videos and in the README in the "Starting Kit" at the "Files" link (see left) are provided only for you to check how your code works within a Docker Image locally. It is highly advised to ensure your code runs locally within Docker (without accessing the internet) before submitting to the Challenge platform. Do not submit built Docker Images to the Challenge platform. When submitting your model to the platform for inference, the building of the Docker Image will be performed on the Challenge platform (and your zip archive submission must contain all necessary code to build this Docker Image). 

## Uploading Submissions 
To upload your submission (zip archive) to the Challenge platform, go to the "Submit/View Results" link (left). For more instructions, watch the video under ‘How to’ step 3 in the “Tutorials” section (the "Tutorials" link under the "Learn the Details" tab.) 