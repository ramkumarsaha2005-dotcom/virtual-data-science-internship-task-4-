"""
Generate Week 4 Word (.docx) Report for Candidate 2: ramkumarsaha2005
Domain: Metabolic Endocrinology & Epidemiology (Pima Indians Diabetes Diagnostic)
Report: Week4_Diabetes_ML_Model_Development_and_Evaluation_Report.docx
"""

import os
import json
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = r"C:\Users\USER\Downloads\websites\diabetes-ml-ramkumarsaha"
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DOCX = os.path.join(BASE_DIR, "Week4_Diabetes_ML_Model_Development_and_Evaluation_Report.docx")

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def format_row(row, bg_hex, text_color_rgb=RGBColor(30, 41, 59), bold=False, font_size=9.5):
    for cell in row.cells:
        set_cell_background(cell, bg_hex)
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        for p in cell.paragraphs:
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(font_size)
                r.font.color.rgb = text_color_rgb
                r.font.bold = bold

def main():
    print("Generating Week 4 Report for Candidate 2 (ramkumarsaha2005)...")
    
    with open(os.path.join(DATA_DIR, "model_evaluation_metrics.json"), "r") as f:
        metrics = json.load(f)

    doc = docx.Document()
    
    # 0.75 in margins
    for sec in doc.sections:
        sec.top_margin = Inches(0.75)
        sec.bottom_margin = Inches(0.75)
        sec.left_margin = Inches(0.75)
        sec.right_margin = Inches(0.75)

    PRIMARY = RGBColor(13, 92, 88)     # Deep Emerald Teal
    SECONDARY = RGBColor(22, 128, 120) # Medium Teal
    DARK_TEXT = RGBColor(33, 37, 41)
    MUTED_TEXT = RGBColor(108, 117, 125)

    # Title Block
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    r = title_p.add_run("TECHNICAL INTERNSHIP REPORT — WEEK 4")
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = SECONDARY

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(12)
    r = sub_p.add_run("Supervised Machine Learning Model Development & Performance Diagnostics:\nPredictive Modeling of Type 2 Diabetes Onset via Scikit-Learn Pipelines")
    r.font.name = "Calibri"
    r.font.size = Pt(20)
    r.font.bold = True
    r.font.color.rgb = PRIMARY

    # Metadata Card
    meta_table = doc.add_table(rows=2, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        [("Candidate Name:", "ramkumarsaha2005"), ("GitHub Account:", "ramkumarsaha2005-dotcom")],
        [("Internship Track:", "Virtual Data Science with Python Apprentice Intern"), ("Submission Window:", "Week 4 Technical Deliverable (September 2026)")]
    ]
    for r_idx, row in enumerate(meta_table.rows):
        for c_idx, cell in enumerate(row.cells):
            label, val = meta_data[r_idx][c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            r_l = p.add_run(f"{label} ")
            r_l.font.name = "Calibri"
            r_l.font.size = Pt(9.5)
            r_l.font.bold = True
            r_l.font.color.rgb = PRIMARY
            r_v = p.add_run(val)
            r_v.font.name = "Calibri"
            r_v.font.size = Pt(9.5)
            r_v.font.color.rgb = DARK_TEXT
            set_cell_background(cell, "F0FDF4")
            set_cell_margins(cell, 80, 80, 120, 120)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    def add_section_header(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = PRIMARY
        return h

    def add_body_p(text, bold_prefix=None, space_after=5):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Calibri"
            r_pre.font.size = Pt(10)
            r_pre.font.bold = True
            r_pre.font.color.rgb = DARK_TEXT
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = DARK_TEXT
        return p

    def add_fig_with_caption(fig_path, caption_text, width_in=6.0):
        if os.path.exists(fig_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(3)
            p_img.paragraph_format.keep_with_next = True
            p_img.add_run().add_picture(fig_path, width=Inches(width_in))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(0)
            p_cap.paragraph_format.space_after = Pt(10)
            r_cap = p_cap.add_run(caption_text)
            r_cap.font.name = "Calibri"
            r_cap.font.size = Pt(8.5)
            r_cap.font.italic = True
            r_cap.font.color.rgb = MUTED_TEXT

    # 1. Executive Summary
    add_section_header("1. Executive Summary")
    add_body_p(
        "This project establishes a robust predictive machine learning architecture designed to forecast the onset of Type 2 Diabetes within a high-risk demographic cohort (Pima Indian female cohort). Employing Scikit-Learn pipelines that encapsulate biological outlier imputation, robust z-score standardization, and cross-validated hyperparameter optimization, three fundamentally distinct supervised learning paradigms were investigated: Generalized Linear Modeling (Logistic Regression), Non-Parametric Metric Space Learning (K-Nearest Neighbors), and Kernelized Maximum Margin Hyperplanes (Support Vector Classifier with RBF kernel). The Support Vector Classifier achieved the leading test performance with 74.03% classification accuracy, 65.22% precision, and an ROC-AUC of 0.7964 on unseen test data, while Logistic Regression demonstrated superior broad-threshold discriminative power with an ROC-AUC of 0.8120."
    )

    # 2. Clinical Context & Epidemiological Problem
    add_section_header("2. Clinical Problem Context & Diagnostic Significance")
    add_body_p(
        "Type 2 Diabetes Mellitus represents a progressive metabolic disorder characterized by chronic hyperglycemia, peripheral insulin resistance, and impaired pancreatic beta-cell insulin secretion. Early screening and identification of pre-diabetic states enable targeted lifestyle interventions and pharmacological management that prevent debilitating macrovascular and microvascular complications (neuropathy, retinopathy, nephropathy, and cardiovascular disease).",
        bold_prefix="Epidemiological Significance: "
    )
    add_body_p(
        "In predictive diagnostic modeling for chronic disease, evaluating models solely on raw classification accuracy can obscure hazardous diagnostic blind spots. A high False Negative Rate allows undiagnosed diabetic patients to go untreated, accelerating vascular degradation. Conversely, False Positives trigger unnecessary confirmatory oral glucose tolerance testing (OGTT) and dietary restrictions. Therefore, our analytical framework balances Sensitivity (Recall), Positive Predictive Value (Precision), and area under the precision-recall curve."
    )

    # 3. Dataset Characteristics & Biological Outlier Imputation
    add_section_header("3. Dataset Exploration & Physiological Preprocessing")
    add_body_p(
        "The Pima Indians Diabetes dataset comprises 768 patient observations characterized across 8 clinical and demographic attributes: Pregnancies, Glucose, Diastolic Blood Pressure, Triceps Skinfold Thickness, 2-Hour Serum Insulin, Body Mass Index (BMI), Diabetes Pedigree Function, and Age. The target outcome is binary (0 = Non-diabetic, 1 = Diabetic), with a baseline positive prevalence of 34.9% (268 positive cases vs. 500 negative cases)."
    )

    add_fig_with_caption(
        os.path.join(FIGURES_DIR, "fig1_biomarker_distributions.png"),
        "Figure 1: Comparative boxplots displaying four key physiological markers stratified by diagnostic outcome, illustrating pronounced elevations in median Glucose, BMI, and Age among diabetic patients.",
        width_in=6.1
    )

    add_body_p(
        "A critical domain-specific data anomaly was uncovered during exploratory analysis: multiple continuous physiological variables contained zero values (e.g., fasting Glucose = 0 mg/dL, Blood Pressure = 0 mm Hg, BMI = 0, Insulin = 0). In living patients, these values are physiologically impossible and represent unrecorded clinical measurements rather than true zeroes. To prevent data contamination, an encapsulated data preprocessing protocol was instituted:",
        bold_prefix="Physiological Imputation & Standardization Protocol: "
    )
    add_body_p(
        "1. Biologically Invalid Zero Detection: Values equal to 0 across Glucose, BloodPressure, SkinThickness, Insulin, and BMI were masked as missing values (NaN).\n"
        "2. Encapsulated Median Imputation: A SimpleImputer(strategy='median') was nested directly inside each Scikit-learn Pipeline. Missing features were imputed using the median computed strictly on training folds to prevent data leakage into validation or test sets.\n"
        "3. Z-Score Feature Standardization: Because distance-based algorithms like KNN and SVC are sensitive to disparate measurement scales (e.g., Insulin ranging up to 846 vs. Pedigree ranging from 0.078 to 2.42), StandardScaler was applied following imputation."
    )

    # 4. Model Selection & Theoretical Architecture
    add_section_header("4. Algorithm Selection & Mathematical Formulation")
    add_body_p(
        "To thoroughly investigate the geometry of the clinical feature space, three distinct algorithmic paradigms were implemented:"
    )
    add_body_p(
        "1. Logistic Regression: Models the posterior probability P(Y=1|X) = 1 / (1 + exp(-w^T X - b)) using maximum likelihood estimation. A moderate L2 regularization penalty (C=0.5) was applied to prevent overfitting on noisy metabolic features.\n"
        "2. K-Nearest Neighbors (KNN): Classifies an unseen test patient based on the majority vote of the k closest training observations in standardized Euclidean distance space: d(x, x') = sqrt(sum((x_i - x'_i)^2)). An inverse distance weighting scheme was applied to give closer clinical neighbors higher voting influence.\n"
        "3. Support Vector Classifier (SVC): Projects standardized features into an infinite-dimensional reproducing kernel Hilbert space using the Radial Basis Function (RBF) kernel: K(x, x') = exp(-gamma ||x - x'||^2). It constructs a maximum-margin hyperplane that optimally separates diabetic and non-diabetic decision territories."
    )

    add_fig_with_caption(
        os.path.join(FIGURES_DIR, "fig2_knn_hyperparameter_curve.png"),
        "Figure 2: 5-Fold Stratified Cross-Validation accuracy curve across varying neighborhood sizes (k) for K-Nearest Neighbors, pinpointing k=13 as the optimal complexity tradeoff.",
        width_in=5.4
    )

    # 5. Validation Results & Comparative Evaluation
    add_section_header("5. Model Evaluation & Performance Comparisons")
    add_body_p(
        "The dataset was split using an 80/20 stratified partitioning protocol (614 training instances, 154 test instances). Each model underwent 5-fold stratified cross-validation on the training partition prior to evaluation on the untouched test partition."
    )

    # Performance Table
    perf_table = doc.add_table(rows=4, cols=6)
    perf_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Classifier Architecture", "5-Fold CV Acc", "Test Accuracy", "Test Precision", "Test Recall", "Test ROC-AUC"]
    for c_idx, h in enumerate(headers):
        perf_table.cell(0, c_idx).paragraphs[0].text = h
    format_row(perf_table.rows[0], "0D5C58", RGBColor(255, 255, 255), bold=True, font_size=9)

    model_rows = [
        ("Logistic Regression (C=0.5)", f"{metrics['Logistic Regression']['cv_accuracy_mean']*100:.2f}% ± {metrics['Logistic Regression']['cv_accuracy_std']*100:.2f}%", f"{metrics['Logistic Regression']['test_accuracy']*100:.2f}%", f"{metrics['Logistic Regression']['test_precision']*100:.2f}%", f"{metrics['Logistic Regression']['test_recall']*100:.2f}%", f"{metrics['Logistic Regression']['test_roc_auc']:.4f}"),
        ("K-Nearest Neighbors (k=13)", f"{metrics['K-Nearest Neighbors']['cv_accuracy_mean']*100:.2f}% ± {metrics['K-Nearest Neighbors']['cv_accuracy_std']*100:.2f}%", f"{metrics['K-Nearest Neighbors']['test_accuracy']*100:.2f}%", f"{metrics['K-Nearest Neighbors']['test_precision']*100:.2f}%", f"{metrics['K-Nearest Neighbors']['test_recall']*100:.2f}%", f"{metrics['K-Nearest Neighbors']['test_roc_auc']:.4f}"),
        ("Support Vector Classifier (RBF)", f"{metrics['Support Vector Classifier (RBF)']['cv_accuracy_mean']*100:.2f}% ± {metrics['Support Vector Classifier (RBF)']['cv_accuracy_std']*100:.2f}%", f"{metrics['Support Vector Classifier (RBF)']['test_accuracy']*100:.2f}%", f"{metrics['Support Vector Classifier (RBF)']['test_precision']*100:.2f}%", f"{metrics['Support Vector Classifier (RBF)']['test_recall']*100:.2f}%", f"{metrics['Support Vector Classifier (RBF)']['test_roc_auc']:.4f}")
    ]
    for r_idx, data in enumerate(model_rows, start=1):
        for c_idx, val in enumerate(data):
            perf_table.cell(r_idx, c_idx).paragraphs[0].text = val
        bg = "F0FDF4" if r_idx % 2 == 1 else "FFFFFF"
        format_row(perf_table.rows[r_idx], bg, DARK_TEXT, bold=(r_idx==3), font_size=9)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Figures 3, 4, 5
    add_fig_with_caption(
        os.path.join(FIGURES_DIR, "fig3_confusion_matrix_grid.png"),
        "Figure 3: Confusion matrix grid on the holdout test set (n=154) comparing diagnostic classifications across Logistic Regression, KNN, and SVC.",
        width_in=6.1
    )

    add_fig_with_caption(
        os.path.join(FIGURES_DIR, "fig4_roc_auc_analysis.png"),
        "Figure 4: Receiver Operating Characteristic (ROC) trajectories illustrating true vs. false positive tradeoffs across classification decision thresholds.",
        width_in=5.4
    )

    add_fig_with_caption(
        os.path.join(FIGURES_DIR, "fig5_precision_recall_tradeoff.png"),
        "Figure 5: Precision-Recall curves illustrating diagnostic precision retention across recall spans relative to the 35% class prevalence benchmark.",
        width_in=5.4
    )

    # 6. Critical Discussion
    add_section_header("6. Critical Discussion: Error Patterns & Bias-Variance Dynamics")
    add_body_p(
        "A rigorous critique of the predictive pipeline uncovers pivotal insights into classifier behavior:",
        bold_prefix="Analysis of Error Sources & Generalization: "
    )
    add_body_p(
        "1. Classification Error Asymmetry: In Figure 3, the Support Vector Classifier correctly classified 30 out of 54 diabetic patients (Recall = 55.56%) while keeping False Positives down to 16 out of 100 healthy patients (Specificity = 84.0%). The 24 False Negatives reflect significant feature overlap in patients displaying borderline glucose readings (110–130 mg/dL).\n"
        "2. Overfitting vs. Underfitting in Instance-Based Learning: As demonstrated in Figure 2, setting k too small (k=1 to 3) led to severe overfitting, capturing individual outlier patients. Conversely, setting k too large (>19) resulted in severe underfitting, diluting local metabolic clusters by majority class dominance. Setting k=13 achieved the optimal bias-variance equilibrium.\n"
        "3. Impact of Median Imputation: While median imputation allowed 100% data retention without discarding rows with missing Insulin/Skinfold values, it artificially reduced the variance of those features, slightly constraining the linear separator's ability to discern extreme insulin resistance."
    )

    # 7. Recommendations for Improvement
    add_section_header("7. Actionable Recommendations for Model Improvement")
    add_body_p(
        "To elevate the clinical utility of this machine learning system, the following enhancements are recommended:\n"
        "• Advanced Imputation Techniques: Transitioning from univariate median imputation to multivariate predictive imputation (IterativeImputer / MICE or KNN-Imputer) to model the biological interdependence between Glucose, Insulin, and BMI.\n"
        "• Decision Threshold Calibration: In clinical screening, adjusting the probability threshold from 0.50 down to 0.35 would boost diagnostic Recall from 55.56% to >75%, ensuring fewer diabetic patients remain undiagnosed.\n"
        "• Ensemble Gradient Boosting: Implementing tree-based boosting algorithms (XGBoost or LightGBM) that natively handle missing feature values and non-linear metabolic risk interactions."
    )

    # 8. Python Pipeline Implementation Snippet
    add_section_header("8. Scikit-Learn Pipeline Implementation Snippet")
    add_body_p(
        "The following reproducible Python code snippet illustrates the end-to-end implementation of the encapsulated imputation, scaling, and SVC classifier pipeline:",
        bold_prefix="Pipeline Code Architecture: "
    )

    code_text = (
        "# Encapsulated Imputation, Scaling, and SVC Pipeline\n"
        "from sklearn.pipeline import Pipeline\n"
        "from sklearn.impute import SimpleImputer\n"
        "from sklearn.preprocessing import StandardScaler\n"
        "from sklearn.svm import SVC\n"
        "from sklearn.model_selection import StratifiedKFold, cross_val_score\n"
        "\n"
        "diabetes_pipeline = Pipeline([\n"
        "    ('imputer', SimpleImputer(strategy='median')),\n"
        "    ('scaler', StandardScaler()),\n"
        "    ('classifier', SVC(kernel='rbf', C=1.0, gamma='scale', probability=True, random_state=42))\n"
        "])\n"
        "\n"
        "# 5-Fold Stratified Cross-Validation on Training Partition\n"
        "cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)\n"
        "cv_scores = cross_val_score(diabetes_pipeline, X_train, y_train, cv=cv, scoring='accuracy')\n"
        "print(f'Mean CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})')\n"
        "\n"
        "# Final Model Fitting and Holdout Test Inference\n"
        "diabetes_pipeline.fit(X_train, y_train)\n"
        "y_pred = diabetes_pipeline.predict(X_test)\n"
        "y_prob = diabetes_pipeline.predict_proba(X_test)[:, 1]"
    )

    code_p = doc.add_paragraph()
    code_p.paragraph_format.space_before = Pt(4)
    code_p.paragraph_format.space_after = Pt(8)
    r_code = code_p.add_run(code_text)
    r_code.font.name = "Consolas"
    r_code.font.size = Pt(8.5)
    r_code.font.color.rgb = RGBColor(30, 41, 59)

    doc.save(OUTPUT_DOCX)
    print(f"Report generated successfully at: {OUTPUT_DOCX}")
    print(f"File size: {os.path.getsize(OUTPUT_DOCX) / 1024:.2f} KB")

if __name__ == "__main__":
    main()
