"""Feature engineering for match prediction."""
import pandas as pd
import numpy as np


BEST_RESULT_MAP = {
    "Winner": 7,
    "Runner_up": 6,
    "3rd_place": 5,
    "4th": 4.5,
    "QF": 4,
    "R16": 3,
    "SF": 5,
    "Group_Stage": 1,
    "Never": 0,
}

CONTINENTAL_TITLES_WEIGHT = {
    "UEFA": 1.0,
    "CONMEBOL": 1.0,
    "CAF": 0.85,
    "AFC": 0.80,
    "CONCACAF": 0.80,
    "OFC": 0.60,
}


def load_teams(teams_path: str) -> pd.DataFrame:
    df = pd.read_csv(teams_path)
    df["best_wc_result_score"] = df["best_wc_result"].map(BEST_RESULT_MAP).fillna(1)
    df["last_wc_stage_score"] = df["last_wc_stage"].map(BEST_RESULT_MAP).fillna(1)
    df["conf_weight"] = df["confederation"].map(CONTINENTAL_TITLES_WEIGHT).fillna(0.75)
    return df.set_index("team")


def build_match_features(team1: str, team2: str, teams_df: pd.DataFrame,
                          is_neutral: bool = True) -> dict:
    """Build feature vector for a single match."""
    t1 = teams_df.loc[team1]
    t2 = teams_df.loc[team2]

    # Host advantage factor
    host_elo_bonus = 0
    if t1.get("is_host", 0) == 1:
        host_elo_bonus = 80
    elif t2.get("is_host", 0) == 1:
        host_elo_bonus = -80

    features = {
        # ELO & ranking
        "elo_diff": (t1["elo_rating"] + host_elo_bonus) - t2["elo_rating"],
        "fifa_rank_diff": t2["fifa_rank"] - t1["fifa_rank"],  # positive = t1 better ranked

        # WC pedigree
        "wc_participations_diff": t1["wc_participations"] - t2["wc_participations"],
        "best_wc_result_diff": t1["best_wc_result_score"] - t2["best_wc_result_score"],
        "last_wc_stage_diff": t1["last_wc_stage_score"] - t2["last_wc_stage_score"],

        # Squad quality
        "top5_players_diff": t1["players_top5_leagues"] - t2["players_top5_leagues"],

        # Recent form
        "avg_goals_scored_diff": t1["avg_goals_scored"] - t2["avg_goals_scored"],
        "avg_goals_conceded_diff": t1["avg_goals_conceded"] - t2["avg_goals_conceded"],
        "recent_goal_diff_diff": t1["recent_goal_diff"] - t2["recent_goal_diff"],
        "win_pct_diff": t1["win_pct_last10"] - t2["win_pct_last10"],
        "clean_sheets_diff": t1["clean_sheets_last10"] - t2["clean_sheets_last10"],

        # Strength of schedule
        "win_vs_top20_diff": t1["win_pct_vs_top20"] - t2["win_pct_vs_top20"],

        # Continental strength
        "continental_titles_diff": t1["continental_titles"] - t2["continental_titles"],
        "conf_weight_diff": t1["conf_weight"] - t2["conf_weight"],

        # Coach stability
        "coach_years_diff": t1["coach_years"] - t2["coach_years"],

        # Context
        "is_host_t1": int(t1.get("is_host", 0)),
        "is_host_t2": int(t2.get("is_host", 0)),

        # Raw values for Poisson model
        "lambda_t1": (t1["avg_goals_scored"] + t2["avg_goals_conceded"]) / 2,
        "lambda_t2": (t2["avg_goals_scored"] + t1["avg_goals_conceded"]) / 2,
        "elo_t1": t1["elo_rating"] + host_elo_bonus,
        "elo_t2": t2["elo_rating"],
    }
    return features


def build_dataset(fixtures_df: pd.DataFrame, teams_df: pd.DataFrame) -> pd.DataFrame:
    """Build feature matrix for all fixtures."""
    rows = []
    for _, row in fixtures_df.iterrows():
        t1, t2 = row["team1"], row["team2"]
        if t1 not in teams_df.index or t2 not in teams_df.index:
            continue
        feats = build_match_features(t1, t2, teams_df)
        feats["match_id"] = row["match_id"]
        feats["team1"] = t1
        feats["team2"] = t2
        feats["phase"] = row.get("phase", "Group")
        feats["group"] = row.get("group", "")
        feats["date"] = row.get("date", "")
        rows.append(feats)
    return pd.DataFrame(rows)
