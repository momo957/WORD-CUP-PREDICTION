"""
Main prediction pipeline: combines ELO/Poisson and ML models.
Outputs probabilities for all WC 2026 matches.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np

from src.features import load_teams, build_dataset
from src.elo_model import elo_win_probability, poisson_match_probabilities
from src.ml_model import load_or_train_model, ml_predict, FEATURE_COLS

# Weights for ensemble combination
ELO_WEIGHT = 0.30
POISSON_WEIGHT = 0.25
ML_WEIGHT = 0.45

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
PREDICTIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "predictions")


def run_predictions(fixtures_path=None, teams_path=None, output_path=None):
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(PREDICTIONS_DIR, exist_ok=True)

    # Load data
    teams_path = teams_path or os.path.join(DATA_DIR, "teams_features.csv")
    fixtures_path = fixtures_path or os.path.join(DATA_DIR, "wc2026_fixtures.csv")
    output_path = output_path or os.path.join(PREDICTIONS_DIR, "predictions.csv")

    print("Loading team data...")
    teams_df = load_teams(teams_path)

    print("Loading fixtures...")
    fixtures_df = pd.read_csv(fixtures_path)

    print("Building feature matrix...")
    features_df = build_dataset(fixtures_df, teams_df)

    # ---- ELO probabilities ----
    print("Computing ELO probabilities...")
    elo_probs = []
    for _, row in features_df.iterrows():
        pw1, pd_, pw2 = elo_win_probability(row["elo_t1"], row["elo_t2"])
        elo_probs.append({"elo_win1": pw1, "elo_draw": pd_, "elo_win2": pw2})
    elo_df = pd.DataFrame(elo_probs, index=features_df.index)

    # ---- Poisson probabilities ----
    print("Computing Poisson probabilities...")
    poisson_probs = []
    for _, row in features_df.iterrows():
        pw1, pd_, pw2 = poisson_match_probabilities(row["lambda_t1"], row["lambda_t2"])
        poisson_probs.append({"poi_win1": pw1, "poi_draw": pd_, "poi_win2": pw2})
    poi_df = pd.DataFrame(poisson_probs, index=features_df.index)

    # ---- ML probabilities ----
    print("Training / loading ML model...")
    model_path = os.path.join(MODELS_DIR, "gb_model.pkl")
    model = load_or_train_model(teams_df, model_path)
    ml_df = ml_predict(model, features_df)

    # ---- Ensemble ----
    print("Combining models...")
    results = features_df[["match_id", "team1", "team2", "phase", "group", "date"]].copy()

    results["p_win_team1"] = (
        ELO_WEIGHT * elo_df["elo_win1"]
        + POISSON_WEIGHT * poi_df["poi_win1"]
        + ML_WEIGHT * ml_df["win1"]
    )
    results["p_draw"] = (
        ELO_WEIGHT * elo_df["elo_draw"]
        + POISSON_WEIGHT * poi_df["poi_draw"]
        + ML_WEIGHT * ml_df["draw"]
    )
    results["p_win_team2"] = (
        ELO_WEIGHT * elo_df["elo_win2"]
        + POISSON_WEIGHT * poi_df["poi_win2"]
        + ML_WEIGHT * ml_df["win2"]
    )

    # Normalize to sum to 1
    total = results[["p_win_team1", "p_draw", "p_win_team2"]].sum(axis=1)
    results["p_win_team1"] = (results["p_win_team1"] / total).round(4)
    results["p_draw"] = (results["p_draw"] / total).round(4)
    results["p_win_team2"] = (results["p_win_team2"] / total).round(4)

    # Confidence label
    results["predicted_outcome"] = results.apply(_predict_label, axis=1)
    results["confidence"] = results[["p_win_team1", "p_draw", "p_win_team2"]].max(axis=1)
    results["confidence_level"] = pd.cut(
        results["confidence"],
        bins=[0, 0.45, 0.55, 0.65, 1.0],
        labels=["Incertain", "Modéré", "Probable", "Très probable"]
    )

    # Add ELO and Poisson details
    results["elo_win1"] = elo_df["elo_win1"].round(4)
    results["elo_draw"] = elo_df["elo_draw"].round(4)
    results["elo_win2"] = elo_df["elo_win2"].round(4)
    results["poi_win1"] = poi_df["poi_win1"].round(4)
    results["poi_draw"] = poi_df["poi_draw"].round(4)
    results["poi_win2"] = poi_df["poi_win2"].round(4)
    results["ml_win1"] = ml_df["win1"].round(4)
    results["ml_draw"] = ml_df["draw"].round(4)
    results["ml_win2"] = ml_df["win2"].round(4)

    results.to_csv(output_path, index=False)
    print(f"\nPredictions saved to: {output_path}")
    print(f"Total matches predicted: {len(results)}")

    return results


def _predict_label(row):
    probs = {
        f"Victoire {row['team1']}": row["p_win_team1"],
        "Match nul": row["p_draw"],
        f"Victoire {row['team2']}": row["p_win_team2"],
    }
    return max(probs, key=probs.get)


def print_summary(results: pd.DataFrame, group_filter: str = None):
    if group_filter:
        results = results[results["group"] == group_filter]

    for _, row in results.iterrows():
        print(
            f"[{row['group']}] {row['team1']:20s} vs {row['team2']:20s} | "
            f"W1: {row['p_win_team1']:.1%}  D: {row['p_draw']:.1%}  W2: {row['p_win_team2']:.1%} "
            f"=> {row['predicted_outcome']}  [{row['confidence_level']}]"
        )


if __name__ == "__main__":
    results = run_predictions()
    print("\n" + "="*100)
    print("RÉSULTATS PAR GROUPE")
    print("="*100)
    for grp in sorted(results["group"].unique()):
        print(f"\n--- GROUPE {grp} ---")
        print_summary(results, group_filter=grp)
