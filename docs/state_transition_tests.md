# Behavioral State Transition Tests
*(Argeia – Procrastination States Tests)*

## Section 1 - No Proposal Does Nothing

### Case 1 - Stable with no proposal of negative kind

Given State: Stable

When: No proposal of any kind

Then: No state change

---

### Case 2 - Drifting with no proposal of negative kind

Given State: Drifting

When: No proposal of any kind

Then: No state change

---

### Case 3 - Strained with no proposal of negative kind

Given State: Strained

When: No proposal of any kind

Then: No state change

---

### Case 4 - Disengaged with no proposal of negative kind

Given State: Disengaged

When: No proposal of any kind

Then: No state change

---


## Section 2 - Standard Degradation (one step at a time)

### Case 1 - Stable with a Proposal of NORMAL severity

Given State: Stable

When: Proposal(kind=DEGRADATION, severity=NORMAL)

Then: Change state to Drifting

---

### Case 2 - Drifting with a Proposal of NORMAL severity

Given State: Drifting

When: Proposal(kind=DEGRADATION, severity=NORMAL)

Then: Change state to Strained

---

### Case 3 - Strained with a Proposal of NORMAL severity

Given State: Strained

When: Proposal(kind=DEGRADATION, severity=NORMAL)

Then: Change state to Disengaged

---

### Case 4 - Disengaged with a Proposal of NORMAL severity

Given State: Disengaged

When: Proposal(kind=DEGRADATION, severity=NORMAL)

Then: No state change

---

## Section 3 - Escalated Degradation

### Case 1 - Stable with a Proposal of SEVERE severity

Given State: Stable

When: Proposal(kind=DEGRADATION, severity=SEVERE)

Then: Strained

---

### Case 2 - Drifting with a Proposal of SEVERE severity

Given State: Drifting

When: Proposal(kind=DEGRADATION, severity=SEVERE)

Then: Disengaged

---

### Case 3 - Strained with a Proposal of SEVERE severity

Given State: Strained

When: Proposal(kind=DEGRADATION, severity=SEVERE)

Then: Disengaged

---

### Case 4 - Stable with a Proposal of SEVERE severity can never lead to Disengaged

Given State: Stable

When: Proposal(kind=DEGRADATION, severity=SEVERE)

Then: State must NOT become Disengaged

---

## Section 4 - Recovery is Slow and Earned

### Case 1 - Disengaged with a Proposal of RECOVERY kind

Given State: Disengaged

When: Proposal of RECOVERY kind

Then: Strained

---

### Case 2 - Strained with a Proposal of RECOVERY kind

Given State: Strained

When: Proposal of RECOVERY kind

Then: Drifting

---

### Case 3 - Drifting with a Proposal of RECOVERY kind

Given State: Drifting

When: Proposal of RECOVERY kind

Then: Stable

---

### Case 4 - Stable with a Proposal of RECOVERY kind

Given State: Stable

When: Proposal of RECOVERY kind

Then: Stable

---

## Section 5 - Symmetry checks

### Case 1 - Recovery never skips steps

Given State: Disengaged

When: Proposal of RECOVERY kind

Then: State becomes Strained

And: State does NOT become Drifting or Stable

---

### Case 2 - Stable cannot over-heal

Given State: Stable

When: Proposal of RECOVERY kind

Then: State remains Stable

---

### Case 3 - State cannot change without a Proposal (even positively)

Given State: Any state

When: No proposal

Then: State remains unchanged

---