## Challenge details 
### Challenge task
The classification of frontal view portable chest radiographs (CXRs) for the presence of pneumonia, both on a by-image basis (the overall classification task) and on a by-pixel basis (the explainability maps). 
### Chest radiographs and expert annotations
The CXR images (a single antero-posterior view CXR per patient in DICOM format) have been annotated by 3 expert radiologists (out of a pool of 14 expert annotators). Annotators provided a score for pneumonia severity and manual outlines of lung opacities, if any. The severity scores were used by the challenge organizers to balance the distribution of normal, mild, moderate and severe cases between validation and test sets. Note that ‘normal’ images, i.e., images without lung opacities are also included! 
The expert manual outlines have been used to generate probability maps for the presence of lung opacities, with regions annotated by 3 experts receiving a probability of 1, by 2 annotators a probability of 1/2, by one annotator a probability of 1/3, and by none of the annotators a probability of 0. Please see the “Evaluation” tab for details on how this reference standard is used to assess your generated explainability maps and calculate the primary performance metric. 

### Model training 
Annotated training data is not provided for this Challenge. You are welcome to train your model using your own data, publicly available datasets, and the data available in the MIDRC portal data.midrc.org.  The MIDRC GitHub repository contains helpful Jupyter notebooks as well for cohort building and downloading. 

### Performance metrics
The primary performance metric to rank submissions is the weighted log-loss calculated from the pixel-by-pixel explainability maps as a measure for the agreement of participants’ explainability maps and the probability maps based on the 3 expert manual annotations of lung opacities. The secondary performance metric is calculated from the by-image output and is the area under the receiver operating curve (AUCROC) in the task of classifying CXRs for the presence of pneumonia. See “Evaluation” for more details.
Submissions will be ranked using the prmimary performance metric. A statistically significant difference in performance between the winner and runners-up is not required to "win" the Challenge. Only performance on the test set will be used to determine the final ranking of submissions. 

### Output of your model/algorithm
For each CXR, the output of your model should be 
1.	an estimated overall probability of pneumonia, and 
2.	an explainability map indicating the likelihood of lung opacity presence at each pixel.

### Formatting the output of your model
1. The by-image output of your method should be provided in a single comma-separated CSV file with image names in the first column and the corresponding output probability score in the second column.  

	Make sure the header and rows are in this specific format: 

			fileNamePath,score 
			<dicom-name-1>.dcm,<float between 0 and 1> 	
			<dicom-name-2>.dcm,<float between 0 and 1> 
			<dicom-name-3>.dcm, float between 0 and 1> 
			... 
			etc. 

2. The by-pixel explainability maps should be of the same size as the input image and at each pixel indicate the likelihood of there being a lung opacity at that location with values between 0 and 1. Values do not need to add to 1 for an image. Note that also ‘normal’ images, i.e., images without lung opacities will be part of the validation and test sets. [COMING SOON: the exact format for the explainability maps].

### The Challenge platform specs
[COMING SOON: exact platform specs, including GPU]

Note that internet connectivity is not provided within the Challenge platform. All necessary code, model weights, and library requirements need to be provided in your submission. GPU will only be available during the validation and test phases, not for the practice submissions during the training phase. 

### Submissions to the Challenge platform
For detailed instructions how to perform submissions to the platform, please see the “How to submit” tab. 
 It is important to note that all model training and fine-tuning needs to be performed on your own hardware. The Challenge platform only performs inference using trained models submitted in the required format. 

There is no performance assessment for the practice submissions using the practice data, given the small number of cases in this phase, but you will be able to compare output generated on the platform to that generated locally. The performance of your model(s) will be reported back to you and shown on the Leaderboard in the validation phase. For the test phase, performance will be reported after conclusion of the Challenge.  

In the test phase, a description of your model and training data (plain text or Word file) needs to be included in your zip archive submission for your submission to be considered a valid submission, i.e., for its performance to be reported back to you and to be part of the Challenge.  

### Local computer requirements
It is advisable to have Docker installed on your local computer so you can check locally how your code runs within a Docker Image. Go to https://docs.docker.com/ to learn more about how to install Docker on your own computer and see "Tutorials" for additional information.  
Docker Images will be built and run on the Challenge platform with Docker. A local install of Docker should be version version 20.10.13 and above. 

### Sharing of code and trained models
It is highly encouraged that you allow MIDRC to make your code and trained model(s) public on the MIDRC GitHub and a requirement to receive prize money (see "Terms and Conditions").  

### Summary
>**Challenge data,** single portable CXR per patient, normal CXRs without lung opacities are included 
>Training phase: only 10 'annotated practice' cases
>Validation phase: ~300 CXRs
>Test	phase:~2000 CXRs

> **Submissions**
> Training phase: no limit
> Validation phase: 10 (leaderboard)
> Test phase: 3 (no leaderboard)
 
[COMING SOON: maximum size of submissions, maximum run time]

Note: Submissions that exit with an error, i.e., submissions that fail, do not count towards the maximum number of submissions allowed.