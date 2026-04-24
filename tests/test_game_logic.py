from logic_utils import check_guess, get_range_for_difficulty, update_score, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_range_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_range_normal():
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_range_hard():
    assert get_range_for_difficulty("Hard") == (1, 50)

def test_range_unknown_defaults():
    assert get_range_for_difficulty("Unknown") == (1, 100)

def test_update_score_win_first_attempt():
    assert update_score(0, "Win", 1) == 90

def test_update_score_win_later_attempt():
    assert update_score(0, "Win", 5) == 50

def test_update_score_win_minimum_points():
    # At attempt 10+, points floor at 10
    assert update_score(0, "Win", 10) == 10

def test_update_score_too_high_deducts():
    assert update_score(50, "Too High", 1) == 45

def test_update_score_too_low_deducts():
    assert update_score(50, "Too Low", 1) == 45

def test_update_score_unknown_outcome_unchanged():
    assert update_score(50, "Unknown", 1) == 50

def test_parse_guess_valid():
    assert parse_guess("42") == (True, 42, None)

def test_parse_guess_decimal_truncates():
    assert parse_guess("3.7") == (True, 3, None)

def test_parse_guess_none():
    assert parse_guess(None) == (False, None, "Enter a guess.")

def test_parse_guess_empty():
    assert parse_guess("") == (False, None, "Enter a guess.")

def test_parse_guess_non_numeric():
    assert parse_guess("abc") == (False, None, "That is not a number.")
