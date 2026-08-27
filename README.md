# Password Strength Statistical Evaluator

This project implements a quantifiable, four-step probabilistic framework to estimate password vulnerability. Moving beyond simple qualitative heuristics (like "weak" or "strong"), this tool analyzes character strings using information theory, transition matrices, and statistical hypothesis testing.

## The Four-Step Probabilistic Model

1. **Shannon and Pool Entropy:** Evaluates theoretical keyspace and character diversity. It contrasts standard Shannon entropy (average uncertainty per character) against pool entropy (the overall search space based on utilized character classes)[cite: 1].
2. **Markov Dependencies (Bigrams):** Models human typing biases to determine sequence likelihood[cite: 1]. By training a first-order Markov chain on the `rockyou.txt` leaked credentials dataset, the system calculates the conditional probability of character transitions to identify predictable human patterns[cite: 1].
3. **Geometric Distribution:** Models independent brute-force attacks as Bernoulli trials[cite: 1]. This evaluates the theoretical number of attempts an attacker would need to guess the password with varying degrees of confidence[cite: 1].
4. **Chi-Square Goodness-of-Fit:** Tests for statistical randomness[cite: 1]. This heuristic determines if the characters were selected uniformly or if they heavily deviate toward a recognizable pattern[cite: 1].

## Setup and Execution

**1. Clone the repository**
Ensure you have Python 3 installed. Clone this project to your local machine:
*   `git clone https://github.com/your-username/Password-Strength-Statistical-Model.git`
*   `cd Password-Strength-Statistical-Model`

**2. Download the training corpus**
Due to size constraints, the `rockyou.txt` dictionary is not included. Download it directly into the project directory:
*   **Windows:** `curl.exe -L -o rockyou.txt "https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt"`
*   **Linux / Pop!_OS:** `wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt`

**3. Run the evaluator**
*   Execute `python password_evaluator.py` in your terminal.
*   On its initial run, the script will parse the corpus and serialize a `pretrained_bigram_model.json` file to instantly load the Markov states on future executions.

## Scoring Methodology

The evaluator generates a normalized 0–100 security score based on a weighted heuristic:
*   **Pool Entropy (40%):** Rewards massive theoretical search spaces.
*   **Log-Likelihood (40%):** Rewards highly negative probability scores, indicating true randomness and resistance to dictionary attacks.
*   **Shannon Entropy (20%):** Rewards string diversity.

---
**Author:** Henrik Sebastian 
**License:** MIT
