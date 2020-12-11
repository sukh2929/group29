# Readmission to Hospital Predictor for Diabetic Patients 

# Contributors: 
Javairia Raza, Rachel Wong, Zhiyong Wang, Sukhdeep Kaur

## Introduction 
For this project, we are trying to answer the predictive question: Given a patient’s demographic, medication history and management of diabetes during hospital stay, can we predict if they will be readmitted to the hospital or not?  Analysis with machine learning models will identify features more likely to predict patient readmission. This will be important for management of hospital care for diabetic patients, because it will identify areas where changes can be made to decrease patient readmission and reduce burden on the healthcare system.

## Importance:
Due to Covid-19, it is critical to reduce the burden on the healthcare system and prevent readmission rates from increasing to make space for Covid cases. Our predictor aims to look at the diabetes management and diagnosis during a patient’s hospital stay to understand how much this affects their readmission. This will allow us to create and improve patient safety protocols to better manage diabetic patients during their hospital stay to provide effective care and prevent readmission during this critical time.  
The data are submitted on behalf of the Center for Clinical and Translational Research, Virginia Commonwealth University, a recipient of NIH CTSA grant UL1 TR00058, and a recipient of the CERNER data. This dataset was collected from 1998-2008 among 130 US hospitals and integrated delivery networks. The dataset can be found [here](https://archive.ics.uci.edu/ml/datasets/diabetes+130-us+hospitals+for+years+1999-2008#). Research from this collected data was used to assess diabetic care during hospitalization and determine if patients were likely to be readmitted or not. The paper by Strack et al. (2014) can be found [here](https://www.hindawi.com/journals/bmri/2014/781670/) and the descriptions for the features can be found [here](https://www.hindawi.com/journals/bmri/2014/781670/tab1/). 

## Usage
To replicate this analysis, clone this repository, install the dependencies below, and run the following code in your terminal:

```python
python src/download.py --url https://archive.ics.uci.edu/ml/machine-learning-databases/00480/Measurements_Upload_Smaller.zip --local_path=./
```

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
   
## Features:
There are a total of 55 total features describing the diabetic encounters. There is a mix of categorical, numerical, and binary features so we will be doing the appropriate transformations based on feature type. We will also be removing duplicate values and doing imputation to deal with missing values. From our initial EDA, some of the important features are admission type (emergency, urgent, elective, etc.), age, diagnosis 1 (primary diagnosis) and diabetes medications (if there were any diabetic medication prescribed). 

## Selecting the Best Model
There is a mix of categorical, numerical, and binary features for which we will apply proper transformations for use in analysis. There is potential class imbalance based on the target readmitted column having 54864 values of NO, 35545 values of >30, and 11357 values of <30. Class imbalance here was avoided by changing the readmitted column to binary "YES" or "NO" values if the patient was readmitted or not. This would then give us 54864 "NO" values and 46902 "YES" values, and thus avoiding class imbalance. This will also allow us to perform binary-classification rather than multi-classification. We will test RBF SVM and LR models and pick based on best scores which model to proceed with. RBF SVM would be interesting to test since we can change the support vectors with expert knowledge. Insight from the paper suggest a logistic regression model may be most useful for our question, especially with information about feature correlation (weights will be assigned proportionally) and easier to determine informative features. After selecting our final model, we will split the data into 80% training and 20% testing and re-fit the best model on the entire training data set. Next, we will evaluate its performance on the test data set. At this point, we will look at overall accuracy as well as misclassification errors (from the confusion matrix) to assess prediction performance. We will report these values as a table in the final report.

## Exploratory Data Analysis
Before building our model, we have done the exploratory data analysis where we have identified the independence of data, rows having NAs or missing values, drop columns which are irrelevant for prediction, the columns correlation, etc. Additionally, Pandas Profiling was used to generate feature analysis, and any interactions and correlation between the features to assist in data wrangling. EDA analysis will provide us with a table after data wrangling to show dropped features that are not informative to answering our question. A repeated histogram will be generated to compare numerical features compared against each other, highlighting correlation and potential relationships amongst features and the target. Through the EDA, we have determined that there are certain features that should be dropped including encounter_id, patient number due to all unique values and missing values in majority of the rows for features like payer code, medical speciality, examide, citogliton. We have also discovered that race is not a informative feature because although diabetes affects certain races disproportionately, the distribution amongst the target is very similar in our dataset. 

Please find our EDA [here](https://github.com/UBC-MDS/group29/blob/main/reports/EDA/EDA_initial.ipynb).

## Sharing Our Results 
To share the results of our analysis, we plan to generate figures summarizing our results of model performance (tested against a baseline classifier), and evaluation of features most indicative of patient readmission and features most indicative of no patient readmission. Model performance figures will also show hyperparameter optimization, tested against default hyperparameters. With our analysis and results, we hope that our model will be able to predict patient readmission using deployment data in future analysis, and identify areas for change in hospitalization management.

## Citation  
Beata Strack, Jonathan P. DeShazo, Chris Gennings, Juan L. Olmo, Sebastian Ventura, Krzysztof J. Cios, and John N. Clore, “Impact of HbA1c Measurement on Hospital Readmission Rates: Analysis of 70,000 Clinical Database Patient Records,” BioMed Research International, vol. 2014, Article ID 781670, 11 pages, 2014.


## License:
The materials used for this project are under an open access article distributed under the Creative Commons Attribution License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original work is properly cited. If reusing/referencing, please provide a link to this webpage. 
