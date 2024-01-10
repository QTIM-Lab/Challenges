# IVIM dMRI Model and Challenge Data

Details of the data generation methodology will be provided on the IVIM-dMRI Reconstruction Challenge website (**COMING SOON**).

In IVIM-dMRI, a series of MR images are acquired, each under a diffusion weight $ b $. The MRI signal of each voxel $ S(x, y, b) $ follows a bi-exponential equation as

$ S(x, y, b) = S_0(x, y) \left[ (1 - f(x, y))e^{-D(x,y)b} + f(x, y)e^{-D^*(x,y)b} \right] $

where $ S_0(x, y) $ is signal intensity at $ b = 0 s/mm^2 $. For each diffusion weight, the measured complex k-space data $ g(k_x, k_y, b) $ is related to $ S(x, y, b) $ via the standard Fourier Transform (FT) procedure with noise as

$ g(k_x, k_y, b) = \mathcal{F} $ { $S(x, y, b) $ } $ (k_x, k_y, b) + n(k_x, k_y, b) $

$= \mathcal{F} $ 
{
	$ S_0(x, y) $ 
	$[(1 - f(x, y))e^{-D(x,y)b} + f(x, y)e^{-D^*(x,y)b} ]$
} 
$(k_x, k_y, b) + n(k_x, k_y, b) $, 

where $F$ {$\cdot$}

denotes $FT$ operation, and $n(k_x,k_y,b)$ is an independent and identically distributed (i.i.d.) Gaussian noise. 
In this challenge, participants are given k-space data $g(k_x,k_y,b)$ at a series of known $b$ values, and are tasked to reconstruct images of $f(x,y)$, $D_t(x,y)$, and $D^*(x,y)$. Participants can choose to derive these IVIM parameter maps directly from the k-space data or via a two-step approach that first reconstructs MR images at various $b$ values and then performs pixel-wise data fitting of the IVIM model. 

We generated simulated breast MR images using the VICTRE breast phantom [https://breastphantom.readthedocs.io/en/latest/](https://breastphantom.readthedocs.io/en/latest/). These breast phantom images will depict realistic breast anatomy consisting of various types of normal breast tissues and tumor tissue types demonstrating intratumoral heterogeneity (See the figure). In this figure, (a) depicts tissue compositions with each voxel value being an integer label for illustration purpose. 

<img src="https://qtim-challenges.southcentralus.cloudapp.azure.com:9000/public/ivim/figure_a.jpg" width=400px>

For each tissue type, we assigned known values for $f$, $D^*$ and $D_t$ serving as the gold standard. The values for $f$, $D^*$ and $D_t$ will adhere to the parameters established in prior scientific literature, ensuring their alignment with realistic biological interpretations. Based on the tissue specific MRI properties, we generated the images $S(x,y,b)$. Figure (b-c) shows images at  $b = 0$ and $1000 s/mm2$ in the absence of noise. (d) illustrates the signal decay for a tumor and a tissue voxel. 
Finally, based on the simulated $S(x,y,b)$ at a series of $b$ values, $FT$ was performed for image at each $b$ value and then noise was added, yielding the k-space data available for the reconstruction.
