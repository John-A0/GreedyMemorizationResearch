# 🛡️ Greedy Memorization Creates Security Risks  
### Static Malware Detection Using Ensemble Learning on PE Metadata

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![ML](https://img.shields.io/badge/Machine%20Learning-Ensemble-orange)
![Security](https://img.shields.io/badge/Cybersecurity-Malware%20Detection-red)
![Status](https://img.shields.io/badge/Research-Academic-success)

---

## 📌 Abstract

Signature-based detection systems often fail against modern obfuscation techniques.  
This research evaluates four ensemble learning algorithms for **static malware detection**
using only **Portable Executable (PE) header metadata**.

Although all models achieve >99.6% accuracy, we demonstrate that they are highly
vulnerable to **adversarial mimicry attacks**, where malware copies benign metadata
to bypass detection. This exposes a critical limitation of metadata-based static analysis.

---

## 🎯 Research Objectives

- Compare ensemble learning models on PE metadata
- Analyze operational trade-offs (False Positives vs False Negatives)
- Investigate feature importance concentration
- Test robustness using adversarial header manipulation

---

## 🧪 Models Evaluated

| Algorithm | Paradigm |
|--------|--------|
| Random Forest | Bagging |
| XGBoost | Boosting |
| LightGBM | Boosting |
| Histogram Gradient Boosting | Boosting |

---

## 📊 Dataset

- **Total samples:** 34,054 Windows PE executables  
- **Benign:** 18,626  
- **Malware:** 15,428  
- **Features:** 54 PE header attributes  
- **Extraction:** `pefile` Python library  
- **Split:** 80% Train / 20% Test  

### Feature Categories

- Linker versions
- OS versions
- Entry point
- Image base
- Section alignment
- Checksum
- Structural header values

---

## ⚙️ Experimental Setup

- Libraries:
  - `scikit-learn`
  - `xgboost`
  - `lightgbm`
  - `pefile`
- Metrics:
  - Accuracy
  - Precision
  - Recall
  - False Positives (FP)
  - False Negatives (FN)
- Feature importance analysis performed for all models

---

## ✅ Results Summary

All models exceed **99.6% accuracy** on clean test data.

| Model | Accuracy | FP | FN |
|--------|--------|----|----|
| HistGradientBoosting | **99.80%** | **6** | 8 |
| XGBoost | 99.78% | 8 | 7 |
| LightGBM | 99.75% | 7 | 10 |
| Random Forest | 99.65% | 19 | **5** |

### Operational Insights

- **HistGradientBoosting** → best for user-facing systems (lowest FP)
- **Random Forest** → best for backend detection (lowest FN)

---

## ⚠️ Feature Importance Risk

Boosting models rely heavily on **single metadata features**, especially:

- `Minor Linker Version`

This creates a **Single Point of Failure** where modifying only one field can bypass
detection. Random Forest distributes importance across multiple features, offering
better structural stability.

---

## 🧨 Adversarial Mimicry Attack

### Attack Method

1. Select malware sample detected by all models
2. Modify only PE header metadata
3. Copy linker version values from `calc.exe`
4. Keep malicious payload unchanged

### Results

All models misclassified malware as benign:

| Model | Prediction | Confidence |
|--------|-----------|--------|
| HistGradientBoosting | Benign | 99.6% |
| LightGBM | Benign | 99.3% |
| XGBoost | Benign | 97.9% |
| Random Forest | Benign | 62% |

➡️ Random Forest showed uncertainty but still failed.

---

## ⚠️ Case Study — AnyDesk False Positive

The legitimate remote tool **AnyDesk.exe** was classified as malware due to:

- Outdated linker versions
- High entropy from compression

This highlights that metadata-only models detect **structural obfuscation patterns**, which
may overlap between malware and legitimate privacy tools.

---

## 🧠 Conclusion

Metadata-based ensemble learning provides:

- ⚡ High-speed scanning
- 📈 Excellent benchmark accuracy

But also:

- ❌ Extremely weak adversarial robustness

### ✅ Recommended Deployment

Use these models strictly as:

> 🚦 **High-speed pre-filtering layer**

Must be combined with:

- Byte-level N-gram analysis
- Import Address Table hashing
- Dynamic sandbox analysis

for final verdicts in high-security environments.

---

## ▶️ How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
