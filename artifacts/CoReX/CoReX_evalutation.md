---
layout: default
title: CoReX Evaluation
nav_order: 4
has_children: false
permalink: /docs/CoReX_evalutation
---

## RQ1 (Reduction Rate) and RQ2 (Execution Time) 

### Program Subjects:
We borrowed the evaluation dataset that includes 286 subjects from existing work [InPreSS](https://ieeexplore.ieee.org/abstract/document/10172711),
which includes 278 failures from six projects of the popular Defects4J benchmark (download [here](https://zenodo.org/record/7683853#.Y_3L1y-975g)) and 8 large client-library project pairs with upgrade failures from LibRench (download [here](https://zenodo.org/record/7683853/files/InPreSSBench.zip?download=1)).

### Results:
Detailed information about the experimental results is provided in the file linked below. The file includes two tabs, "RQ1-Reduction Rate" and "RQ2-Time", each showing results for all 286 subjects, grouped by project.

The "RQ1-Reduction Rate" tab shows slice sizes and reduction rates achieved by the DualSlice, InPreSS, CoReXI, and CoReX slices, with results reported separately for the old and new program versions. For comparison, we also include the size of the entire trace and the synchronized slice on this trace.

The "RQ2-Time" tab shows the runtime measurements (in minutes) for DualSlice, InPreSS, CoReXI, and CoReX. We separate the tools’ runtime into that for the slicing and slice summarization. 

* ### [Quantitative Evaluation Results](../../assets/results/QuantitativeEvaluationResults.xlsx)

---

## RQ3 (Alignment with Developers' Selections) 

### Program Subjects:
We used code samples used in the [user study](https://anonymousresearcher24.github.io/docs/user_study).


### Results:
The raw data obtained in this study cannot be shared because of privacy issues. However, we have provided the Precision, Recall, and F-Measure for each developer’s selection across all five slices: Sync.Slice, DualSlice, InPreSS, CoReXI, and CoReX. 
These values are available in the file linked below.

* ### [Alignment Results](../../assets/results/AlignmentResults.xlsx)