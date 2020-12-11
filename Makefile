# Makefile
# Group29: Zhiyong Wang, Javairia Raza, Sukhdeep Kaur, and Rachel Wong
# Date: December, 2020
# This driver script completes the exploratory data analysis,
# data cleaning and wrangling, and machine learning analysis 
# of diabetic patient encounter data. Figures of machine learning 
# model analysis and features most predictive of patient readmission 
# are generated in a rendered .html report. This script takes no arguments.
# example usage:
# make all
all : doc/diabetes_final_report.html
# reading in the data
data/raw/dataset_diabetes/diabetic_data.csv : src/download_script1.py
	python src/download_script1.py --local_path=./data/raw --url=https://archive.ics.uci.edu/ml/machine-learning-databases/00296/dataset_diabetes.zip
# processing the data
data/processed/diabetes_clean.csv : data/raw/dataset_diabetes/diabetic_data.csv src/processingdata.py
	python src/processingdata.py --input=data/raw/dataset_diabetes/diabetic_data.csv --output=data/processed
data/processed/diabetes_with_race.csv : data/raw/dataset_diabetes/diabetic_data.csv src/processingdata.py
	python src/processingdata.py --input=data/raw/dataset_diabetes/diabetic_data.csv --output=data/processed
# exploratory data analysis
reports/figures/figure4_numscatter_eda.svg reports/figures/figure1_racedist_eda.svg reports/figures/figure2_numhisttarget_eda.svg reports/figures/figure3_numcattarget_eda.svg : data/processed/diabetes_with_race.csv src/eda2.py
	python src/eda2.py --input="data/raw/dataset_diabetes/diabetic_data.csv;data/processed/diabetes_with_race.csv" --output=reports/figures
# tune model and test the data
reports/figures/script4_classifier_scores.csv reports/figures/script4_confusion_matrix.png reports/figures/script4_ROC_AUC.png reports/figures/script4_coefficients.csv : data/processed/diabetes_clean.csv src/explore_script4.py
	python src/explore_script4.py --input=data/processed/diabetes_clean.csv --output=reports/figures
# render the report
doc/diabetes_final_report.html : doc/diabetes_final_report.Rmd reports/figures/figure1_racedist_eda.svg reports/figures/figure2_numhisttarget_eda.svg reports/figures/figure3_numcattarget_eda.svg reports/figures/script4_classifier_scores.csv reports/figures/script4_confusion_matrix.png reports/figures/script4_ROC_AUC.png reports/figures/script4_coefficients.csv doc/references.bib 
	Rscript -e "rmarkdown::render('doc/diabetes_final_report.Rmd')" 
clean :
	rm -rf data/raw/dataset_diabetes/diabetic_data.csv
	rm -rf data/processed/diabetes_with_race.csv
	rm -rf data/processed/diabetes_clean.csv
	rm -rf reports/figures/*
	rm -rf doc/diabetes_final_report.md doc/diabetes_final_report.html