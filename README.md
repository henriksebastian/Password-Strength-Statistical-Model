# Password-Strength-Statistical-Model
Overview
This project implements a four-step probabilistic model to quantitatively estimate password vulnerability. Moving beyond basic heuristic checks, this script evaluates cryptographic strength through rigorous statistical analysis. The pipeline measures information content via Shannon entropy, models human typing biases using conditional probabilities (bigrams) trained on real-world data, applies a Geometric distribution to model brute-force attack vectors, and utilizes a Chi-square goodness-of-fit test to check for uniform character distribution.
