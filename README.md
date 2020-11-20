# Readmission to Hospital Predictor for Diabetic Patients 

# Introduction 

**Question:** Given a patient’s demographic, medication history and management of diabetes during hospital stay, can we predict if they will be readmitted to the hospital or not?

**Type:** Predictive

## Importance:
Due to Covid-19, it is critical to reduce the burden on the healthcare system and prevent readmission rates from increasing to make space for Covid cases. Our predictor aims to look at the diabetes management and diagnosis during a patient’s hospital stay to understand how much this affects their readmission. This will allow us to create and improve patient safety protocols to better manage diabetic patients during their hospital stay to provide effective care and prevent readmission during this critical time.  
This dataset used for this project is initially used by Strack et al (2014) and collected by a third-party data warehouse company in the US. This [dataset](https://archive.ics.uci.edu/ml/datasets/diabetes+130-us+hospitals+for+years+1999-2008#) contains approximately 70,000 unique encounters with diabetic patients from 1999-2008 in 130 hospitals across the United States of America. Research from this collected data was used to assess diabetic care during hospitalization and determine if patients were likely to be readmitted or not. The paper by Strack et al (2014) can be found [here](https://www.hindawi.com/journals/bmri/2014/781670/) and the descriptions for the features can be found [here](https://www.hindawi.com/journals/bmri/2014/781670/tab1/). 

## Features:
There are a total of 55 total features describing the diabetic encounters. There is a mix of categorical, numerical, and binary features so we will be doing the appropriate transformations based on feature type. We will also be removing duplicate values and doing imputation to deal with missing values. From our initial EDA, some of the important features include admission type (emergency, urgent, elective, etc.), age, diagnosis 1 (primary diagnosis), diabetes medications (if there were any diabetic medication prescribed). 

## Our Plan
To answer our predictive question, we plan to use a predictive classification model to determine if they will be readmitted or not. Before building our model, we realized that there was a class imbalance with the multiclass target. To address this, we changed the target column to a binary class (readmitted status to Yes or No). Through the EDA, we have determined that there are certain features that should be dropped including encounter_id, patient number due to all unique values and missing values in majority of the rows for features like payer code, medical speciality, examide, citogliton. We have also discovered that race is not a informative feature because although diabetes effects certain races disproportionately (include citation), the distribution amongst the target is very similar in our dataset. We will be exploring a logistic regression model. 

Please find our EDA here. 

## Dataset Information (should we include?)
This dataset was collected from 1998-2008 among 130 US hospitals and integrated delivery networks. 101,766 unique diabetes patient encounters were collected following these specific criteria:
(1) It is an inpatient encounter (a hospital admission).
(2) It is a diabetic encounter, that is, one during which any kind of diabetes was entered to the system as a diagnosis.
(3) The length of stay was at least 1 day and at most 14 days.
(4) Laboratory tests were performed during the encounter.
(5) Medications were administered during the encounter.

# Citation  
Beata Strack, Jonathan P. DeShazo, Chris Gennings, Juan L. Olmo, Sebastian Ventura, Krzysztof J. Cios, and John N. Clore, “Impact of HbA1c Measurement on Hospital Readmission Rates: Analysis of 70,000 Clinical Database Patient Records,” BioMed Research International, vol. 2014, Article ID 781670, 11 pages, 2014.

# License:
The materials used for this project are under an open access article distributed under the Creative Commons Attribution License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original work is properly cited. If reusing/referencing, please provide a link to this webpage. 
