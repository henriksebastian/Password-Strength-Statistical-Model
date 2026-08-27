import os
import sys
import math
import json
import random
from collections import Counter, defaultdict

# ---------------------------------------------------------
# A. Shannon and Pool Entropy
# ---------------------------------------------------------
def shannon_entropy(password: str) -> float:
    n = len(password)
    counts = Counter(password)
    probs = [c / n for c in counts.values()]
    return -sum(p * math.log2(p) for p in probs)

def pool_entropy(password: str) -> float:
    pool = 0
    if any(c.islower() for c in password): pool += 26
    if any(c.isupper() for c in password): pool += 26
    if any(c.isdigit() for c in password): pool += 10
    if any(not c.isalnum() for c in password): pool += 33
    pool = max(pool, 1)
    return len(password) * math.log2(pool)

# ---------------------------------------------------------
# B. Bigram Markov Model (Conditional Probability)
# ---------------------------------------------------------
def build_bigram_model(corpus):
    transition_counts = defaultdict(Counter)
    for pw in corpus:
        for a, b in zip(pw, pw[1:]):
            transition_counts[a][b] += 1
    model = {}
    for a, counter in transition_counts.items():
        total = sum(counter.values())
        model[a] = {b: c / total for b, c in counter.items()}
    return model

def sequence_likelihood(password, model, default_prob=1e-4):
    log_p = 0.0
    for a, b in zip(password, password[1:]):
        p = model.get(a, {}).get(b, default_prob)
        log_p += math.log2(p)
    return log_p

# ---------------------------------------------------------
# C. Geometric Distribution CDF & D. Chi-Square Test
# ---------------------------------------------------------
def chi_square_uniform_test(password: str):
    counts = Counter(password)
    n = len(password)
    k = len(counts)
    if k <= 1:
        return float('inf'), 0
    expected = n / k
    chi2 = sum((o - expected)**2 / expected for o in counts.values())
    dof = k - 1
    return chi2, dof

# ---------------------------------------------------------
# E. Model Pretraining & Persistence
# ---------------------------------------------------------
MODEL_FILE = "pretrained_bigram_model.json"

def get_or_train_model(corpus_filepath="rockyou.txt", sample_size=500000):
    if os.path.exists(MODEL_FILE):
        print(f"Loading pretrained model from '{MODEL_FILE}'...")
        with open(MODEL_FILE, 'r') as f:
            return json.load(f)
            
    print(f"Pretrained model not found. Training on {sample_size:,} passwords from '{corpus_filepath}'...")
    try:
        with open(corpus_filepath, 'r', encoding='latin-1') as f:
            corpus = f.read().splitlines()
            
        sampled_corpus = random.sample(corpus, min(sample_size, len(corpus)))
        model = build_bigram_model(sampled_corpus)
        
        with open(MODEL_FILE, 'w') as f:
            json.dump(model, f)
            
        print(f"Model trained and saved to '{MODEL_FILE}'.")
        return model
        
    except FileNotFoundError:
        print(f"\nError: '{corpus_filepath}' not found.")
        print("Please ensure the dataset is in the same directory.")
        sys.exit(1)

# ---------------------------------------------------------
# F. Quantitative Scoring Model
# ---------------------------------------------------------
def calculate_score(h_shannon, h_pool, log_lik):
    """Calculates a normalized score (0-100) using a weighted model of the metrics."""
    
    # 1. Normalize Pool Entropy (Max 40 points): ~100 bits is considered highly secure
    score_pool = min((h_pool / 100.0) * 40.0, 40.0)
    
    # 2. Normalize Log-Likelihood (Max 40 points): highly negative (~-150) indicates true randomness
    score_log = min((abs(log_lik) / 150.0) * 40.0, 40.0)
    
    # 3. Normalize Shannon Entropy (Max 20 points): ~4.5 bits is excellent character diversity
    score_shannon = min((h_shannon / 4.5) * 20.0, 20.0)
    
    # Sum the weights and ensure it stays strictly within the 0-100 bounds
    total = score_pool + score_log + score_shannon
    return min(max(int(total), 0), 100)

# ---------------------------------------------------------
# G. Interactive CLI
# ---------------------------------------------------------
def main():
    print("--- Password Strength Evaluator ---")
    rockyou_model = get_or_train_model('rockyou.txt')
    
    print("\nReady for input.")
    print("-" * 35)
    
    while True:
        try:
            pwd = input("\nEnter a password to test: ")
            if not pwd:
                continue
                
            h_shannon = shannon_entropy(pwd)
            h_pool = pool_entropy(pwd)
            log_lik = sequence_likelihood(pwd, rockyou_model)
            chi2, _ = chi_square_uniform_test(pwd)
            
            # Generate the 0-100 score
            final_score = calculate_score(h_shannon, h_pool, log_lik)
            
            print(f"\n  Shannon Entropy:  {h_shannon:.3f} bits")
            print(f"  Pool Entropy:     {h_pool:.3f} bits")
            print(f"  Log-Likelihood:   {log_lik:.3f}")
            print(f"  Chi-Square Stat:  {chi2:.3f}")
            print(f"  =================================")
            print(f"  OVERALL SCORE:    {final_score} / 100")
            print(f"  =================================")
            
            # Explicit prompt to continue or break the loop
            choice = input("\nTest another password? (y/n): ").strip().lower()
            if choice != 'y':
                print("Exiting program. Goodbye!")
                break
            
        except KeyboardInterrupt:
            print("\nExiting program. Goodbye!")
            break

if __name__ == "__main__":
    main()