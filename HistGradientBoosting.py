import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.inspection import permutation_importance
import joblib
import numpy as np

df = pd.read_csv("C:/Users/JOHN/Downloads/archive(1)/PE_Dataset_Labeled.csv") 

drop_cols = ['Unnamed: 0', 'File_Name', 'DLLs', 'Functions', 'Sections', 'Label']
X = df.drop(columns=drop_cols, errors='ignore') 
y = df['Label'] 

y = y.map({'Benign': 0, 'Malware': 1})
y = y.fillna(1).astype(int) 

def clean_hex(value):
    try:
        if isinstance(value, str) and value.startswith('0x'):
            return int(value, 16)
        return float(value)
    except:
        return 0 

for col in X.columns:
    if X[col].dtype == 'object':
        X[col] = X[col].apply(clean_hex)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training the HistGradientBoosting Model...")
model = HistGradientBoostingClassifier(
    max_iter=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42,
    early_stopping=True,
    validation_fraction=0.1,
    verbose=0
)
model.fit(X_train, y_train)

print("Testing...")
preds = model.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, preds) * 100:.2f}%")
print("\nDetailed Report:\n", classification_report(y_test, preds))

print("\nCalculating feature importances...")
result = permutation_importance(
    model, X_test, y_test, 
    n_repeats=10, 
    random_state=42,
    n_jobs=-1
)

feature_importances = pd.Series(
    result.importances_mean, 
    index=X.columns
)

print("\nTop 10 Features detecting Malware:")
print(feature_importances.nlargest(10))

plt.figure(figsize=(6, 5))
cm = confusion_matrix(y_test, preds)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.title('Confusion Matrix - HistGradientBoosting')
plt.xlabel('Predicted (0=Benign, 1=Malware)')
plt.ylabel('Actual')
plt.show()


plt.figure(figsize=(10, 6))
feat_importances = feature_importances.nlargest(15)
feat_importances.plot(kind='barh', color='steelblue')
plt.title('Top 15 Features for Malware Detection - HistGradientBoosting')
plt.xlabel('Permutation Importance Score')
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.show()

joblib.dump(model, 'hist_gradient_boosting_malware_model.pkl')
model_columns = list(X.columns)
joblib.dump(model_columns, 'hist_gradient_boosting_model_columns.pkl')

print("\nHistGradientBoosting Model Saved Successfully")