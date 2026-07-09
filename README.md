# 2006_Groeneveld_CriticalHeatFlux_LUT and assorted correlations
- An Excel implementation of the 2006 Groeneveld Critical Heat Flux Look Up Table
- A .txt based Matlab implementation of the 2006 Groeneveld Critical Heat Flux Look Up Table
- A python based implementation using SDF
- Additional assorted correlations


## .xlsm method
- May need to enable [ActiveX controls](https://support.microsoft.com/en-us/office/activex-controls-are-disabled-by-default-in-microsoft-365-and-office-2024-9cae60f8-478c-42c6-978c-eca072525d64)
    - `File>Options>Trust Center>ActiveX Settings>Prompt me before enabling all controls with minimal restrictions`
    - Select `Ok`.
- May need to [Unblock](https://support.microsoft.com/en-us/topic/a-potentially-dangerous-macro-has-been-blocked-0952faa0-37e7-4316-b61d-5b5ed6024216) the file:
    - Right-click the .xlsm file and go to Properties>General.
    - At the bottom tick the `Unblock` option.
    - Select `Ok`.
 
# Sources
- 2006 CHF LUT:
    ```
    @article{GROENEVELD20071909,
    title = {The 2006 CHF look-up table},
    journal = {Nuclear Engineering and Design},
    volume = {237},
    number = {15},
    pages = {1909-1922},
    year = {2007},
    note = {NURETH-11},
    issn = {0029-5493},
    doi = {https://doi.org/10.1016/j.nucengdes.2007.02.014},
    url = {https://www.sciencedirect.com/science/article/pii/S0029549307002002},
    author = {D.C. Groeneveld and J.Q. Shan and A.Z. Vasić and L.K.H. Leung and A. Durmayaz and J. Yang and S.C. Cheng and A. Tanase},
    }
    ```
- 2001 Film Boiling Coefficient LUT
    - *Note that this paper ONLY inlcudes a section of the table. It links to a now defunct URL for the full table: [http://www.magma.ca/∼thermal/](http://www.magma.ca/∼thermal/). Contact the authors or their associated university (University of Ottawa’s Department of Mechanical Engineering) if you need the original table source.*
    ```
    @article{GROENEVELD200383,
    title = {A look-up table for fully developed film-boiling heat transfer},
    journal = {Nuclear Engineering and Design},
    volume = {225},
    number = {1},
    pages = {83-97},
    year = {2003},
    issn = {0029-5493},
    doi = {https://doi.org/10.1016/S0029-5493(03)00149-3},
    url = {https://www.sciencedirect.com/science/article/pii/S0029549303001493},
    author = {D.C. Groeneveld and L.K.H. Leung and A.Z. Vasic’ and Y.J. Guo and S.C. Cheng},
    }
    ```
