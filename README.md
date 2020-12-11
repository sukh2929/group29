# Readmission to Hospital Predictor for Diabetic Patients 

# Contributors: 
Javairia Raza, Rachel Wong, Zhiyong Wang, Sukhdeep Kaur

## Introduction 
For this project, we are trying to answer the predictive question: Given a patient’s demographic, medication history and management of diabetes during hospital stay, can we predict if they will be readmitted to the hospital or not?  Analysis with machine learning models will identify features more likely to predict patient readmission. This will be important for management of hospital care for diabetic patients, because it will identify areas where changes can be made to decrease patient readmission and reduce burden on the healthcare system.

## Importance:
Due to Covid-19, it is critical to reduce the burden on the healthcare system and prevent readmission rates from increasing to make space for Covid cases. Our predictor aims to look at the diabetes management and diagnosis during a patient’s hospital stay to understand how much this affects their readmission. This will allow us to create and improve patient safety protocols to better manage diabetic patients during their hospital stay to provide effective care and prevent readmission during this critical time.  
The data are submitted on behalf of the Center for Clinical and Translational Research, Virginia Commonwealth University, a recipient of NIH CTSA grant UL1 TR00058, and a recipient of the CERNER data. This dataset was collected from 1998-2008 among 130 US hospitals and integrated delivery networks. The dataset can be found [here](https://archive.ics.uci.edu/ml/datasets/diabetes+130-us+hospitals+for+years+1999-2008#). Research from this collected data was used to assess diabetic care during hospitalization and determine if patients were likely to be readmitted or not. The paper by Strack et al. (2014) can be found [here](https://www.hindawi.com/journals/bmri/2014/781670/) and the descriptions for the features can be found [here](https://www.hindawi.com/journals/bmri/2014/781670/tab1/). 

## Report 
The final report can be found [here](https://github.com/UBC-MDS/group29/blob/main/doc/diabetes_final_report.Rmd). A pdf version can be found [here](https://github.com/UBC-MDS/group29/blob/main/doc/diabetes_final_report.pdf)

## Usage
There are two suggested ways to run this analysis:

1. Using Docker

*note - the instructions in this section also depends on running this in a unix shell (e.g., terminal or Git Bash)*

To replicate the analysis, install [Docker](https://www.docker.com/get-started). A link to the DockerHub is [here](https://hub.docker.com/repository/docker/rachelywong/group29-dockerfile). Then clone this GitHub repository and run the following command at the command line/terminal from the root directory of this project:

```
docker run --rm -v /$(pwd):/home/group29 rachelywong/group29-dockerfile:v0.3.0 make -C /home/group29 all
```

2. Without using Docker

To reset the repo to a clean state, with no intermediate or results files, run the following command at the command line/terminal from the root directory of this project:

```
docker run --rm -v /$(pwd):/home/group29 rachelywong/group29-dockerfile:v0.3.0 make -C /home/group29 clean
```

To replicate this analysis, clone this repository, install the dependencies below, and run the following code in your terminal from the root directory of this project:

```python
make all
```
To reset the repo to a clean state and re-run the analysis with no intermediate files, run the following code in your terminal from the root directory of this project:

```python
make clean
```

## Dependency Diagram of [Makefile](https://github.com/UBC-MDS/group29/blob/main/Makefile)
![Dependency Diagram](https://github.com/UBC-MDS/group29/blob/main/Makefile.png)

## Dependencies 
* Python 4.8.3 and Python packages:
  * docopt==0.6.2
  * urllib3==1.25.11
  * ChainMap==3.3
  * os==10.15.6
  * tarfile==3.3
  * numpy==1.19.1
  * pandas==1.1.2
  * altair==4.1.0
  * requests==2.24.0
  * zipfile==3.2.0
  * pandas_profiling==2.9.0
  * altair-saver==0.5.0
  * scikit-learn==0.23.2
  * matplotlib==3.3.2
  
  Additional dependencies:
  * npm install -g vega-lite vega-cli canvas
 
* R version 4.89 and R packages:
  * knitr==1.29
  * tidyverse==1.2.3
  * kableExtra==1.3.1

## License:
The materials used for this project are under an open access article distributed under the Creative Commons Attribution License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original work is properly cited. If reusing/referencing, please provide a link to this webpage. 

## References:
Beata Strack, Jonathan P. DeShazo, Chris Gennings, Juan L. Olmo, Sebastian Ventura, Krzysztof J. Cios, and John N. Clore, “Impact of HbA1c Measurement on Hospital Readmission Rates: Analysis of 70,000 Clinical Database Patient Records,” BioMed Research International, vol. 2014, Article ID 781670, 11 pages, 2014.

Dua, Dheeru, and Casey Graff. 2017. “UCI Machine Learning Repository.” University of California, Irvine, School of Information; Computer Sciences. http://archive.ics.uci.edu/ml.
