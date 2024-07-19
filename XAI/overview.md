# MIDRC XAI Challenge:
## Decoding AI decisions for pneumonia on chest radiographs
### Brought to you by the MIDRC Grand Challenges Working Group and MedICI 
#### Organized in the spirit of cooperative scientific progress that benefits the common good and health outcomes for all. 
#### Registration will open July 19!
#### MIDRC XAI is a MICCAI-endorsed event 

### Unmet need addressed by this Challenge
In medical image analysis, including in classification tasks, thereis a critical unmet need for making AI models explainable. Existing saliency map techniques, such as Grad-CAM and LIME, offer visual explanations of AI decision-making processes but have notable shortcomings. These techniques often lack consistency and reliability, sometimes producing different explanations for similar inputs. Moreover, different techniques can offer drastically different ‘explanations’ for output of the same AI model for the same input. Furthermore, they can be sensitive to minor perturbations in the input data, leading to variations in the generated saliency maps that undermine their trustworthiness [ref].
Additionally, saliency maps typically highlight regions of an image without providing clear, interpretable insights into why those regions are significant. The black-box nature of these AI models, combined with the opaque explanations provided by current saliency map techniques, hinders their potential utility in clinical settings, where transparency and interpretability are paramount for gaining the trust of healthcare professionals.
Thus, there is a pressing need for more robust, reliable, and interpretable explainability methods in AI-driven medical image analysis. We are excited to be conducting this Challenge and hope you will participate! We encourage you to invite your colleagues and friends to create a team. 

### Clinical task
Pneumonia manifests on chest radiographs primarily as lung opacities. These opacities appear as areas of increased density compared to the surrounding lung tissue and can be classified as either lobar, bronchopneumonia, or interstitial, depending on the distribution and pattern. The severity of pneumonia on radiographs can vary from mild, with minimal opacities, to severe, with extensive consolidation and possible complications like pleural effusion or abscess formation.
### The goal of this Challenge
This Challenge aims to advance explainable AI for medical image analysis and the goal for participants is to develop and train explainable artificial intelligence/machine learning (AI/ML) model(s) in the task of classifying frontal-view portable chest radiographs (CXRs) for the presence of lung opacities associated with any type of pneumonia for evaluation against the reference standard for the validation and test datasets. The AI/ML output should be, for each CXR, 1) a likelihood that the patient presented with pneumonia of any type, and 2) an ‘explainability’ map, interpretable as the probability of presence of lung opacity at each pixel (of the same size as the input image). Please see the “Details” and “Evaluation” tabs. 
This Challenge uses Docker as a containerization solution. Data will not be available for download.
 
### Prizes
Cash prizes through 7th place!
* 1st Place - $ 15,000
* 2nd Place - $ 8,000
* 3rd Place - $ 7,000
* 4th - 7th Place - $ 5,000 each

First and second place teams will have the opportunity to work with MIDRC when advancing their method/model through the FDA regulatory process. 

See the "Terms and Conditions" for general rules, constraints on participation eligibility and prizes, Challenge manuscripts, and acknowledgements. 

Please make sure to familiarize yourself with the Challenge and read the “Terms and Conditions” before signing up. You will need to agree to these "Terms and Conditions" as part of the sign-up process. Also, remember to check out the Tutorials and please take advantage of the opportunity to make practice submissions during the training phase. 
Questions pertaining to this Challenge should be posted to the ‘Forum’.
 
### Important Dates

Registration opens - July 19, 2024

Calibration Phase opens - August 10, 2024

Validation Phase opens - September 10, 2024

Test Phase opens - October 1, 2024

Challenge conlcuded - October 22, 2024

Winners announced - early November, 2024