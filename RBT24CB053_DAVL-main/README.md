# RBT24CB053_davl_project
# davl
#  Food Nutrition Analysis using Machine Learning

##  Project Overview

This project focuses on analyzing a food nutrition dataset using various Machine Learning techniques. It includes data preprocessing, exploratory data analysis (EDA), dimensionality reduction, and implementation of multiple machine learning models. The aim is to extract meaningful insights and compare model performances effectively.

---

##  Objectives

The main objectives of this project are:

* To perform data cleaning and preprocessing on the dataset
* To visualize data using different EDA techniques
* To apply dimensionality reduction techniques like PCA
* To implement machine learning models for prediction
* To compare the performance of different models

---

##  Dataset

The dataset used in this project is:
**Food_Nutrition_Dataset.csv**

It contains nutritional information such as:

* Calories
* Proteins
* Fats
* Carbohydrates
* Other nutritional attributes

---

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* Streamlit

---

##  Features of the Project

###  Data Loading and Preprocessing

* Dataset is loaded and cleaned
* Column names are formatted
* Only relevant numerical data is used
* Missing values are handled

---

###  Exploratory Data Analysis (EDA)

* Correlation Heatmap
* Histogram
* Box Plot
* Scatter Plot

These visualizations help in understanding patterns and relationships in the dataset.

---

### Dimensionality Reduction

* Principal Component Analysis (PCA) is applied
* Helps in reducing feature dimensions and visualizing data

---

### Machine Learning Models

#### 🔹 Regression

* Linear Regression
* Used to predict continuous values

####  Classification

* Logistic Regression
* Decision Tree
* Random Forest

These models are used to classify data into categories.



### Model Evaluation

* Accuracy Score (for classification)
* R² Score (for regression)
* Confusion Matrix
* Model Comparison using bar charts


##  Frontend

A user-friendly interface is built using **Streamlit**, where users can:

* Select target and features
* Choose between regression and classification
* Select machine learning models
* View graphs and results dynamically



##  How to Run the Project

1. Clone the repository

bash
git clone https://github.com/aarya3106/RBT24CB053_DAVL.git

2. Navigate to the project folder

bash
cd RBT24CB053_DAVL


3. Install required libraries

bash
pip install -r requirements.txt


4. Run the Streamlit app

bash
streamlit run app.py

Project Structure

RBT24CB053_DAVL/
│
├── app.py
├── backend.ipynb
├── Food_Nutrition_Dataset.csv
├── README.md
└── templates/


Conclusion

This project successfully demonstrates the application of machine learning techniques on a real-world dataset. It provides insights into data visualization, model building, and performance comparison, making it a useful tool for understanding data analysis workflows.



Author

Aarya Kashikar

