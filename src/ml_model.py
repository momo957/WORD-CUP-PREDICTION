"""ML model for match outcome prediction (team1 win / draw / team2 win)."""
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

FEATURE_COLS = [
    "elo_diff", "fifa_rank_diff", "wc_participations_diff",
    "best_wc_result_diff", "last_wc_stage_diff", "top5_players_diff",
    "avg_goals_scored_diff", "avg_goals_conceded_diff", "recent_goal_diff_diff",
    "win_pct_diff", "clean_sheets_diff", "win_vs_top20_diff",
    "continental_titles_diff", "conf_weight_diff",
    "coach_years_diff",
    "is_host_t1", "is_host_t2",
]


def generate_synthetic_training_data(teams_df: pd.DataFrame, n_samples: int = 5000,
                                      seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic training data from team features.
    Outcome is derived from ELO difference + noise, giving realistic label distribution.
    """
    rng = np.random.default_rng(seed)
    team_list = list(teams_df.index)
    rows = []

    from src.features import build_match_features
    from src.elo_model import elo_win_probability

    for _ in range(n_samples):
        t1, t2 = rng.choice(team_list, size=2, replace=False)
        feats = build_match_features(t1, t2, teams_df)

        pw1, pd_, pw2 = elo_win_probability(feats["elo_t1"], feats["elo_t2"])
        # Sample an outcome from these probabilities
        outcome = rng.choice(["win1", "draw", "win2"], p=[pw1, pd_, pw2])

        row = {col: feats[col] for col in FEATURE_COLS}
        row["outcome"] = outcome
        rows.append(row)

    return pd.DataFrame(rows)


def train_model(teams_df: pd.DataFrame, model_path: str = None):
    """Train gradient boosting model on synthetic + ELO-derived labels."""
    df = generate_synthetic_training_data(teams_df, n_samples=8000)

    X = df[FEATURE_COLS].values
    y = df["outcome"].values

    model = GradientBoostingClassifier(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=4,
        subsample=0.8,
        random_state=42,
    )
    model.fit(X, y)

    if model_path:
        joblib.dump(model, model_path)
    return model


def load_or_train_model(teams_df: pd.DataFrame, model_path: str):
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return train_model(teams_df, model_path)


def ml_predict(model, features_df: pd.DataFrame) -> pd.DataFrame:
    """Return probability matrix [p_win1, p_draw, p_win2] for each match."""
    X = features_df[FEATURE_COLS].values
    classes = list(model.classes_)
    proba = model.predict_proba(X)

    result = pd.DataFrame(proba, columns=classes, index=features_df.index)
    # Ensure column order is consistent
    for col in ["win1", "draw", "win2"]:
        if col not in result.columns:
            result[col] = 0.0
    return result[["win1", "draw", "win2"]]
