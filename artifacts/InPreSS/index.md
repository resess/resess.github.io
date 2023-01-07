---
layout: default
title: Home
nav_order: 1
description: "Responsibility in Context: On Applicability of Slicing in Semantic Regression Analysis"
permalink: /
---

### Responsibility in Context: On Applicability of Slicing in Semantic Regression Analysis

---

Numerous program slicing approaches aim at helping developers troubleshoot regression failures -- one of the most time-consuming development tasks.
The main idea behind these approaches is to identify a subset of interdependent program statements relevant to the failure, minimizing the amount of code developers need to inspect.
Accuracy and reduction rate achieved by these techniques are key considerations toward their applicability in practice: inspecting only the statements identified in the slice should be faster and more efficient than inspecting the code in full. This paper reports on our experiment applying one of the most recent and accurate slicing approaches, dual slicing, to the task of troubleshooting regression failures in eight large, open-source software projects. The results of our experiments show that slices produced in this setup are still very large to be comfortably managed. Moreover, we observe that most statements in the slice deal with propagation of information between changed code blocks; these statements are essential for obtaining the necessary context for the changes but are not responsible for the failure directly. Motivated by this insight, we propose a novel approach, implemented in a tool named InPreSS, for reducing the size of a slice by accurately identifying and summarizing the propagation-related code blocks.
Our evaluation of InPreSS shows that it is able to produce slices that are 75% shorter than the original ones for our case-study projects (299 vs. 2,449 code-level statements, on average), 
thus, reducing the amount of information developers need to inspect without losing the necessary contextual information.
We believe our study and the proposed approach will help promote the efficient integration of slicing-based techniques in debugging activities and will inspire further research in this area.

This website contains artifacts used for experimental evaluation described in the paper. We anonymized all information which can be related back to the authors of the paper.
