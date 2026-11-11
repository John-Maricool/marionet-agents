---
name: ml-project-checklist
description: End-to-end checklist for machine learning projects, from framing and baselines to data splits, experiments, evaluation and release. Use at any stage of building or fine-tuning a model.
---

# ML project checklist

## Framing
- [ ] What decision will the model drive, and what does a wrong answer cost?
- [ ] Is ML needed? Try rules, an existing API or an off-the-shelf model first.
- [ ] One primary metric that reflects the business cost (not just accuracy on imbalanced data).
- [ ] A baseline measured on the same data.

## Data
- [ ] Licence and consent known for every source.
- [ ] Train / validation / test split by entity or time to avoid leakage.
- [ ] Test set held back and never used for tuning.
- [ ] Class balance and duplicates checked.

## Experiments
- [ ] Config files, fixed seeds, logged versions of code, data and libraries.
- [ ] Start small and cheap: classical models, small open models, LoRA before full fine-tuning.
- [ ] Every run recorded, including failures.

## Evaluation
- [ ] Final metric on the test set, against baseline and target.
- [ ] Breakdown by segment (language, region, device, user group).
- [ ] Robustness and, where people are affected, bias checks.

## Release
- [ ] Model card written.
- [ ] Rollback to the previous model possible.
- [ ] Monitoring for drift, errors, latency and cost.

## Cost control
Use free or local compute (Colab free tier, Kaggle notebooks, a local GPU) for experiments. Estimate full-run cost before scaling and get approval for paid compute.
