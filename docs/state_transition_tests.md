# Behavioral State Transition Tests
*(Argeia – Procrastination States Tests)*

## Section 1 - No Confirmed Pattern does nothing

### Case 1 - Stable with no negative pattern

Given State: Stable

When: No confirmed current pattern

Then: No state change

---

### Case 2 - Drifting with no negative/positive pattern

Given State: Drifting

When: No confirmed current pattern

Then: No state change

---

### Case 3 - Strained with no negative/positive pattern

Given State: Strained

When: No confirmed current pattern

Then: No state change

---

### Case 4 - Disengaged with no positive pattern

Given State: Disengaged

When: No confirmed current pattern

Then: No state change

---

## Section 2 - Unconfirmed Pattern or Weak Pattern do nothing

### Case 1 - Stable with an unconfirmed pattern

Given State: Stable

When: Unconfirmed pattern/Weak Pattern

Then: No state change

---

### Case 2 - Drifting with an unconfirmed pattern

Given State: Drifting

When: Unconfirmed pattern/Weak Pattern

Then: No state change

---

### Case 3 - Strained with an unconfirmed pattern

Given State: Strained

When: Unconfirmed pattern/Weak Pattern

Then: No state change

---

### Case 4 - Disengaged with an unconfirmed pattern

Given State: Disengaged

When: Unconfirmed pattern/Weak Pattern

Then: No state change

---

## Section 3 - Standard Degradation (one step at a time)

### Case 1 - Stable with a Confirmed Negative Pattern

Given State: Stable

When: Confirmed Negative Pattern

Then: Change state to Drifting

---

### Case 2 - Drifting with a Confirmed Negative Pattern

Given State: Drifting

When: Confirmed Negative Pattern

Then: Change state to Strained

---

### Case 3 - Strained with a Confirmed Negative Pattern

Given State: Strained

When: Confirmed Negative Pattern

Then: Change state to Disengaged

---

### Case 4 - Disengaged with a Confirmed Negative Pattern

Given State: Disengaged

When: Confirmed Negative Pattern

Then: No state change

---

## Section 4 - Escalated Degradation

### Case 1 - Stable with Confirmed Severe Degradation Pattern

Given State: Stable

When: Confirmed Severe Degradation Pattern

Then: Strained

---

### Case 2 - Drifting with Confirmed Severe Degradation Pattern

Given State: Drifting

When: Confirmed Severe Degradation Pattern

Then: Disengaged

---

### Case 3 - Strained with Confirmed Severe Degradation Pattern

Given State: Strained

When: Confirmed Severe Degradation Pattern

Then: Disengaged

---

### Case 4 - Stable with Confirmed Severe Degradation Pattern can never lead to Disengaged

Given State: Stable

When: Confirmed Severe Degradation Pattern

Then: State must NOT become Disengaged

---

## Section 5 - Recovery is Slow and Earned

### Case 1 - Drifting with a single Positive Signal

Given State: Drifting

When: Single Positive Signal

Then: Drifting

---

### Case 2 - Disengaged with a Confirmed Positive Pattern

Given State: Disengaged

When: Confirmed Positive Pattern

Then: Strained

---

### Case 3 - Strained with a Confirmed Positive Pattern

Given State: Strained

When: Confirmed Positive Pattern

Then: Drifting

---

### Case 4 - Drifting with a Confirmed Positive Pattern

Given State: Drifting

When: Confirmed Positive Pattern

Then: Stable

---

### Case 5 - Stable with a Confirmed Positive Pattern

Given State: Stable

When: Confirmed Positive Pattern

Then: Stable

---

## Section 6 - Symmetry checks

### Case 1 - One good task does NOT undo one bad pattern

Given State: Strained

And: A confirmed negative pattern was previously responsible for degradation

When: A single positive signal occurs

Then: State remains Strained

---

### Case 2 - If it can degrade, it must block recovery

Given State: Drifting

And: A confirmed negative pattern exists in the current window

When: Positive signals are present

Then: Recovery does NOT occur

And: State remains Drifting

---

### Case 3 - Recovery never skips steps

Given State: Disengaged

When: Sustained improvement pattern detected

Then: State becomes Strained

And: State does NOT become Drifting or Stable

---

### Case 4 - Stable cannot over-heal

Given State: Stable

When: Sustained improvement pattern detected

Then: State remains Stable

---

### Case 5 - State cannot change without a pattern (even positively)

Given State: Any state

When: No pattern exists (only isolated signals)

Then: State remains unchanged

---