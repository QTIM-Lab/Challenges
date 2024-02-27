This challenge consists of 3 phases:

##### Phase 1 (training & development phase)
At the start of phase 1, a **training dataset** with 14,000 cases will be provided for training, validation, and algorithm development. Each case will include 4 types of data as illustrated in Figure 1:

(1) image without metal (label)
(2) image with metal (corrupted)
(3) sinogram without metal (label)
(4) sinogram with metal (corrupted)

The methodology used to produce the challenge datasets will be shared in detail via the challenge website (COMING SOON). The desired final result is an image without any streak artifacts but that still contains the metal object (9). Participants can choose to develop image-domain, sinogram-domain, or hybrid MAR methods. For example, an image-domain method could generate (1) from (2) directly. A sinogram-domain method could generate (3) from (4) and then use the reconstruction routine to generate (1). A hybrid method could start from (4) and perform sinogram-domain operations, reconstruction, and image-domain operations to achieve (1), possibly in an iterative reconstruction framework. A standard 2D filtered back projection (FBP) reconstruction routine will be provided in Python so that the participants do not need to develop their own reconstruction method (unless their MAR approach were to include a new reconstruction). Since the final image should still contain the metal object, participants may need to estimate the contour of the metal object and reintroduce the metal object in the end.

##### Phase 2 (feedback & refinement phase)
At the start of phase 2, a **testing dataset** with an additional 1,000 cases will be provided for the participants’ own testing purpose. The 1,000 cases will not be used for the final score, but we will request that participants compute standard metrics (PSNR and SSIM) and report those using the Field-Of-View (FOV) image mask that will be provided to mask out the out-of-FOV region.

The results will be used only as supporting information. These 1,000 cases should not be used for training & validation and should not be submitted.

Figure 1

At the start of phase 2, we will also provide a **preliminary scoring dataset** including 5 clinical cases (without labels) (i.e., only (2) and (4)). During phase 2, the participants can submit their results for this preliminary scoring dataset through the challenge website to see their scores and rankings on the leaderboard. Approximately 7 image quality metrics will be computed for each case. The methodology used to score the submitted images will be shared in detail via the website. The participants are allowed to submit their results up to 2 times for preliminary scoring.

##### Phase 3 (final scoring phase)
At the start of phase 3, a **final scoring dataset** with 30 cases will be provided. Only input images (2) and sinograms (4) will be shared; Labels will not be shared. The participants will be given 2 weeks to submit their final results. Again, approximately 7 image quality metrics will be computed for each case. The final score and rankings will be announced approximately two weeks later. Only the top 3 will be publicly shared.