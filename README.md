# Greedy Memorization Creates Security Risks: Metadata Overfitting in Malware Detection

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Machine Learning](https://img.shields.io/badge/Library-Scikit--Learn-orange)
![Research](https://img.shields.io/badge/Research-Security-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 📄 Abstract
Static analysis of PE headers is a cornerstone of modern cybersecurity due to its scalability. However, does high accuracy imply robustness? 
This research conducts a comparative analysis of **Random Forest** vs. **Gradient Boosting variants** (XGBoost, LightGBM, HistGradientBoosting) on a balanced dataset of **34,054 Windows executables**. 

**The Shocking Discovery:** While *HistGradientBoosting* achieved the highest baseline accuracy (**99.80%**), we uncovered a critical "Greedy" vulnerability. A simple **"Mimicry Attack"** (disguising malware metadata as `calc.exe`) successfully bypassed **all** models, proving that metadata-based detection is structurally brittle and must be used strictly as a pre-filtering layer.

---

## 📊 Key Results

### 1. Performance vs. Usability Trade-off
We evaluated models based on precision (low false alarms) and recall (security).

| Model | Accuracy | False Positives (FP) | False Negatives (FN) | Verdict |
|-------|----------|----------------------|----------------------|---------|
| **HistGradientBoosting** | **99.80%** | **6** (Lowest) | 8 | Best for **UX** (Minimizes Alert Fatigue) |
| **Random Forest** | 99.65% | 19 | **5** (Lowest) | Best for **Security** (Max Detection) |
| XGBoost | 99.78% | 8 | 7 | Balanced |
| LightGBM | 99.75% | 7 | 10 | Fast Training |

### 2. Feature Importance: The "Greedy" Flaw
Our analysis reveals why Boosting models are vulnerable. They rely heavily on single features (e.g., `Minor_Linker_Version`), creating a **Single Point of Failure**. Random Forest, by contrast, distributes importance democratically.

<p align="center">
  <img src="Images/HIST22.png" width="45%" alt="HistGradient Feature Importance">
  <img src="Images/RF22.png" width="45%" alt="Random Forest Feature Importance">
</p>
<p align="center"><em>Figure 1: Boosting (Left) is greedy & brittle. Random Forest (Right) is distributed & robust.</em></p>

---

## ⚠️ The "Mimicry" Attack (Proof of Concept)
To validate the vulnerability, we performed a **Gray-Box Adversarial Attack**. We took a known malware sample and modified **only** its PE Header metadata (Linker Version, OS Version) to match a legitimate system file (`calc.exe`).

### The Result: Systemic Failure
All models failed to detect the modified malware, but with a crucial difference in confidence:

* **HistGradientBoosting:** Flipped from **Malware** to **Benign** with **99.62% Confidence**. (Complete Deception).
* **Random Forest:** Flipped to **Benign**, but with significantly lower confidence (**62%**).

> **Conclusion:** Metadata models are blind to the "payload" and can be trivially evaded. They must be augmented with content-based inspection (e.g., Byte N-grams).

---

## 📂 Project Structure
