# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 bullet points. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- The "New Game" button reset the secret and attempts but never reset `status`, so the game stayed in "won" or "lost" state and `st.stop()` blocked play immediately after rerun.
- `st.session_state.attempts` was initialized to `1` instead of `0`, making the "Attempts left" display off by one on the very first load.
- Hard difficulty used a range of `1–50`, which is actually *easier* than Normal's `1–100` — the difficulty levels were in the wrong order.
- `update_score` calculated points as `100 - 10 * (attempt_number + 1)`, so even a first-try win gave 80 points instead of 90 — the `+1` was an off-by-one error.
- The "New Game" handler also forgot to clear `history`, so old guesses carried over into the next game's debug panel.

---

## 2. How did you use AI as a teammate?

- I used Claude Code to do a full audit of all files before touching anything, so I had a complete bug list upfront instead of fixing one thing at a time blindly.
- For each bug, I asked Claude to explain *why* it was wrong, not just what to change — this helped me understand the root cause rather than just copy a fix.
- Claude spotted the Hard mode range issue (`1–50`) by comparing it against the other difficulty values side by side, something easy to miss when reading a single function in isolation.
- I verified each fix by tracing through the logic manually — for the `status` bug, I walked through the rerun sequence step by step to confirm the game would actually restart.

---

## 3. Debugging and testing your fixes

- For the New Game bug, I traced the full rerun flow: button clicked → state reset → `st.rerun()` → script re-executes from top → hits `st.stop()` because `status` was never reset. That trace made the fix obvious.
- For the score bug, I plugged in `attempt_number = 1` and compared `100 - 10 * 1 = 90` vs. `100 - 10 * 2 = 80` to confirm the `+1` was wrong.
- I ran `pytest tests/test_game_logic.py -v` after every change to `logic_utils.py` to catch any regressions immediately.
- Having the Developer Debug Info expander in the app was useful — it let me see `secret`, `attempts`, and `status` live while testing each fix.

---

## 4. What did you learn about Streamlit and state?

- Streamlit reruns the entire script from top to bottom on every user interaction — button click, text input, dropdown change.
- Without `st.session_state`, every rerun would generate a brand new secret number and reset all progress, making the game completely unplayable.
- `st.stop()` immediately halts the rest of the script, so anything placed after it (like the guess form) never renders — order of checks matters.
- State fields like `status`, `history`, and `attempts` all need to be explicitly reset together in the New Game handler, or stale values from the previous game will bleed into the new one.

---

## 5. Looking ahead: your developer habits

- Habit to keep: audit all files before fixing anything — listing every bug first prevents fixing one issue while accidentally introducing another.
- Next time: trace through the full execution flow (not just the changed line) before marking a bug as fixed, as seen with the `status` reset bug.
- AI is useful for catching non-obvious comparisons like difficulty ranges, but I still need to verify the logic myself before accepting a suggestion.
- This project showed that AI-generated code can look complete and run without crashing while still having subtle logic errors that only surface during real use — always review and test before trusting it.
- Writing tests early, even simple ones, would have caught the score formula bug immediately instead of finding it through manual tracing.
