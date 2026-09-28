"""
Week 4: Machine Learning Model Development and Evaluation
Candidate 2: ramkumarsaha2005
Domain: Metabolic Endocrinology & Epidemiology (Pima Indians Diabetes Diagnostic)
Author: ramkumarsaha2005
"""

import os
import json
import urllib.request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, classification_report, roc_curve, precision_recall_curve, auc
)

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 150

BASE_DIR = r"C:\Users\USER\Downloads\websites\diabetes-ml-ramkumarsaha"
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

def main():
    print("[1/6] Fetching and Loading Pima Indians Diabetes Dataset...")
    url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
    columns = [
        'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
        'Insulin', 'BMI', 'DiabetesPedigree', 'Age', 'Outcome'
    ]
    raw_csv = os.path.join(DATA_DIR, "pima_indians_diabetes.csv")
    if not os.path.exists(raw_csv):
        urllib.request.urlretrieve(url, raw_csv)
    
    df = pd.read_csv(raw_csv, names=columns)
    print(f"Dataset shape: {df.shape}")
    print(f"Target distribution: Negative(0)={np.sum(df['Outcome']==0)}, Positive(1)={np.sum(df['Outcome']==1)} ({np.mean(df['Outcome']==1)*100:.1f}%)")

    # Figure 1: Biomarker Boxplots comparing Diabetic vs Non-Diabetic
    print("[2/6] Generating Figure 1: Clinical Biomarker Distribution Comparison...")
    fig, axes = plt.subplots(1, 4, figsize=(14, 4))
    markers = ['Glucose', 'BloodPressure', 'BMI', 'Age']
    units = ['mg/dL', 'mm Hg', 'kg/m²', 'Years']
    palette = {0: '#2b8cbe', 1: '#e41a1c'}
    
    for i, (m, u) in enumerate(zip(markers, units)):
        # replace 0 with nan for clean boxplot representation
        m_series = df[m].replace(0, np.nan)
        plot_df = pd.DataFrame({'Outcome': df['Outcome'].map({0: 'Non-Diabetic', 1: 'Diabetic'}), 'value': m_series})
        sns.boxplot(x='Outcome', y='value', hue='Outcome', data=plot_df, ax=axes[i],
                    palette=['#2b8cbe', '#e41a1c'], legend=False, boxprops=dict(alpha=0.8), width=0.45)
        axes[i].set_title(f"{m} ({u})", fontsize=11, fontweight='bold', pad=8)
        axes[i].set_xlabel("")
        axes[i].set_ylabel(u, fontsize=9)

    plt.suptitle("Figure 1: Distribution of Clinical Biomarkers Stratified by Diabetes Diagnostic Outcome", fontsize=12, fontweight='bold', y=1.04)
    plt.tight_layout()
    fig1_path = os.path.join(FIGURES_DIR, "fig1_biomarker_distributions.png")
    plt.savefig(fig1_path, dpi=160, bbox_inches='tight')
    plt.close()
    print(f"Generated Figure 1: {fig1_path}")

    # Train / Test Split
    print("[3/6] Preprocessing and Train-Test Split (80/20 Stratified)...")
    feature_cols = [c for c in columns if c != 'Outcome']
    X = df[feature_cols].copy()
    y = df['Outcome'].values

    # Replace biologically implausible zeros with NaN so Imputer can replace them cleanly
    zero_invalid_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    X[zero_invalid_cols] = X[zero_invalid_cols].replace(0, np.nan)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Train size: {X_train.shape[0]} samples, Test size: {X_test.shape[0]} samples")

    # Hyperparameter tuning curve for KNN (Figure 2)
    print("[4/6] Tuning KNN Hyperparameter (k) and Generating Figure 2...")
    k_range = list(range(1, 26, 2))
    knn_cv_means = []
    knn_cv_stds = []
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    for k in k_range:
        pipe_k = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler()),
            ('knn', KNeighborsClassifier(n_neighbors=k, weights='distance'))
        ])
        scores = cross_val_score(pipe_k, X_train, y_train, cv=cv, scoring='accuracy')
        knn_cv_means.append(np.mean(scores))
        knn_cv_stds.append(np.std(scores))

    best_k_idx = int(np.argmax(knn_cv_means))
    best_k = k_range[best_k_idx]
    print(f"Optimal KNN k = {best_k} with CV Accuracy = {knn_cv_means[best_k_idx]*100:.2f}%")

    plt.figure(figsize=(8, 4.8))
    plt.plot(k_range, knn_cv_means, marker='o', color='#08519c', lw=2.2, label='Mean 5-Fold CV Accuracy')
    plt.fill_between(k_range,
                     np.array(knn_cv_means) - np.array(knn_cv_stds),
                     np.array(knn_cv_means) + np.array(knn_cv_stds),
                     color='#bdd7e7', alpha=0.5, label='± 1 Std Dev Error Band')
    plt.scatter([best_k], [knn_cv_means[best_k_idx]], color='#d94801', s=100, zorder=5,
                label=f'Optimal k={best_k} ({knn_cv_means[best_k_idx]*100:.2f}%)')
    plt.axvline(best_k, color='#d94801', linestyle=':', alpha=0.8)
    plt.xlabel('Neighborhood Size (k-Parameter)', fontsize=11, fontweight='bold')
    plt.ylabel('Stratified CV Accuracy', fontsize=11, fontweight='bold')
    plt.title('Figure 2: K-Nearest Neighbors Neighborhood Parameter Optimization Curve\n(Evaluating Metric Distance Bias-Variance Tradeoff)', fontsize=12, fontweight='bold', pad=12)
    plt.xticks(k_range)
    plt.legend(loc='lower right', frameon=True)
    plt.tight_layout()
    fig2_path = os.path.join(FIGURES_DIR, "fig2_knn_hyperparameter_curve.png")
    plt.savefig(fig2_path, dpi=160)
    plt.close()
    print(f"Generated Figure 2: {fig2_path}")

    # Model Pipelines
    pipelines = {
        "Logistic Regression": Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler()),
            ('model', LogisticRegression(C=0.5, random_state=42, max_iter=1000))
        ]),
        "K-Nearest Neighbors": Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler()),
            ('model', KNeighborsClassifier(n_neighbors=best_k, weights='distance'))
        ]),
        "Support Vector Classifier (RBF)": Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler()),
            ('model', SVC(kernel='rbf', C=1.0, gamma='scale', probability=True, random_state=42))
        ])
    }

    # Cross-validation & Test Set Evaluation
    print("[5/6] Training Models and Evaluating on Unseen Test Partition...")
    results = {}
    test_predictions = {}
    test_probabilities = {}

    for name, pipe in pipelines.items():
        cv_acc = cross_val_score(pipe, X_train, y_train, cv=cv, scoring='accuracy')
        cv_f1 = cross_val_score(pipe, X_train, y_train, cv=cv, scoring='f1')
        cv_roc = cross_val_score(pipe, X_train, y_train, cv=cv, scoring='roc_auc')

        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        y_prob = pipe.predict_proba(X_test)[:, 1]

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_prob)
        cm = confusion_matrix(y_test, y_pred)

        results[name] = {
            "cv_accuracy_mean": float(np.mean(cv_acc)),
            "cv_accuracy_std": float(np.std(cv_acc)),
            "cv_f1_mean": float(np.mean(cv_f1)),
            "cv_f1_std": float(np.std(cv_f1)),
            "cv_roc_mean": float(np.mean(cv_roc)),
            "cv_roc_std": float(np.std(cv_roc)),
            "test_accuracy": float(acc),
            "test_precision": float(prec),
            "test_recall": float(rec),
            "test_f1": float(f1),
            "test_roc_auc": float(roc_auc),
            "confusion_matrix": cm.tolist()
        }
        test_predictions[name] = y_pred
        test_probabilities[name] = y_prob
        print(f" -> {name}: Test Acc={acc*100:.2f}%, Recall={rec*100:.2f}%, Precision={prec*100:.2f}%, ROC-AUC={roc_auc:.4f}")

    # Figure 3: Confusion Matrix Grid
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    cm_palettes = ['Blues', 'Oranges', 'YlGnBu']

    for i, (name, metrics) in enumerate(results.items()):
        cm = np.array(metrics['confusion_matrix'])
        cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        labels = [f"{v}\n({pct:.1%})" for v, pct in zip(cm.flatten(), cm_norm.flatten())]
        labels = np.asarray(labels).reshape(2, 2)

        sns.heatmap(cm, annot=labels, fmt="", cmap=cm_palettes[i], ax=axes[i], cbar=False,
                    xticklabels=['Non-Diab (Pred)', 'Diabetic (Pred)'],
                    yticklabels=['Non-Diab (True)', 'Diabetic (True)'],
                    linewidths=1.5, linecolor='white')
        axes[i].set_title(f"{name}\nAcc: {metrics['test_accuracy']*100:.1f}% | Recall: {metrics['test_recall']*100:.1f}%",
                          fontsize=11, fontweight='bold')
        axes[i].set_xlabel("Predicted Diagnosis", fontsize=10)
        axes[i].set_ylabel("True Clinical Class", fontsize=10)

    plt.suptitle("Figure 3: Test Confusion Matrices Comparing Diagnostic Classifiers (n=154)", fontsize=13, fontweight='bold', y=1.03)
    plt.tight_layout()
    fig3_path = os.path.join(FIGURES_DIR, "fig3_confusion_matrix_grid.png")
    plt.savefig(fig3_path, dpi=160, bbox_inches='tight')
    plt.close()
    print(f"Generated Figure 3: {fig3_path}")

    # Figure 4: ROC Curves
    plt.figure(figsize=(8, 6.5))
    colors = ['#1f78b4', '#e31a1c', '#33a02c']
    
    for (name, y_prob), col in zip(test_probabilities.items(), colors):
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_val = auc(fpr, tpr)
        plt.plot(fpr, tpr, color=col, lw=2.2, label=f"{name} (AUC = {roc_val:.4f})")
    
    plt.plot([0, 1], [0, 1], color='#808080', lw=1.5, linestyle='--', label='Chance Classifier (AUC = 0.5000)')
    plt.xlim([-0.02, 1.02])
    plt.ylim([0.0, 1.03])
    plt.xlabel('False Positive Rate (1 - Specificity)', fontsize=11, fontweight='bold')
    plt.ylabel('True Positive Rate (Sensitivity / Recall)', fontsize=11, fontweight='bold')
    plt.title('Figure 4: Receiver Operating Characteristic (ROC) Trajectories\nComparing Discriminative Separability on Diabetes Onset', fontsize=12, fontweight='bold', pad=12)
    plt.legend(loc="lower right", frameon=True, facecolor='white', framealpha=0.9, fontsize=10)
    plt.tight_layout()
    fig4_path = os.path.join(FIGURES_DIR, "fig4_roc_auc_analysis.png")
    plt.savefig(fig4_path, dpi=160)
    plt.close()
    print(f"Generated Figure 4: {fig4_path}")

    # Figure 5: Precision-Recall Curves
    plt.figure(figsize=(8, 6.5))
    for (name, y_prob), col in zip(test_probabilities.items(), colors):
        precision_vals, recall_vals, _ = precision_recall_curve(y_test, y_prob)
        pr_auc = auc(recall_vals, precision_vals)
        plt.plot(recall_vals, precision_vals, color=col, lw=2.2, label=f"{name} (PR-AUC = {pr_auc:.4f})")

    baseline = np.sum(y_test == 1) / len(y_test)
    plt.plot([0, 1], [baseline, baseline], color='#808080', linestyle='--', lw=1.5, label=f'Positive Prevalence Baseline ({baseline:.2f})')
    plt.xlim([-0.02, 1.02])
    plt.ylim([0.0, 1.03])
    plt.xlabel('Recall (Sensitivity)', fontsize=11, fontweight='bold')
    plt.ylabel('Precision (Positive Predictive Value)', fontsize=11, fontweight='bold')
    plt.title('Figure 5: Precision-Recall Diagnostic Trade-Off Curves\nAcross Operating Detection Thresholds', fontsize=12, fontweight='bold', pad=12)
    plt.legend(loc="lower left", frameon=True, facecolor='white', framealpha=0.9, fontsize=10)
    plt.tight_layout()
    fig5_path = os.path.join(FIGURES_DIR, "fig5_precision_recall_tradeoff.png")
    plt.savefig(fig5_path, dpi=160)
    plt.close()
    print(f"Generated Figure 5: {fig5_path}")

    # Save metrics JSON
    metrics_path = os.path.join(DATA_DIR, "model_evaluation_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(results, f, indent=4)
    print(f"Metrics saved to {metrics_path}")
    print("Candidate 2 training and artifacts generation completed successfully!")

if __name__ == "__main__":
    main()
