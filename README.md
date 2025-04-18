# PacketSleuth

**AI-Based Detection of Man-in-the-Middle and Tampering (MIMT) Attacks Using Machine Learning**

## Overview

PacketSleuth is a Python-based machine learning pipeline designed to detect Man-in-the-Middle and Tampering (MIMT) attacks in network traffic. It uses the publicly available TON_IoT dataset and a supervised learning approach (Random Forest) to classify traffic as benign or malicious.

---

## Features

- Preprocessing and normalization of raw NetFlow traffic data
- Binary classification of traffic (Benign vs MIMT)
- Random Forest-based detection model
- Performance evaluation using standard metrics
- Modular, script-based architecture
- Prediction on new traffic samples

---

## Dataset

**Source:** [TON_IoT Dataset – UNSW](https://research.unsw.edu.au/projects/toniot-datasets)  
**File Used:** `Train_Test_Network.csv`  
Includes labeled samples for benign traffic and various attack types including MITM and tampering.

---

## File Structure

```
PacketSleuth/
├── data/
│   ├── raw/                 # Raw TON_IoT dataset
│   └── processed/           # (Optional) cleaned data
├── models/                  # Trained model (.pkl)
├── results/                 # Evaluation outputs
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── train_model.py
│   ├── evaluate.py
│   ├── predict.py
│   └── utils.py
├── exploration.ipynb        # EDA (optional)
├── requirements.txt
└── README.md
```

---

## Usage

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the pipeline

```bash
python src/data_loader.py
python src/preprocessing.py
python src/train_model.py
python src/evaluate.py
python src/predict.py --input data/raw/sample.csv
```

---

## Model

- **Algorithm:** Random Forest (Scikit-learn)
- **Target:** Binary classification (0 = Benign, 1 = MIMT)
- **Metrics:** Accuracy, Precision, Recall, F1-score, Confusion Matrix

---

## License

This project is for educational and research purposes only.  
All dataset sources are publicly licensed and credited to UNSW Canberra Cyber.

---

## Author

Nick DeVeau  
