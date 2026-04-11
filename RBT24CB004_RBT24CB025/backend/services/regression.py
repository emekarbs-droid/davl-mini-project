import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split
import plotly.express as px
import plotly.graph_objects as go
import json

def perform_regression(df_scaled: pd.DataFrame, target_col: str) -> dict:
    try:
        if target_col not in df_scaled.columns:
            return {"error": f"Target column '{target_col}' not found in the processed data."}
            
        X = df_scaled.drop(columns=[target_col])
        y = df_scaled[target_col]
        
        if X.empty:
            return {"error": "No features available for regression."}
            
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Ridge regression
        model = Ridge(alpha=1.0)
        model.fit(X_train, y_train)
        
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
        
        from backend.services.evaluation import evaluate_model
        metrics = evaluate_model(y_train, y_train_pred, y_test, y_test_pred)
        
        # Actual vs Predicted plot
        fig_actual_pred = px.scatter(
            x=y_test, y=y_test_pred, 
            labels={'x': 'Actual', 'y': 'Predicted'},
            title="Actual vs Predicted (Test Set)"
        )
        fig_actual_pred.add_shape(
            type="line", line=dict(dash="dash"),
            x0=float(y.min()), y0=float(y.min()), x1=float(y.max()), y1=float(y.max())
        )
        
        # Residual plot
        residuals = y_test - y_test_pred
        fig_residuals = px.scatter(
            x=y_test_pred, y=residuals,
            labels={'x': 'Predicted', 'y': 'Residuals'},
            title="Residual Plot"
        )
        fig_residuals.add_hline(y=0, line_dash="dash", line_color="red")
        
        return {
            "metrics": metrics,
            "actual_vs_predicted": json.loads(fig_actual_pred.to_json()),
            "residual_plot": json.loads(fig_residuals.to_json())
        }
    except Exception as e:
        return {"error": str(e)}
