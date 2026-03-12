# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

--- New game was not starting new game when hitting. 

--- When guessing lower number than the secret number, hint was giving "lower number" hint rather than giving "higher number" hint. Also When guessing higher number than the secret number, hint was giving "higher" hint rather than giving "lower number" hint.

--- Scoring system was off. Should -5 when the wrong number is guessed regardless of higher or lower number.

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---Used Claude Code
--- Prompt 1: when I click the new game button, does not start a new game. Help me find the bug
--- Claude Suggestions:
"Here's the problem flow:                                                                                                                                            
  1. Game ends (won or lost) → st.session_state.status becomes "won" or "lost"                                                                                        
  2. Player clicks "New Game" → attempts and secret are reset, but status stays "won"/"lost"                                                                          
  3. After st.rerun(), the check at line 140 sees status != "playing" and calls st.stop(), halting the game immediately                                              
  -- The fix is to reset status (and history) in the new_game block:
                                                                                                                             
⏺ The fix adds two missing resets in the new_game block (app.py:134):                                                                                                 

  - st.session_state.status = "playing" — without this, a finished game's "won"/"lost" status persists after clicking New Game, causing st.stop() to fire immediately 
  on rerun
  - st.session_state.history = [] — clears guess history for the new game                                                                                             
  - Also changed random.randint(1, 100) to random.randint(low, high) so the new secret respects the selected difficulty range (was always 1–100 regardless of       
  difficulty)

--- Prompt 2: "When guessing number, hint is giving wrong information. When entered lower number than the secret number, gives lower number hints. When entered higher number than the secret number, gives higher number hints."

-- Looking at check_guess in app.py, the messages are swapped:                                                                                                         
                                                                                                                                                                    
  - guess > secret → returns "Too High" but message says "📈 Go HIGHER!" (should say Go LOWER)                                                                        
  - guess < secret → returns "Too Low" but message says "📉 Go LOWER!" (should say Go HIGHER)   

-- Fixed the bug by swapping messages.

---Prompt 3: when guessing wrong number, scoring is incorrect. Lower or higher, should still -5. 


⏺ Yes, looking at update_score (line 57-60), there's a bug:

  if outcome == "Too High":
      if attempt_number % 2 == 0:
          return current_score + 5  # ← wrong! should be -5
      return current_score - 5

  On even-numbered attempts, a "Too High" guess gives +5 instead of -5. "Too Low" always correctly gives -5, but "Too High" only penalizes on odd attempts.

Update(app.py)
  ⎿  Removed 2 lines
      55          return current_score + points
      56  
      57      if outcome == "Too High":
      58 -        if attempt_number % 2 == 0:                                                                                                                  
      59 -            return current_score + 5                                                                                                                 
      58          return current_score - 5
      59  
      60      if outcome == "Too Low":
  
## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

--- 
I used pytest to run tests. I had AI help me design the tests.
One of the test was to see if game correctly deducts 5 points when guessing high number.
def test_too_high_even_attempt_deducts_5():
    # Even attempt, guess too high → should ALSO lose 5 (not gain 5)
    result = update_score(100, "Too High", 2)
    assert result == 95, f"Expected 95 but got {result} (bug: even attempts were giving +5)"
I initially had problem with running pytest due to directory issue. 
AI was able to detect the error for me and created conftest.py to allow pytest.
Successfully passed 8 tests that was created.

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

streamlit reruns so secret number was kept changing in the original app.
"everytime you move to the next step, streamlit forgets previous steps and reruns from the previous steps to the next step."
Allowing stable scret number:
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
- 

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

- Prompting Strategy, working one at a time, and asking clear specific question
- For testing, I would try to ask to write specific tests.
- AI generated code is great but needs guidance for accurate code generation.
