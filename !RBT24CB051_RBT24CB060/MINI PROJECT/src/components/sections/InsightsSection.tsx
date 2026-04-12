import React from "react";
import { useData } from "@/context/DataContext";

interface Finding {
  tag: string;
  title: string;
  body: React.ReactNode;
  stats: { label: string; value: string }[];
}

interface Improvement {
  priority: "HIGH" | "MED" | "LOW";
  title: string;
  body: string;
  action: string;
}

export const InsightsSection: React.FC = () => {
  const { analysis, fileName } = useData();

  if (!analysis) return <p className="text-muted-foreground">Upload a CSV first.</p>;

  const { correlation, pca, lda, factorAnalysis, regression, classification, target } = analysis;
  const bestModel = classification.models[0];
  const worstModel = classification.models[classification.models.length - 1];
  const accSpread = bestModel.accuracy - worstModel.accuracy;

  const findings: Finding[] = [
    {
      tag: "DATASET SCALE",
      title: "Dataset Overview",
      body: (
        <>The dataset contains <b className="text-foreground">{analysis.totalRows.toLocaleString()}</b> records across <b className="text-foreground">{analysis.totalColumns}</b> columns with <span className="font-mono text-primary">{analysis.totalMissing}</span> missing values.</>
      ),
      stats: [
        { label: "Rows", value: analysis.totalRows.toLocaleString() },
        { label: "Columns", value: analysis.totalColumns.toString() },
        { label: "Missing", value: analysis.totalMissing.toString() },
      ],
    },
    {
      tag: "FEATURE CORRELATION",
      title: "Correlation Analysis",
      body: (
        <>The strongest correlated pair is <b className="text-foreground">{correlation.topPair[0]}</b> and <b className="text-foreground">{correlation.topPair[1]}</b> at <span className="font-mono text-primary">{correlation.topPair[2].toFixed(2)}</span>. Found <span className="font-mono text-primary">{correlation.highCorrCount}</span> highly correlated pairs (|r| &gt; 0.75). Top predictor of target: <b className="text-foreground">{correlation.topPredictorOfTarget[0]}</b> (<span className="font-mono text-primary">{correlation.topPredictorOfTarget[1].toFixed(2)}</span>).</>
      ),
      stats: [
        { label: "Top pair", value: correlation.topPair[2].toFixed(2) },
        { label: "High corrs", value: correlation.highCorrCount.toString() },
        { label: "Top predictor", value: correlation.topPredictorOfTarget[1].toFixed(2) },
      ],
    },
    {
      tag: "DIMENSIONALITY REDUCTION",
      title: "PCA Analysis",
      body: (
        <>The first two principal components explain <span className="font-mono text-primary">{pca.totalVariance.toFixed(1)}%</span> of total variance. PC1 captures <span className="font-mono text-primary">{pca.varianceExplained[0]?.toFixed(1)}%</span> and PC2 captures <span className="font-mono text-primary">{pca.varianceExplained[1]?.toFixed(1)}%</span>.</>
      ),
      stats: [
        { label: "PC1", value: `${pca.varianceExplained[0]?.toFixed(1)}%` },
        { label: "PC2", value: `${pca.varianceExplained[1]?.toFixed(1)}%` },
        { label: "Total", value: `${pca.totalVariance.toFixed(1)}%` },
      ],
    },
    {
      tag: "CLASS SEPARABILITY",
      title: "LDA Results",
      body: (
        <>Linear Discriminant Analysis achieved <span className="font-mono text-primary">{(lda.accuracy * 100).toFixed(1)}%</span> training accuracy. Classes split at mean threshold of target variable. Used <span className="font-mono text-primary">{lda.ldComponents}</span> LD component(s).</>
      ),
      stats: [
        { label: "Accuracy", value: `${(lda.accuracy * 100).toFixed(1)}%` },
        { label: "Components", value: lda.ldComponents.toString() },
      ],
    },
    {
      tag: "LATENT STRUCTURE",
      title: "Factor Analysis",
      body: (
        <>Factor 1 is most loaded on <b className="text-foreground">{factorAnalysis.topFeaturePerFactor[0]?.[0]}</b> (<span className="font-mono text-primary">{factorAnalysis.topFeaturePerFactor[0]?.[1]?.toFixed(2)}</span>). {factorAnalysis.topFeaturePerFactor[1] && <>Factor 2 loads on <b className="text-foreground">{factorAnalysis.topFeaturePerFactor[1][0]}</b> (<span className="font-mono text-primary">{factorAnalysis.topFeaturePerFactor[1][1].toFixed(2)}</span>).</>}</>
      ),
      stats: [
        { label: "F1 top", value: factorAnalysis.topFeaturePerFactor[0]?.[1]?.toFixed(2) || "—" },
        { label: "F2 top", value: factorAnalysis.topFeaturePerFactor[1]?.[1]?.toFixed(2) || "—" },
      ],
    },
    {
      tag: "REGRESSION",
      title: "Regression Performance",
      body: (
        <>Linear regression achieved R² = <span className="font-mono text-primary">{regression.r2.toFixed(3)}</span> with RMSE of <span className="font-mono text-primary">{regression.rmse.toFixed(3)}</span>. Target variable skew: <span className="font-mono text-primary">{target.skew.toFixed(2)}</span>. Fit quality: <b className="text-foreground">{regression.r2 > 0.7 ? "Good" : regression.r2 > 0.4 ? "Moderate" : "Weak"}</b>.</>
      ),
      stats: [
        { label: "R²", value: regression.r2.toFixed(3) },
        { label: "RMSE", value: regression.rmse.toFixed(3) },
        { label: "Skew", value: target.skew.toFixed(2) },
      ],
    },
    {
      tag: "CLASSIFICATION",
      title: "Classification Results",
      body: (
        <>Best model: <b className="text-foreground">{bestModel.name}</b> at <span className="font-mono text-primary">{(bestModel.accuracy * 100).toFixed(1)}%</span> accuracy. Accuracy spread across models: <span className="font-mono text-primary">{(accSpread * 100).toFixed(1)}%</span>. Worst: {worstModel.name} at {(worstModel.accuracy * 100).toFixed(1)}%.</>
      ),
      stats: [
        { label: "Best", value: `${(bestModel.accuracy * 100).toFixed(1)}%` },
        { label: "Spread", value: `${(accSpread * 100).toFixed(1)}%` },
        { label: "Models", value: classification.models.length.toString() },
      ],
    },
  ];

  const improvements: Improvement[] = [];
  if (analysis.totalMissing > 0)
    improvements.push({ priority: "HIGH", title: "Address Missing Data", body: `${analysis.totalMissing} missing values detected. Imputation could improve model performance.`, action: "Use sklearn.impute.KNNImputer" });
  if (correlation.highCorrCount > 0)
    improvements.push({ priority: "HIGH", title: "Remove Redundant Features", body: `${correlation.highCorrCount} highly correlated feature pairs found. Consider dropping collinear features.`, action: "Apply VIF analysis or correlation threshold filtering" });
  if (regression.r2 < 0.6)
    improvements.push({ priority: "HIGH", title: "Upgrade the Regression Model", body: `R² of ${regression.r2.toFixed(3)} indicates weak fit. Consider polynomial features or gradient boosting.`, action: "Try XGBoost or polynomial regression" });
  if (pca.totalVariance < 70)
    improvements.push({ priority: "MED", title: "Extend PCA Components", body: `Only ${pca.totalVariance.toFixed(1)}% variance captured by 2 components. More may be needed.`, action: "Increase n_components in PCA" });
  if (lda.accuracy < 0.75)
    improvements.push({ priority: "MED", title: "Improve Class Boundary Definition", body: `LDA accuracy of ${(lda.accuracy * 100).toFixed(1)}% suggests overlap. Try non-linear methods.`, action: "Use QDA or kernel-based methods" });
  if (accSpread > 0.05)
    improvements.push({ priority: "MED", title: `Tune ${worstModel.name}`, body: `${(accSpread * 100).toFixed(1)}% accuracy gap between models. Hyperparameter tuning could help.`, action: "GridSearchCV with cross-validation" });
  improvements.push({ priority: "MED", title: "Add Ensemble and Boosted Models", body: "Gradient boosting and stacking ensembles often outperform individual classifiers.", action: "Add XGBoost, LightGBM, or stacking" });
  improvements.push({ priority: "LOW", title: "Cross-Validate All Results", body: "Current results use a single train-test split. K-fold cross-validation provides more robust estimates.", action: "Use 5-fold or 10-fold CV" });
  improvements.push({ priority: "LOW", title: "Engineer Targeted Features", body: "Feature engineering based on domain knowledge can significantly improve model performance.", action: "Create interaction terms and polynomial features" });

  const verdict = regression.r2 > 0.7 && bestModel.accuracy > 0.8
    ? "well-structured"
    : regression.r2 > 0.4
      ? "promising but needs refinement"
      : "in early stages";

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <p className="text-xs font-mono text-primary mb-2">◈ Analytical Report · {fileName}</p>
        <h2 className="font-heading text-3xl font-extrabold text-foreground mb-2">
          What your data is telling you
        </h2>
        <p className="text-sm text-muted-foreground max-w-2xl">
          Analysis of {analysis.totalRows.toLocaleString()} records across {analysis.totalColumns} columns from {fileName}.
        </p>
      </div>

      {/* Score chips */}
      <div className="flex flex-wrap gap-3">
        {[
          { label: "R² Score", value: regression.r2.toFixed(3) },
          { label: "PCA Coverage", value: `${pca.totalVariance.toFixed(1)}%` },
          { label: "Best Classifier", value: `${(bestModel.accuracy * 100).toFixed(1)}%` },
          { label: "LDA Accuracy", value: `${(lda.accuracy * 100).toFixed(1)}%` },
          { label: "Records", value: analysis.totalRows.toLocaleString() },
          { label: "Missing", value: analysis.totalMissing.toString() },
        ].map(chip => (
          <div key={chip.label} className="card-surface px-4 py-2.5">
            <p className="font-heading text-lg font-bold text-primary">{chip.value}</p>
            <p className="label-mono mt-0.5">{chip.label}</p>
          </div>
        ))}
      </div>

      {/* Two columns */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Key Findings */}
        <div>
          <h3 className="font-heading text-xl font-bold text-foreground mb-1">Key Findings</h3>
          <p className="label-mono mb-4">Statistical insights from your dataset</p>
          <div className="space-y-4">
            {findings.map((f, idx) => (
              <div
                key={f.tag}
                className="finding-card opacity-0 animate-fade-up"
                style={{ animationDelay: `${idx * 30}ms`, animationFillMode: "forwards" }}
              >
                <span className="pill-badge bg-primary/20 text-primary text-[9px] mb-2 inline-block">{f.tag}</span>
                <h4 className="font-heading text-[15px] font-bold text-foreground mb-1">{f.title}</h4>
                <p className="text-[13px] text-muted-foreground leading-relaxed">{f.body}</p>
                <div className="flex gap-3 mt-3">
                  {f.stats.map(s => (
                    <div key={s.label} className="bg-accent rounded-md px-3 py-1.5">
                      <p className="font-mono text-xs text-foreground">{s.value}</p>
                      <p className="label-mono text-[9px]">{s.label}</p>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Improvements */}
        <div>
          <h3 className="font-heading text-xl font-bold text-foreground mb-1">Areas of Improvement</h3>
          <p className="label-mono mb-4">Recommended next steps</p>
          <div className="space-y-4">
            {improvements.map((imp, idx) => (
              <div
                key={imp.title}
                className={`card-surface p-5 ${imp.priority === "HIGH" ? "priority-high" : imp.priority === "MED" ? "priority-med" : "priority-low"} opacity-0 animate-fade-up`}
                style={{ animationDelay: `${idx * 30}ms`, animationFillMode: "forwards" }}
              >
                <div className="flex items-center gap-2 mb-2">
                  <span className={`pill-badge text-[9px] py-0.5 ${
                    imp.priority === "HIGH" ? "bg-destructive/20 text-destructive" :
                    imp.priority === "MED" ? "bg-[hsl(40,90%,50%)]/20 text-[hsl(40,90%,50%)]" :
                    "bg-success/20 text-success"
                  }`}>
                    {imp.priority}
                  </span>
                  <h4 className="font-heading text-[14px] font-bold text-foreground">{imp.title}</h4>
                </div>
                <p className="text-[13px] text-muted-foreground leading-relaxed">{imp.body}</p>
                <p className="text-[11px] font-mono text-muted-foreground mt-2 flex items-center gap-1.5">
                  <span className="h-1 w-1 rounded-full bg-muted-foreground" />
                  {imp.action}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Verdict */}
      <div className="card-surface border-l-[3px] border-l-primary p-7 bg-accent/50">
        <p className="text-xs font-mono text-primary mb-2">◈ Overall Verdict · {fileName}</p>
        <h3 className="font-heading text-xl font-bold text-foreground mb-2">
          Dataset is {verdict}
        </h3>
        <p className="text-sm text-muted-foreground leading-relaxed max-w-3xl">
          With {analysis.totalRows.toLocaleString()} records and {analysis.totalColumns} features, this dataset 
          achieved an R² of {regression.r2.toFixed(3)} in regression and {(bestModel.accuracy * 100).toFixed(1)}% 
          best classification accuracy ({bestModel.name}). PCA captured {pca.totalVariance.toFixed(1)}% variance 
          in 2 components and LDA separation reached {(lda.accuracy * 100).toFixed(1)}%. 
          {analysis.totalMissing > 0 ? ` There are ${analysis.totalMissing} missing values that should be addressed.` : " The data is clean with no missing values."}
          {correlation.highCorrCount > 0 ? ` ${correlation.highCorrCount} highly correlated feature pair(s) may indicate redundancy.` : ""}
        </p>
      </div>
    </div>
  );
};
