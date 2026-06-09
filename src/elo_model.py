"""ELO-based match outcome probability model."""
import numpy as np


def expected_score(elo_a, elo_b):
    """Expected score for team A against team B."""
    return 1 / (1 + 10 ** ((elo_b - elo_a) / 400))


def elo_win_probability(elo_a, elo_b, home_advantage=0):
    """
    Returns (p_win_a, p_draw, p_win_b) using ELO ratings.
    Draw probability estimated via a draw tendency factor.
    """
    elo_a_adj = elo_a + home_advantage
    exp_a = expected_score(elo_a_adj, elo_b)

    # Bradley-Terry model with draw zone
    draw_factor = 0.22  # baseline draw probability in football
    p_win_a_raw = exp_a
    p_win_b_raw = 1 - exp_a

    # Scale to leave room for draws
    p_win_a = p_win_a_raw * (1 - draw_factor)
    p_win_b = p_win_b_raw * (1 - draw_factor)

    # Draw more likely when teams are close
    elo_diff = abs(elo_a_adj - elo_b)
    draw_adj = draw_factor * np.exp(-elo_diff / 300)
    extra = draw_factor - draw_adj

    p_win_a += extra * p_win_a_raw
    p_win_b += extra * p_win_b_raw
    p_draw = draw_adj

    return p_win_a, p_draw, p_win_b


def poisson_match_probabilities(lambda_a, lambda_b, max_goals=8):
    """
    Given expected goals for each team, compute win/draw/loss probabilities
    using independent Poisson distributions.
    """
    from scipy.stats import poisson

    goals_range = np.arange(0, max_goals + 1)
    p_win_a = p_draw = p_win_b = 0.0

    for i in goals_range:
        for j in goals_range:
            p = poisson.pmf(i, lambda_a) * poisson.pmf(j, lambda_b)
            if i > j:
                p_win_a += p
            elif i == j:
                p_draw += p
            else:
                p_win_b += p

    return p_win_a, p_draw, p_win_b
