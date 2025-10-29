#  Naive Bayes Classification Algorithm

---

##  Bayes Theorem

**Formula**:  


\[
P(pass | X) = (P(X | pass) * P(pass))P(X)
\]



Where:  


\[
P(X | C) = P(f_1 | C) * P(f_2 | C) *...........
\]



---

## 📁 Input

**Given**: A path to a CSV file  
**Task**: Read the CSV file using the `pandas` library and create a DataFrame  

Let:  
- \( X \) = test variables (feature1, feature2, ...)  
- \( C \) = [pass, fail]

---

## 🪜 Step-by-Step Procedure

### Step 1: Feature Extraction  
- Create a list of features from the DataFrame  
- Initialize an empty list `P = []`

### Step 2: Prior Probabilities  
- Count the total number of rows for each class in the target feature (e.g., "pass" or "fail")  
- Calculate:  
  - `Pp` → probability of "pass"  
  - `Pf` → probability of "fail"

### Step 3: Conditional Probabilities \( P(X | C) \)  
For each feature in the list of features:
- Create a list of categories in that feature from the DataFrame (e.g., high, medium, low)  
- Append the feature to list `P`  
- For each category in the feature:
  - Count the number of rows where the feature equals the category and the class is "pass"  
  - Divide this count by the total number of rows where the class is "pass"  
  - Store the result in `P[i]`  
- Repeat the same process for the class "fail"

- stores these probilities in a 3d dictionary here 1st index is bivariate and repersent class of target variable rows.keys repersents the rows of the feature sequential order arrival in dataframe and column.keys repersent the category in order of their arrival in the feature.

---

## 🔍 Step 4: Predicting the Class of Test Variable \( X \)

Given a test sample:  


\[
X = \{f_1 = v_1, f_2 = v_2, ..., f_n = v_n\}
\]
test fetures are always given in same order in which they are stored in data frame, value in test variable repersents their category


- Initialize scores:  
  - `score_pass = Pp`  
  - `score_fail = Pf`

- For each feature in the test sample:
  - Find `score_pass` by multiplying probabilty
  - use 2d dictionary to retrive the stored probablity.
  - Multiply probilities these probabilty to get `score_pass`   
  - Multiply `score_pass` by \( P(f_i = v_i | \text{pass}) \)  
  - Multiply `score_fail` by \( P(f_i = v_i | \text{fail}) \)

- Final Prediction:
  - If `score_pass > score_fail`, predict the class as **"pass"**  
  - Otherwise, predict the class as **"fail"**

---

## ✅ Notes

- This algorithm assumes **categorical features** and **independence** between them.
- You can enhance it with **Laplace smoothing** to handle unseen categories.
- Extendable to **multi-class classification** with minimal changes.

---
