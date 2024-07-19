# MIDRC mRALE Mastermind Challenge;

## Challenge Details 

### Challenge Task

The task is to predict COVID-19 severity in terms of **mRALE score** from portable chest X-ray radiographs (CXRs) obtained within 2 days of a positive COVID test. The acronym mRALE stands for modified RALE score which, in turn, stands for Radiographic Assessment of Lung Edema. This grading scale was originally validated for use in pulmonary edema assessment in acute respiratory distress syndrome and incorporates the extent and density of alveolar opacities on chest radiographs. The grading system is relevant to COVID-19 patients as the chest radiograph findings tend to involve multifocal alveolar opacities, and many hospitalized COVID-19 patients develop acute respiratory distress syndrome. To obtain an mRALE score,each lung is assigned a score for the extent of involvement by consolidation or ground glass/hazy opacities (0 = "none"; 1 = "≤ 25%"; 2 = "25%–50%"; 3 = "51%–75%"; 4 = ">75%" involvement). Each lung score is then multiplied by an overall density score (1 = "hazy", 2 = "moderate", 3 = "dense"). The sum of scores from each lung is the mRALE score.Thus, a normal chest radiograph receives a score of 0, while a chest radiograph with complete consolidation of both lungs receives the maximum score of 24.  

### Chest X-ray Radiograph Expert Annotations

The CXR exams have been annotated in terms of left lung/right lung extent of involvement and density from which the mRALE score has been calculated. Note that for frontal CXR, the left lung is displayed on the right and vice versa. For completeness, and potential use in model training, the individual left/right lung assessments are included in the annotation file (see "Get Data") with self-explanatory column headers and the encoding for involvement: 0 = "none"; 1 = "≤ 25%"; 2 = "25%–50%"; 3 = "51%–75%"; 4 = ">75%" involvement, and for overall density:1 = "hazy", 2 = "moderate", 3 = "dense". 

The estimated mRALE score is the only output your AI/ML model needs to provide. Other output scores are not allowed. 

### Performance Metrics [COMING SOON]

The primary performance metric to rank submissions is **..?..**. Submissions will be ranked using the primary performance metric. A statistically significant difference in performance between the winner and runners-up is notrequired to "win" the Challenge.Only performance on the test set will be used to rank submissions. A secondary performance metric, **..?..**, will be used to break ties, if needed. 

### Output of Your Model/Algorithm

The output of your model should be an estimated mRALE score (a single score per CXR image), which is a score between 0 (normal) and 24 (the most severe).  

### Formatting the Output of Your Model

The output of your method should be provided in a single comma-separated CSV file with image name in the first column and the corresponding output mRALE score in the second column.  

* Make sure the header and rows are in this specific format: 

fileNamePath,score [coming soon]

<dicom-name-1>.dcm,<integer mRALE score between 0 and 24> 

<dicom-name-2>.dcm,<integer mRALE score between 0 and 24> 

<dicom-name-3>.dcm,<integer mRALE score between 0 and 24> 

... 

etc. 

### The Challenge Platform Specs
The system specifications are as follows: 

| Azure VM Name     | vCPU  | RAM (GB)  |  Temp Storage SSD (GB)  |  GPU  | GPU Memory (GB)  |  Max uncached disk throughput:  IOPS/MBps  |  Max NICs |
|-------------------|-------|-----------|-------------------------|-------|------------------|--------------------------------------------|-----------|
| Standard_NC6s_v3  | 6     | 112       | 736                     | 1     | 16               | 20000/200                                  | 4         |

**Note that** internet connectivity is not provided within the Challenge platform. All necessary code, model weights, and library requirements need to be provided in your submission. GPU will only be available during the validation and test phases, not for the practice submissions during the training phase. 

### Submissions to the Challenge Platform
You need to supply a zip archive that contains a Dockerfile, all necessary code, and a trained model to allow the Challenge platform to build a Docker Image to run and evaluate your model on the practice cases, validation, or test sets, depending on the Challenge phase, respectively. Example zip archives suitable for submission are provided in the "Starting Kit" (go to the "Participate" tab, then to "Files"). Each trained model needs to be submitted in its own zip archive. It is important to note that all model training and fine-tuning needs to be performed on your own hardware. The Challenge platform only performs inference using trained models submitted in the required format. 

There is no performance assessment for the practice submissions using the practice data.The performance of your model(s) will be reported back to you and shown on the Leaderboard in the validation phase. For the test phase, performance will be reported after conclusion of the Challenge.  

**In the test phase, a description of your model and training data (plain text or Word file) needs to be included in your zip archive submission for your submission to be considered a valid submission, i.e., for its performance to be reported back to you and to be part of the Challenge.** 

### Local Computer Requirements
It is advisable to have Docker installed on your local computer so you can check locally how your code runs within a Docker Image. Go to https://docs.docker.com/ to learn more about how to install Docker on your own computer. The videos at the "Tutorials" link (left) provideadditional information.  

Docker Images will be built and run on the Challenge platform with Docker version 20.10.13 and above, so, if possible, a local install of Docker should be that version or higher. 

### Sharing of Code and Trained Models
It is highly encouraged that you allow MIDRC to make your code and trained model(s) public on the MIDRC GitHub (see "Terms and Conditions").  

### Summary Tables [COMING SOON]
 
| Challenge data       | Data available for download  | Data available on platform for inference  | Number of CXR exams  |
|----------------------|------------------------------|-------------------------------------------|----------------------|
| Training             | Yes                          | No                                        | ~2,000               |
| Practice submission  | Yes                          | Yes                                       | 12                   |
| Validation           | No                           | Yes                                       |  ~300                |
| Test                 | No                           | Yes                                       | ~1,000               |
 
| Challenge phase      | Leaderboard  |  GPU available  |  Maximum number of submissions  | Maximum size of zip archive submissions  |  Maximum submission run time on platform  |
|----------------------|--------------|-----------------|---------------------------------|------------------------------------------|-------------------------------------------|
| Training*            | N/A          | N/A             | N/A                             | N/A                                      | N/A                                       |
| Practice submission  | No           | No              | 20                              | ?                                        | ?                                         |
| Validation           | Yes          | Yes             | 10                              | ?                                        | ?                                         |
| Test                 | No           | Yes             | 3                               | ?                                        | ?                                         |

### Summary of Important Points
1. All model training and fine-tuning needs to be performed on your own hardware. The Challenge platform submission system should be used for inference only using a trained model during the Docker practice submission period and for the validation and test phases of the Challenge. 

2. The validation and test data will not be made available to participants and both sets contain unpublished data (to be made publicly available in time after conclusion of this Challenge). 

3. It is highly encouraged to practice submitting a Docker archive to the platform during the Challenge training phase for inference on the small set of ‘practice’ cases on the Challenge platform. Technical help will not be available to your team in later phases of the Challenge if your team did not participate in the practice submissions. 

4. CXRs for the Challenge validation and test datasets 

    a) are portable CXRs in the anteroposterior (AP) view
    b) were obtained within 2 days of a positive COVID test 
    c) are in DICOM format only. Any potential conversion from DICOM to a different image format must be performed within your submitted Docker container.
    d) pertain to adults (no pediatric exams)
    e) represent a single CXR per subject (patient) 
    For more details see the "Get Data" link under the "Participate" tab. 

5. Within the Challenge platform, Docker submissions will **not** be allowed to access the internet (e.g., downloading pre-trained ImageNet weights will not be possible). Everything needed to successfully run your model needs to be included in your submitted Docker container. 

6. GPU will be available on the Challenge platform only during the validation and test phases. 

7. Submissions that exit with an error, i.e., submissions that fail, do not count towards the maximum number of submissions allowed. 