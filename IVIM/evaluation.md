# Evaluation Metrics

The accuracy of the reconstructed IVIM-dMRI parameters will be evaluated using the following metrics:
* Primary metric: relative Root-mean-square-error (rRMSE) for each of the three IVIM parameters will be computed, averaging the results over the provided validation/testing dataset. Specifically, the RMSE is defined as 


$R = \langle \frac{1}{3} \sum_{i} \sqrt{\frac{\sum_{j} (p_{i,j} - p_{i,j}^*)^2}{\sum_{j} (p_{i,j}^*)^2}} \rangle$


where $i=1,…,3$ is the index of IVIM-dMRI parameters, and $p_{i,j}$ is the $i$ th parameter for pixel $j$. $p_{i,j}^*$ is the ground truth parameter. The summation over $j$ runs over all pixels within the breast region, e.g., excluding background air region. The angular bracket $\langle \cdot \rangle$ denotes average over validation/testing cases. 

* Secondary metrics: We will compute the aforementioned metric $rRMSE$ $R$ for each tissue region of tumor, breast glandular, duct, and vessels to investigate performance of the reconstruction algorithms in clinically relevant regions. As such, the summation over $j$ runs over pixels within the corresponding tissue. 
If needed, the secondary metrics averaged over the four regions will be used to break ties under the primary evaluation metric.
