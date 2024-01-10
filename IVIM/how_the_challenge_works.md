## How the Challenge Works

This challenge consists of three phases:

<ins>Phase I (training and development phase)</ins>: 
Participants will be given access to the simulation codes with a description of the simulation process for generating k-space datasets with a range of b-values from the known tissue microstructural parametric maps. A training dataset including 1000 cases will be provided for the participants to develop reconstruction models. Each case will include 
1.	A series of images with 200×200 pixels to represent known tissue microstructural parametric maps.
2.	An image with 200×200 pixels representing known tissue types of each voxel.
3.	Ground truth noiseless $S(x,y,b)$ images with 200×200 pixels at a series of $b$ values.
4.	Simulated noisy k-space data of complex images with 200×200 pixels at corresponding $b$ values. 
To facilitate the understanding of the dMRI model and our data, we will provide a MATLAB script that performs inverse FT to recover $S(x,y,b)$ from k-space data and then derive tissue parameter maps via pixel-wise data fitting. The script will also include codes to write the results in a specific format for automatic evaluation by the Challenge webpage. 

<ins>Phase II (validation and refinement phase)</ins>: 
Participants will validate their algorithms using provided validation dataset and submit their reconstruction results through the Challenge webpage. The validation dataset will consist of 10 cases, each including noisy k-space data of complex images with 200×200 pixels at corresponding $b$ values. Ground truth of the validation datasets will not be provided. 

After the participants submit their results to the Challenge webpage, the results will be evaluated using predetermined evaluation metrics, and a leaderboard will display the performance of different participants. At this phase, the number of submissions is unlimited.
* Required submission: 
  - Reconstructed tissue microstructure parametric maps for the validation cases, each in the form of a 200×200×3 image. The third dimension corresponds to the three parameters ($f$, $D^*$, and $D_t$).

<ins>Phase III (testing and final scoring phase)</ins>: 
Participants will run their algorithms on provided test dataset and submit their reconstruction results through the Challenge webpage. The test dataset will consist of 100 cases, each including noisy k-space data of complex images with 200×200 pixels at corresponding $b$ values. Ground truth of the test datasets will not be provided. 

After the participants submit their results to the Challenge webpage, the results will be evaluated using predetermined evaluation metrics, and a leaderboard will display the performance of different participants. At this phase, each participant team is allowed a maximum of three submissions. 

Required submission: 

* Reconstructed tissue microstructure parametric maps for the test cases, each in the form of a 200×200×3 image. The third dimension corresponds to the three parameters ($f$, $D^*$, and $D_t$).
* A one-page technical note describing the reconstruction algorithm.
