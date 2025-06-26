# Query Expansion for Enhanced Information Retrieval (IR2025)

This project is a multi-phase implementation of an advanced **Information Retrieval (IR)** system using **query expansion** to improve search performance. The system is designed and evaluated over the **IR2025 document collection**, and implements traditional and modern expansion techniques such as **BM25**, **WordNet synonyms**, and **Word2Vec-based semantic neighbors**.

## Project Goal

To enhance retrieval effectiveness by expanding user queries with relevant synonyms, helping bridge vocabulary mismatches between query and document terms - a common challenge in IR systems.

---

## Phase Overview

### Phase 1 - Classical IR with BM25

- Uses **Elasticsearch** configured with custom analyzers for stopword removal and stemming.
- Applies **BM25 similarity** to rank documents.
- Baseline evaluation using **MAP** and **avgPre@k (P@k)** for `k = 5, 10, 15, 20`.

### Phase 2 - Query Expansion with WordNet

- Expands selected query terms using **WordNet synonyms** and **hypernyms**.
- Implemented in two variants:
  - Expansion using NLTK before preprocessing.
  - Use of custom **Elasticsearch synonym_graph filters**.
- Tests two pipelines:
  - **Preprocess → Expand** (default)
  - **Expand → Preprocess** (experimental)
- Performance compared to Phase 1 using same evaluation metrics.

### Phase 3 - Query Expansion with Word2Vec

- Trains a **Gensim Word2Vec** model using the IR2025 corpus.
- Tests two pipelines:
  - **Preprocess → Expand** (default)
  - **Expand → Preprocess** (experimental)
- Improves **MAP at k=50** over previous phases.
- Finds that semantic expansion before preprocessing boosts mid-rank precision.

---

## 🛠️ Tools & Libraries

- `Elasticsearch 8.17` - Document indexing and search engine.
- `Python 3.x`
- `Gensim` - Word2Vec training and inference.
- `NLTK` - WordNet integration and token processing.
- `pytrec_eval` - TREC-style evaluation (MAP, avgPre@k).
- `Pandas` - Result analysis and metric comparison.

---

## 📊 Evaluation Metrics

Each phase is evaluated using:

- **MAP** - Mean Average Precision
- **avgPre@k** - Average precision at k retrieved documents (`k = 5, 10, 15, 20`)
- **Cutoffs Tested:** 20, 30, and 50

Comparisons are visualized using `compare_phases()` from `utils.py`.

---

## Results

| **Cutoff (k)** | **Phase 1**<br/>(Baseline)       | **Phase 2A**<br/>(WordNet Synonyms) | **Phase 2B**<br/>(WordNet Hypernyms) | **Phase 3**<br/>(Word2Vec Synonyms)  |
|----------------|----------------------------------|-------------------------------------|--------------------------------------|--------------------------------------|
| **MAP**        | 0.020569 / 0.027753 / 0.039911   | 0.020554 / 0.028373 / 0.040848      | 0.020773 / 0.028601 / 0.040099       | **0.021931 / 0.029312 / 0.042975**   |
| **avgPre@5**   | 0.640                            | 0.608                               | 0.636                                | **0.644**                             |
| **avgPre@10**  | 0.582                            | 0.586                               | 0.574                                | **0.610**                             |
| **avgPre@15**  | 0.564                            | 0.556                               | 0.545                                | **0.5907**                            |
| **avgPre@20**  | 0.549                            | 0.538                               | 0.537                                | **0.574**                             |

Phase 3 demonstrates consistent improvements in deeper ranking cutoffs with Word2Vec expansion.

---

## How to Run

1. **Start Elasticsearch server**
2. **Run desired notebook:**
   - `notebook_Phase_1.ipynb` → BM25 baseline
   - `notebook_Phase_2.ipynb` → WordNet expansion
   - `notebook_Phase_3.ipynb` → Word2Vec expansion
3. **Evaluate with `utils.py`:**
   ```bash
   python utils.py
   ```
4. Results are saved in the `results/` folder as `.json`.

---

## 📄 Documentation

Each phase includes a detailed PDF report with:

- Technical implementation
- Experiment design
- Result discussion
- Comparison with prior phases
- Insights into effectiveness of each expansion strategy

Refer to:
- `report-Phase-1.pdf`
- `report-Phase-2.pdf`
- `report-Phase-3.pdf`

---

## 📚 References

- Mikolov et al. (2013). *Efficient Estimation of Word Representations in Vector Space*
- Bird, S. (2006). *NLTK: The Natural Language Toolkit*
- Fellbaum, C. (1998). *WordNet: An Electronic Lexical Database*
- Carpineto & Romano (2012). *A Survey of Automatic Query Expansion in IR*
- BEIR Benchmark, TREC Evaluation Guidelines

---

## Developers

> Maria Schoinaki, BSc Student <br />
> Department of Informatics, Athens University of Economics and Business <br />
> p3210191@aueb.gr <br/><br/>

> Nikos Mitsakis, BSc Student <br />
> Department of Informatics, Athens University of Economics and Business <br />
> p3210122@aueb.gr <br/><br/>

Based on the coursework of **Information Retrieval 2025** @ AUEB  