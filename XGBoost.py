import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import joblib


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

print("Training the XGBoost Model...")
model = XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=6,
    random_state=42,
    eval_metric='logloss'
)
model.fit(X_train, y_train)

print("Testing...")
preds = model.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, preds) * 100:.2f}%")
print("\nDetailed Report:\n", classification_report(y_test, preds))

feature_importances = pd.Series(model.feature_importances_, index=X.columns)
print("\nTop 5 Features detecting Malware:")
print(feature_importances.nlargest(5))

plt.figure(figsize=(6, 5))
cm = confusion_matrix(y_test, preds)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.title('Confusion Matrix - XGBoost')
plt.xlabel('Predicted (0=Benign, 1=Malware)')
plt.ylabel('Actual')
plt.show()

plt.figure(figsize=(10, 6))
feat_importances = pd.Series(model.feature_importances_, index=X.columns)
feat_importances.nlargest(10).plot(kind='barh', color='purple')
plt.title('Top 10 Features for Malware Detection - XGBoost')
plt.xlabel('Importance Score')
plt.show()

joblib.dump(model, 'xgboost_malware_model.pkl')
model_columns = list(X.columns)
joblib.dump(model_columns, 'xgboost_model_columns.pkl')

print("XGBoost Model Saved Successfully")