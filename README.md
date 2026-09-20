# Multi-Modal Dish Classifier & Review Intelligence Engine

An end-to-end deep learning pipeline that combines computer vision and natural language processing to analyze food images and reviews together — predicting the dish, the review's sentiment, and whether the image and review actually match (with anomaly detection for mismatched pairs).

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Dataset Strategy](#dataset-strategy)
4. [Tech Stack](#tech-stack)
5. [Project Structure (Notebook Sections)](#project-structure)
6. [Results](#results)
7. [Challenges and Problems Faced](#challenges-and-problems-faced)
8. [Limitations](#limitations)

---

## Project Overview

Given a food photo and a written review, the system:
- Identifies the dish shown in the image (CNN, transfer learning)
- Predicts the sentiment of the review (GRU)
- Approximates a 1-5 star rating from sentiment confidence
- Extracts embeddings from both the image and text
- Fuses these embeddings to predict whether the image and review genuinely describe the same dish
- Flags an anomaly when they don't match, and explains why

This mirrors a real-world use case: automatically catching mislabeled or fraudulent food reviews (e.g., a photo of pizza with a review describing biryani).

---

## Architecture

```
FOOD IMAGE                                    REVIEW TEXT
    |                                              |
    v                                              v
MobileNetV2 (frozen, ImageNet)              Embedding -> GRU (64 units)
    |                                              |
GlobalAveragePooling2D                    Dense(64) "text_embedding"
    |                                              |
Dense(256) -> BatchNorm -> Dropout                |
    |                                              |
Dense(10, softmax) --> Dish Prediction    Dense(1, sigmoid) --> Sentiment Prediction
    |                                              |
[1280-dim image embedding]              [64-dim text embedding]
    |                                              |
[10-dim CNN class probabilities] -+   +--[10-dim dish keyword vector]
                                   |   |
                                   v   v
                    Concatenate (1364-dim fused vector)
                                   |
                        BatchNormalization
                                   |
       Dense(256) -> BatchNorm -> Dropout -> Dense(128) -> BatchNorm -> Dropout
                                   |
                        Dense(64) "fused_representation"
                                   |
                        Dense(1, sigmoid)
                                   |
                Match / Mismatch Prediction (Anomaly Detection)
```

**Design philosophy:** rather than training one giant end-to-end model, we train three specialized models separately (image classifier, text sentiment classifier, fusion classifier) and connect them through extracted embeddings. This is more practical for limited data/compute (Google Colab) and mirrors how real production multi-modal systems are often built.

---

## Dataset Strategy

No single public dataset contains (food image + dish label + matching review + rating + match/anomaly label) together, so this project combines multiple sources and clearly documents what is real versus constructed:

| Data element | Source | Real or Constructed |
|---|---|---|
| Food images (10 classes, 2,500 images) | [Food-101](https://www.tensorflow.org/datasets/catalog/food101) via `tensorflow_datasets` | Real |
| Dish labels | Food-101 | Real |
| Sentiment training text (20,000 reviews) | [Amazon Polarity](https://huggingface.co/datasets/fancyzhx/amazon_polarity) via HuggingFace `datasets` | Real (general product reviews, not food-specific) |
| Dish-specific review text | Custom template generator (tone-consistent, dish-specific vocabulary) | **Constructed** |
| Rating (1-5 stars) | Approximated from sentiment confidence | **Constructed approximation** — no real star-rating labels were available for this pipeline |
| Match / mismatch label | Generated via controlled positive/negative image-review pairing | **Constructed by design** |
| Helpful / verified label | Not implemented | Out of scope for this version |

The 10 selected dish classes: `pizza, sushi, hamburger, ice_cream, samosa, ramen, tacos, waffles, fried_rice, chicken_wings`.

---

## Tech Stack

- **Framework:** TensorFlow / Keras
- **Vision model:** MobileNetV2 (transfer learning, ImageNet-pretrained, frozen base)
- **NLP model:** GRU (Gated Recurrent Unit)
- **Fusion model:** Multi-Layer Perceptron (MLP)
- **Data sources:** `tensorflow_datasets` (Food-101), HuggingFace `datasets` (Amazon Polarity)
- **Evaluation:** scikit-learn (metrics), Matplotlib/Seaborn (visualization)
- **Environment:** Google Colab (GPU-optional, CPU-compatible)

---

## Project Structure

| Section | Purpose |
|---|---|
| 1-3 | Environment setup, dependency fixes, imports |
| 4-7 | Food-101 download, class selection, image saving, stratified split, `tf.data` pipeline |
| 8-10 | CNN (MobileNetV2) training, evaluation, image embedding extraction |
| 11-15 | Review dataset loading, text preprocessing, GRU training, evaluation, text embedding extraction |
| 16-17 | Synthetic dish-review generation, match/mismatch pairing table construction |
| 18-19 | Dish-keyword feature engineering, fused feature extraction |
| 20-21 | Fusion MLP training and evaluation |
| 22-23 | End-to-end prediction function (`analyze_food_review()`), test examples |
| 24 | Model comparison table (image-only vs. text-only vs. fusion) |

---

## Results

| Model | Task | Test Accuracy |
|---|---|---|
| CNN (MobileNetV2) | 10-class dish classification | 83% |
| GRU | Binary sentiment classification | 83% |
| Fusion MLP | Image-review match/mismatch detection | 86% |

**Model comparison (image-only vs. text-only vs. fusion):**

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| Image-Only (keyword alignment) | 0.903 | 0.972 | 0.829 | 0.895 |
| Text-Only (embedding + keyword) | 0.504 | 0.503 | 0.579 | 0.538 |
| **Multi-Modal Fusion** | **0.861** | **0.831** | **0.907** | **0.867** |

**Interpretation:** Text-only performance near chance (50%) confirms that review text alone cannot determine a match without knowing what the image shows — image information is necessary. The Image-Only baseline scores highest because it directly re-applies the same rule used to generate the ground-truth labels, making it closer to a reference ceiling than an independent model. The Fusion model's 86% is the most meaningful result: it learned the image-text alignment relationship purely from data (1,364 numeric features and training examples), without ever being given the comparison rule directly.

---

## Challenges and Problems Faced

This project involved several real debugging episodes, documented here in detail since they represent genuine deep learning engineering problems, not just implementation of a known-working tutorial.

### 1. Dependency conflicts (protobuf / tensorflow_datasets)

**Problem:** `tensorflow_datasets` failed to import with a `VersionError` due to a protobuf gencode/runtime version mismatch in the Colab environment. A first attempt to fix this with `pip install -U protobuf` made things worse, upgrading protobuf to a version (7.x) that broke *other* pre-installed Colab packages (`grpcio-status`, `ydf`, `google-ai-generativelanguage`).

**Fix:** Pinned exact compatible versions (`protobuf==5.29.6`, `tensorflow-metadata==1.17.1`, `tensorflow_datasets==4.9.7`) instead of blindly upgrading, and required a runtime restart afterward since protobuf is loaded into memory once per session.

**Lesson:** Blind `-U` upgrades in a shared, pre-configured environment like Colab can cascade into unrelated breakages; targeted version pinning is safer.

### 2. Missing `importlib_resources` dependency

**Problem:** After fixing the protobuf issue, `tensorflow_datasets` still failed with `ModuleNotFoundError: No module named 'importlib_resources'` — a transitive dependency that wasn't pre-installed.

**Fix:** A simple `pip install importlib_resources` plus a runtime restart.

### 3. Kaggle authentication friction (dataset pivot)

**Problem:** The original plan used the "Amazon Fine Food Reviews" dataset from Kaggle, which requires an API token (`kaggle.json`) uploaded via Colab's file picker. Multiple attempts to generate and upload this token failed — the download button did not produce a locatable file, and `files.upload()` proceeded without a file actually being selected, causing a `FileNotFoundError`.

**Fix:** Pivoted entirely to the `fancyzhx/amazon_polarity` dataset via HuggingFace's `datasets` library, which requires no authentication. This was a deliberate trade-off: real food-specific ratings and helpfulness votes were sacrificed for a frictionless, reliable data source, with this limitation clearly documented rather than hidden.

**Lesson:** When a data-access method introduces disproportionate friction relative to project value, switching sources with transparent trade-off documentation is often more practical than persisting with authentication debugging.

### 4. Renamed HuggingFace dataset repository

**Problem:** `load_dataset("amazon_polarity")` failed with `HfUriError: Repository id must be 'namespace/name'`, because HuggingFace's dataset resolution changed and the dataset had moved under a namespaced owner.

**Fix:** Identified via research that the dataset now lives at `fancyzhx/amazon_polarity` and updated the load call accordingly.

### 5. Silent data leakage from filename collisions

**Problem:** When saving filtered Food-101 images to disk, the image-saving function used a per-class counter that restarted at zero for both the "train" and "validation" source splits (e.g., both producing `pizza_0000.jpg`). Since both were saved to the same folder, validation images silently overwrote training images with matching filenames. This was only caught because a leakage-detection `assert` statement (built proactively per the project's anti-leakage requirements) failed, reporting dozens of overlapping file paths between the train and validation/test splits.

**Fix:** Included the source split name in every saved filename (e.g., `train_pizza_0000.jpg` vs `val_pizza_0000.jpg`), guaranteeing no collisions, then re-verified with the same leakage-detection assertions.

**Lesson:** Proactively building automated leakage checks (rather than trusting the pipeline "should" be correct) is what caught a real, silent correctness bug that would otherwise have invalidated the model's evaluation metrics.

### 6. Notebook-editing artifact: broken f-strings

**Problem:** A long single-line Python f-string, when copied from chat into a Colab cell, occasionally wrapped mid-string due to editor line-wrapping, producing `SyntaxError: unterminated f-string literal`.

**Fix:** Replaced long f-strings with shorter, comma-separated `print()` calls that are immune to line-wrap corruption during copy-paste.

### 7. Vocabulary gap breaking dish-identity signal in text

**Problem:** After building the synthetic dish-review dataset for the fusion task, the fusion model failed to learn at all (stuck at exactly chance-level accuracy, ~50%). Diagnosis revealed that several critical dish names (`ramen`, `samosa`, `tacos`, `wasabi`) never appeared even once in the GRU's real sentiment-training corpus (Amazon Polarity), and others (`sushi`, `hamburger`, `waffles`) appeared too rarely to survive the tokenizer's vocabulary size cutoff. As a result, these words all collapsed into the same generic `<OOV>` (out-of-vocabulary) token — meaning the model had no way to distinguish a review about ramen from a review about samosa at the tokenization level, before the neural network even saw the input.

**Fix (first attempt):** Artificially boosted the frequency of dish-specific words in the tokenizer's fitting corpus, expanding effective vocabulary coverage from 60% to 100% for project-relevant words.

**Further diagnosis:** Even after fixing tokenization, a follow-up sanity check (comparing embedding differences between reviews about different dishes) revealed the *learned* representations for these words were still extremely weak (roughly 20-50x smaller in magnitude than the sentiment signal the GRU was actually trained to detect) — because vocabulary presence alone doesn't force a model to learn meaningful representations; only the training *objective* does, and the sentiment GRU was never asked to distinguish dishes.

**Fix (final):** Rather than continuing to force this through the sentiment GRU, attempted training a dedicated second GRU specifically for dish classification, using synthetically generated, dish-labeled reviews.

### 8. A from-scratch model failing to converge (dead ReLU suspicion)

**Problem:** The dedicated dish-classification GRU (from the fix above) completely failed to learn — loss remained frozen at almost exactly `ln(10) ≈ 2.303` (the theoretical value for pure random guessing among 10 classes) across multiple training attempts, including with adjusted batch sizes, learning rates, and patience settings.

**Diagnosis process:** Ruled out data/label bugs through systematic checks (label-value integrity, text/label alignment, untrained model prediction sanity checks — all came back clean). Attempted the classic ML debugging technique of testing whether the model could overfit a tiny 32-example subset; it showed partial improvement before permanently plateauing, a pattern consistent with dead ReLU units (neurons whose weights get pushed into a state where their output and gradient are permanently zero, halting further learning in that pathway).

**Fix (pragmatic pivot):** Rather than continuing to debug an unstable neural network under time pressure, replaced the dish-classification GRU entirely with a simple, deterministic keyword-matching function — checking whether a dish's name literally appears as a word in the review text. This requires no training and cannot suffer from convergence failures, while still providing the dish-identity signal the fusion model needs.

**Lesson:** Not every sub-problem in a deep learning pipeline needs a trained neural network; a simple, interpretable, engineered feature is sometimes more reliable and equally effective, particularly under time constraints.

### 9. Weak fusion signal despite a reliable keyword feature

**Problem:** Even after adding the deterministic keyword feature, the fusion model still only reached ~54% accuracy — barely better than chance for a balanced binary task.

**Diagnosis:** A direct arithmetic check (comparing the CNN's predicted dish against the keyword-detected dish, with no model involved) showed 96.5% theoretical accuracy was achievable from the available features — meaning the answer was clearly present in the data, but the trained model wasn't finding it. The root cause was a feature-scale mismatch: the 1280-dimension image embedding had high-variance values (roughly 0-4 range), while the informative keyword/probability features were small, clean 0-1 values — the network's first layer had to implicitly learn to "tune out" noisy high-variance features to find the small, clean signal, which was happening too slowly within the training budget.

**Fix:** Added `BatchNormalization` immediately after the model's input layer, normalizing all 1,364 raw fused features to a consistent scale before any learning occurs. This single change took validation accuracy from ~54% to ~89% within the same training run.

**Lesson:** Feature scale consistency across concatenated multi-modal inputs is critical; without normalization, a strong signal can be effectively invisible to a model even when it is mathematically present in the data.

---

## Limitations

1. Review text is synthetically templated rather than authored by real users; the sentiment-training corpus itself is also not food-specific.
2. Rating prediction is a documented approximation derived from sentiment confidence, not a genuinely trained regression against real star ratings.
3. Helpful/verified review prediction was not implemented within this version's scope.
4. The "Image-Only" comparison baseline directly reuses the same logic used to generate ground-truth labels, so it should be read as a reference ceiling rather than a fully independent competing model.
5. Dataset size (2,500 images across 10 classes; 20,000 reviews) is modest by production standards; a deployed system would need substantially more data and broader dish coverage.
