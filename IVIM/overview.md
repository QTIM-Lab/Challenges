# Welcome!

## Overview
This is an example competition.
The [American Association of Physicists in Medicine (AAPM)](https://www.aapm.org/) is sponsoring the Quantitative Intravoxel Incoherent Motion (IVIM) Diffusion MRI (dMRI) Reconstruction Challenge, leading up to the 2024 AAPM Annual Meeting & Exhibition. We invite participants to develop image reconstruction and model fitting methods to improve the accuracy and robustness of quantitative parameter estimation for the widely used IVIM model of dMRI [1]. Both deep learning (DL) and non-DL approaches are welcome. Methods can operate in the image-domain, in the k-space domain, or in a combination of both. In this Challenge, participants will be provided with k-space data of breast dMRI generated via rigorous simulations that accurately represent the dMRI signal generation process associated with the IVIM model across a range of diffusion weighting (b-values). The participants will be asked to derive IVIM parameter maps and compete for the most accurate reconstruction results. The two top-performing teams (only one member per team) will be awarded complimentary meeting registration to present on their methodologies during the 2024 AAPM Annual Meeting & Exhibition in Los Angeles, CA from July 21-25, 2024 (in-person attendance is required). The challenge organizers will summarize the challenge results in a journal publication after the Annual meeting.  

## Background
Diffusion MRI (dMRI) has been extensively employed over the years for the diagnosis of diseases and is increasingly used to guide radiation therapy and assess treatment responses. dMRI captures the random motion of water protons influenced by tissue microstructure, thus offering valuable insights into clinically significant tissue microstructural properties [2, 3]. Unlike conventional MRI reconstruction problems, which focus on retrieving anatomical images from measured k-space data, dMRI reconstruction aims to quantitatively determine images of biophysical tissue microstructural parameters. However, the estimation of these parameters is often accompanied by considerable uncertainties due to the complex inverse problem posed by the highly nonlinear nature of dMRI signal models [4, 5], particularly in scenarios with low signal-to-noise ratios (SNRs) resulting from fast image acquisition and physiological motion. The substantial variation and bias in parameter estimation hinder the interpretation of results and impede the reliable clinical application of dMRI in tissue characterization and longitudinal evaluations. 

## Objective
The proposed IVIM-dMRI Reconstruction Challenge aims to enhance accuracy and robustness of quantitative dMRI reconstruction, with a focus on the widely used and clinically significant IVIM model [1]. The IVIM model enables simultaneous assessment of perfusion and diffusion by fitting the dMRI signal to a biexponential model that captures both water molecular diffusion and blood microcirculation. The primary task of this Challenge is to achieve quantitative reconstruction of IVIM dMRI tissue parametric maps, specifically fractional perfusion ($f$) related to microcirculation, pseudo-diffusion coefficient ($D^*$), and true diffusion coefficient ($D_t$), from the provided k-space data, and strive for the most accurate reconstruction results.  

## Important Dates
* **January 15, 2024**: Phase 1 starts. Registration opens. Training dataset and script are made available.
* **February 15, 2024**: Phase 2 starts. Validation datasets are made available. Participants can submit preliminary results and receive feedback on relative scoring for unlimited number of times.
* **May 15, 2024**: Phase 3 starts. Final test datasets are made available. 
* **June 3,2024**: Deadline for the final submission of results and a one-page summary describing the algorithm (midnight, ET)
* **June 10, 2024**: Participants are notified with challenge results and winners (top 2) are announced.
* **July 21-25, 2024**: AAPM Annual Meeting & Exhibition**: top two teams will present on their work during a dedicated challenge session.
* **September 2024**: The challenge organizers summarize the grand challenge in a journal paper. Datasets and scoring routines will be made public.

## Results, Prizes and Publication Plan
At the conclusion of the challenge, the following information will be provided to each participant:
* The evaluation results for the submitted cases
* The overall ranking among the participants

The top 2 participants (one member from each team only):
* Will present their algorithm and results at the AAPM Annual Meeting & Exhibition (July 21-25, 2024, Los Angeles, CA). In-person attendance is required.
* Will be awarded complimentary registration to the AAPM Annual Meeting & Exhibition.

A manuscript summarizing the challenge results will be submitted for publication after the AAPM Annual Meeting.

## Organizers
* Xun Jia, Ph.D., DABR, FAAPM (Lead Organizer) (Johns Hopkins University School of Medicine)
* Jie Deng, Ph.D. (University of Texas Southwestern Medical Center)
* Junghoon Lee, Ph.D. (Johns Hopkins University School of Medicine)
* Ahad Ollah Ezzati, Ph.D. (Johns Hopkins University School of Medicine)
* Yan Dai (University of Texas Southwestern Medical Center)
* Xiaoyu Hu, Ph.D. (Johns Hopkins University School of Medicine)
* The AAPM Working Group on Grand Challenges

## Contacts
For further information, please contact the lead organizer, Xun Jia (xunjia@jhu.edu)

## References
1. Le Bihan, D., et al., *MR imaging of intravoxel incoherent motions: application to diffusion and perfusion in neurologic disorders*. Radiology, 1986. **161**(2): p. 401-407.

