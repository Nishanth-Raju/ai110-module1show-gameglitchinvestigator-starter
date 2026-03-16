from logic_utils import check_guess, get_range_for_difficulty, update_score, parse_guess


# --- check_guess ---


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# --- get_range_for_difficulty ---
# Bug: Hard was returning (1, 50), which is easier than Normal's (1, 100)


def test_hard_range_is_wider_than_normal():
    # Hard should cover a bigger range than Normal, not smaller
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high


def test_hard_range_returns_correct_values():
    # Regression: was (1, 50) before the fix
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 500


def test_easy_range_returns_correct_values():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20


def test_normal_range_returns_correct_values():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100


# --- update_score ---
# Bug: formula used (attempt_number + 1), costing an extra 10 pts per win


def test_win_on_first_attempt_scores_90():
    # Regression: was giving 80 due to the +1 bug
    score = update_score(current_score=0, outcome="Win", attempt_number=1)
    assert score == 90


def test_win_on_second_attempt_scores_80():
    score = update_score(current_score=0, outcome="Win", attempt_number=2)
    assert score == 80


def test_win_score_never_below_10():
    # Even with many attempts, minimum win reward is 10
    score = update_score(current_score=0, outcome="Win", attempt_number=100)
    assert score == 10


def test_wrong_guess_deducts_5_points():
    score = update_score(current_score=50, outcome="Too High", attempt_number=3)
    assert score == 45


def test_wrong_guess_too_low_deducts_5_points():
    score = update_score(current_score=50, outcome="Too Low", attempt_number=3)
    assert score == 45


# --- parse_guess ---


def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_empty_string_returns_error():
    ok, value, err = parse_guess("")
    assert ok is False
    assert err is not None


def test_parse_non_number_returns_error():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert err is not None


def test_parse_decimal_truncates_to_int():
    # Decimal inputs are accepted and truncated, not rejected
    ok, value, err = parse_guess("7.9")
    assert ok is True
    assert value == 7
