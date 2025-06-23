import pytrec_eval
import os
import json
import pandas as pd

def compute_metrics(qrels, runs, folder, metrics=['map', 'P_5', 'P_10', 'P_15', 'P_20']):    
    # Metrics to Evaluate
    evaluator = pytrec_eval.RelevanceEvaluator(qrels, {'map', 'P'})
    
    for run_name, run in runs.items():
        k = run_name.split("_")[1]
        print(f"Computing metrics for run with k = {k}")
        
        # Verify how many documents were retrieved per query
        # for query_id, docs in run.items():
            # num_docs = len(docs)
            # print(f"Query ID: {query_id} - Retrieved Documents: {num_docs}")
            
        results = evaluator.evaluate(run)
        
        #Print available metrics for debugging
        # first_query = list(results.keys())[0]
        # print(f"Available metrics for {first_query}: {list(results[first_query].keys())}")
        
        # Compute average metrics
        avg_scores = {metric: 0.0 for metric in metrics}
        num_queries = len(results)
        
        for res in results.values():
            for metric in metrics:
                avg_scores[metric] += res.get(metric, 0.0)
        
        for metric in metrics:
            avg_scores[metric] /= num_queries
                                                                                                                                               
        # Prepare output directory
        output_dir = os.path.join("../results", folder)
        os.makedirs(output_dir, exist_ok=True)
        
        # Save per-query metrics
        per_query_path = os.path.join(output_dir, f"per_query_metrics_top_{k}.json")
        with open(per_query_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)
        
        # Save average metrics
        avg_metrics_path = os.path.join(output_dir, f"average_metrics_top_{k}.json")
        with open(avg_metrics_path, "w", encoding="utf-8") as f:
            json.dump(avg_scores, f, indent=4)
        
        print(f"✅ Per-query metrics saved to: {per_query_path}")
        print(f"✅ Average metrics saved to: {avg_metrics_path}\n")
        
def compare_phases(phases, k_values=[20, 30, 50], metrics=['map', 'P_5', 'P_10', 'P_15', 'P_20']):
    """
    Display and optionally compare retrieval metrics for 1 to 4 phases.
    Parameters:
    - phases: dict mapping phase names to base file paths, e.g.
        {
            "Phase 1": "../results/phase_1/average_metrics_top_{}.json",
            "Phase 2": "../results/phase_2/average_metrics_top_{}.json",
            ...
        }
    - k_values: list of cutoff values to compare (e.g. [20, 30, 50])
    - metrics: list of TREC metric keys (e.g. ['map', 'P_5', 'P_10'])

    Returns:
    - pandas DataFrame with metrics for all phases at each k
    """
    comparison = []

    for k in k_values:
        row = {"k": k}
        for phase_name, base_path in phases.items():
            try:
                with open(base_path.format(k), "r") as f:
                    phase_metrics = json.load(f)
                row[f"{phase_name} MAP"] = phase_metrics["map"]
                for m in metrics[1:]: # exclude MAP
                    row[f"{phase_name} avgPre@{m[2:]}"] = phase_metrics[m]
            except FileNotFoundError:
                print(f"⚠️ File not found: {base_path.format(k)}")
        comparison.append(row)

    df = pd.DataFrame(comparison)
    df.sort_values("k", inplace=True)
    df.set_index("k", inplace=True) # Set 'k' column as the index for visualization purposes
    
    return df