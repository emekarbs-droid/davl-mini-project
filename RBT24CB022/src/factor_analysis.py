"""
DAVL — Factor Analysis Module
Bartlett's test, KMO, optimal factors, scree plot, loadings, rotation, communalities.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# ---------- Compatibility shim for scikit-learn >= 1.8 ----------
# factor_analyzer 0.5.1 passes the removed `force_all_finite` kwarg to
# sklearn.utils.validation.check_array.  We intercept it and translate to
# the replacement `ensure_all_finite` parameter.
import sklearn.utils.validation as _skl_validation

_original_check_array = _skl_validation.check_array


def _patched_check_array(*args, **kwargs):
    if "force_all_finite" in kwargs:
        val = kwargs.pop("force_all_finite")
        kwargs.setdefault("ensure_all_finite", val)
    return _original_check_array(*args, **kwargs)


_skl_validation.check_array = _patched_check_array
# -----------------------------------------------------------------

try:
    from factor_analyzer import FactorAnalyzer
    from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo
    import factor_analyzer.factor_analyzer as _fa_module

    # Patch check_array directly in the factor_analyzer module namespace,
    # since it uses `from sklearn.utils.validation import check_array`
    # which copies the original reference before our module-level patch.
    if hasattr(_fa_module, "check_array"):
        _fa_module.check_array = _patched_check_array

    FACTOR_AVAILABLE = True
except ImportError:
    FACTOR_AVAILABLE = False


def can_apply_factor_analysis(df: pd.DataFrame) -> tuple[bool, str]:
    """Check if factor analysis is applicable."""
    if not FACTOR_AVAILABLE:
        return False, "factor_analyzer package not installed. Run: pip install factor_analyzer"

    numeric_df = df.select_dtypes(include=np.number)
    if numeric_df.shape[1] < 3:
        return False, "Need at least 3 numeric features for factor analysis."

    if numeric_df.shape[0] < numeric_df.shape[1]:
        return False, "Need more observations than features for reliable factor analysis."

    return True, "Factor analysis can be applied."


def run_factor_analysis(df: pd.DataFrame, n_factors: int = None, rotation: str = "varimax") -> dict:
    """
    Run factor analysis with eigenvalue analysis, loadings, and communalities.
    """
    if not FACTOR_AVAILABLE:
        return {"error": "factor_analyzer package not installed."}

    numeric_df = df.select_dtypes(include=np.number)
    numeric_df = numeric_df.dropna(axis=1, how="all")
    numeric_df = numeric_df.fillna(numeric_df.median())

    # Remove zero-variance columns
    numeric_df = numeric_df.loc[:, numeric_df.std() > 0]

    if numeric_df.shape[1] < 3:
        return {"error": "Insufficient numeric features for factor analysis."}

    # Standardize
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numeric_df)
    scaled_df = pd.DataFrame(scaled_data, columns=numeric_df.columns)

    # Bartlett's Test
    try:
        chi_sq, p_value = calculate_bartlett_sphericity(scaled_df)
        bartlett = {
            "chi_square": round(chi_sq, 4),
            "p_value": round(p_value, 6),
            "significant": p_value < 0.05,
        }
    except Exception:
        bartlett = {"chi_square": None, "p_value": None, "significant": None}

    # KMO Test
    try:
        kmo_all, kmo_model = calculate_kmo(scaled_df)
        kmo = {
            "overall": round(kmo_model, 4),
            "per_variable": pd.Series(kmo_all, index=numeric_df.columns).round(4),
            "adequate": kmo_model > 0.6,
        }
    except Exception:
        kmo = {"overall": None, "per_variable": None, "adequate": None}

    # Eigenvalue analysis to determine optimal factors
    try:
        fa_eigen = FactorAnalyzer(rotation=None, n_factors=numeric_df.shape[1], method="principal")
        fa_eigen.fit(scaled_df)
        eigenvalues = fa_eigen.get_eigenvalues()
        ev_original = eigenvalues[0]
        ev_common = eigenvalues[1]

        # Kaiser criterion: eigenvalue > 1
        optimal_factors = int((ev_original > 1).sum())
        optimal_factors = max(1, min(optimal_factors, numeric_df.shape[1] - 1))
    except Exception:
        ev_original = np.array([])
        ev_common = np.array([])
        optimal_factors = min(3, numeric_df.shape[1] - 1)

    if n_factors is None:
        n_factors = optimal_factors

    n_factors = max(1, min(n_factors, numeric_df.shape[1] - 1))

    # Run Factor Analysis
    try:
        fa = FactorAnalyzer(n_factors=n_factors, rotation=rotation, method="principal")
        fa.fit(scaled_df)

        # Factor loadings
        loadings = pd.DataFrame(
            fa.loadings_,
            index=numeric_df.columns,
            columns=[f"Factor {i+1}" for i in range(n_factors)],
        ).round(4)

        # Communalities
        communalities = pd.DataFrame({
            "Variable": numeric_df.columns,
            "Communality": fa.get_communalities().round(4),
            "Uniqueness": (1 - fa.get_communalities()).round(4),
        })

        # Variance explained
        variance = fa.get_factor_variance()
        variance_df = pd.DataFrame({
            "Factor": [f"Factor {i+1}" for i in range(n_factors)],
            "SS Loadings": variance[0].round(4),
            "Proportion Var": (variance[1] * 100).round(2),
            "Cumulative Var": (variance[2] * 100).round(2),
        })

    except Exception as e:
        return {"error": f"Factor analysis failed: {str(e)}"}

    return {
        "bartlett": bartlett,
        "kmo": kmo,
        "eigenvalues": ev_original,
        "optimal_factors": optimal_factors,
        "n_factors": n_factors,
        "loadings": loadings,
        "communalities": communalities,
        "variance": variance_df,
        "rotation": rotation,
        "feature_names": numeric_df.columns.tolist(),
    }
