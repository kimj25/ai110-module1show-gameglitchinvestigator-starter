import sys
from unittest.mock import MagicMock

# Mock streamlit before importing app so module-level st calls don't fail
mock_st = MagicMock()
mock_st.sidebar.selectbox.return_value = "Normal"
mock_st.session_state = MagicMock()
mock_st.columns.return_value = (MagicMock(), MagicMock(), MagicMock())
sys.modules["streamlit"] = mock_st

from app import update_score, check_guess


# --- update_score: Too High ---

def test_too_high_odd_attempt_deducts_5():
    # Odd attempt, guess too high → should lose 5 points
    result = update_score(100, "Too High", 1)
    assert result == 95, f"Expected 95 but got {result}"

def test_too_high_even_attempt_deducts_5():
    # Even attempt, guess too high → should ALSO lose 5 (not gain 5)
    result = update_score(100, "Too High", 2)
    assert result == 95, f"Expected 95 but got {result} (bug: even attempts were giving +5)"

def test_too_high_multiple_attempts_all_deduct():
    # All attempts should consistently deduct 5 for Too High
    score = 100
    for attempt in range(1, 6):
        score = update_score(score, "Too High", attempt)
    assert score == 75, f"Expected 75 after 5 wrong guesses but got {score}"


# --- update_score: Too Low ---

def test_too_low_deducts_5():
    result = update_score(100, "Too Low", 1)
    assert result == 95

def test_too_low_even_attempt_deducts_5():
    result = update_score(100, "Too Low", 2)
    assert result == 95


# --- check_guess: hint messages ---

def test_guess_too_high_says_go_lower():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'LOWER' in hint but got: {message!r}"

def test_guess_too_low_says_go_higher():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'HIGHER' in hint but got: {message!r}"

def test_correct_guess_wins():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message
