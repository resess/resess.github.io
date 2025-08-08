---
layout: default
title: User Study
nav_order: 2
has_children: false
permalink: /docs/user_study
---

## Program Subjects:

As our program subjects, we selected four failures from [Defects4J](https://dl.acm.org/doi/abs/10.1145/2610384.2628055) (a large and popular collection of reproducible real-world failures in Java programs) and two failures from [LibRench](https://ieeexplore.ieee.org/abstract/document/10172711) (a set of real-world client-library project pairs with at least one library upgrade failure).

Table below shows the six selected subjects, together with a short description of each failure. To ensure participants could fully comprehend the code and answer numerous questions within a reasonable time frame of about 30-60 minutes, we shortened and simplified code snippets, preserving the essence of the changes and the failure, while removing implementation details.

<table style="border-collapse: collapse; width: 100%;">
  <tr>
    <th style="border: 1px solid black; padding: 5px; text-align: center;">Dataset</th>
    <th style="border: 1px solid black; padding: 5px; width: 30px; text-align: center;">Sub. ID</th>
    <th style="border: 1px solid black; padding: 5px; text-align: center;">Project (Failure ID)</th>
    <th style="border: 1px solid black; padding: 5px; text-align: center;">Short Description</th>
  </tr>
  <tr>
    <td rowspan="4" style="border: 1px solid black; padding: 5px; text-align: center;"><strong>Defects4J</strong></td>
    <td style="border: 1px solid black; padding: 5px; width: 30px; text-align: center;">S1</td>
    <td style="border: 1px solid black; padding: 5px; text-align: center;">Commons <strong>Chart</strong> (8)</td>
    <td style="border: 1px solid black; padding: 5px; text-align: center;">Modifying <code>timeZone</code> variable reference</td>
  </tr>
  <tr>
    <td style="border: 1px solid black; padding: 5px; width: 30px; text-align: center;">S2</td>
    <td style="border: 1px solid black; padding: 5px; text-align: center;">Commons <strong>Lang</strong> (18)</td>
    <td style="border: 1px solid black; padding: 5px; text-align: center;">Modifying <code>year</code> format</td>
  </tr>
  <tr>
    <td style="border: 1px solid black; padding: 5px; width: 30px; text-align: center;">S3</td>
    <td style="border: 1px solid black; padding: 5px; text-align: center;">Commons <strong>Math</strong> (37)</td>
    <td style="border: 1px solid black; padding: 5px; text-align: center;">Deleting conditional calculations</td>
  </tr>
  <tr>
    <td style="border: 1px solid black; padding: 5px; width: 30px; text-align: center;">S4</td>
    <td style="border: 1px solid black; padding: 5px; text-align: center;">Joda-<strong>Time</strong> (8)</td>
    <td style="border: 1px solid black; padding: 5px; text-align: center;">Modifying arithmetic expression</td>
  </tr>
  <tr>
    <td rowspan="2" style="border: 1px solid black; padding: 5px; text-align: center;"><strong>Librench</strong></td>
    <td style="border: 1px solid black; padding: 5px; width: 30px; text-align: center;">S5</td>
    <td style="border: 1px solid black; padding: 5px; text-align: center;"><strong>Jackson</strong>Databind/OpenAPI</td>
    <td style="border: 1px solid black; padding: 5px; text-align: center;">Removing reference shortcut</td>
  </tr>
  <tr>
    <td style="border: 1px solid black; padding: 5px; width: 30px; text-align: center;">S6</td>
    <td style="border: 1px solid black; padding: 5px; text-align: center;">Alibaba-<strong>Druid</strong>/Dble</td>
    <td style="border: 1px solid black; padding: 5px; text-align: center;">Modifying SQL Parsing</td>
  </tr>
</table>

---

## Study Questionnaires:
The questionnaires were created using the [Qualtrics](https://www.qualtrics.com) – a popular platform that enables the creation and distribution of surveys, and data collection and analysis. Below, we provide two versions of the study questionnaire: "trace first" and "views first," for each of the six subjects. The structure of the questionnaires is identical across subjects, except for the code views and corresponding textual explanations:

* **Subject 1:**
  * [Trace First](../../assets/data/questionnaries/S1_TraceFirstQuestionnaire.pdf)
  * [Views First](../../assets/data/questionnaries/S1_ViewFirstQuestionnaire.pdf)

* **Subject 2:**
  * [Trace First](../../assets/data/questionnaries/S2_TraceFirstQuestionnaire.pdf)
  * [Views First](../../assets/data/questionnaries/S2_ViewFirstQuestionnaire.pdf)

* **Subject 3:**
  * [Trace First](../../assets/data/questionnaries/S3_TraceFirstQuestionnaire.pdf)
  * [Views First](../../assets/data/questionnaries/S3_ViewFirstQuestionnaire.pdf)

* **Subject 4:**
  * [Trace First](../../assets/data/questionnaries/S4_TraceFirstQuestionnaire.pdf)
  * [Views First](../../assets/data/questionnaries/S4_ViewFirstQuestionnaire.pdf)

* **Subject 5:**
  * [Trace First](../../assets/data/questionnaries/S5_TraceFirstQuestionnaire.pdf)
  * [Views First](../../assets/data/questionnaries/S5_ViewFirstQuestionnaire.pdf)

* **Subject 6:**
  * [Trace First](../../assets/data/questionnaries/S6_TraceFirstQuestionnaire.pdf)
  * [Views First](../../assets/data/questionnaries/S6_ViewFirstQuestionnaire.pdf)

---


## Statistical Tests:

To further support our claim that most developers consider contextual statements necessary, we conducted statistical analyses on the statement rankings provided by 55 participants across six debugging subjects, each evaluated using three code views: DualSlice, InPreSS, and Context (i.e., a DualSlice or InPreSS view augmented with contextual information). Specifically, we applied the following statistical tests:

-- **Friedman Test:** To assess whether there are statistically significant differences in participants' rankings across the three tools.

-- **Wilcoxon Signed-Rank Test:** As a post-hoc analysis following the Friedman test, to determine which tool pairs differ significantly from each other.

-- **Kruskal-Wallis Test:** To examine whether participant preferences for each tool differ significantly across the six debugging subjects. This test serves as a non-parametric extension of the Mann-Whitney U test for more than two groups.

These tests help quantify the significance of tool differences and the consistency of preferences across study subjects.


### Test for Differences Between Tools:
<table style="border-collapse: collapse; width: 100%;">
  <tr>
    <th style="border: 1px solid black; padding: 5px; text-align: center; width: 12%;">Test</th>
    <th style="border: 1px solid black; padding: 5px; text-align: center; width: 33%;">Comparison</th>
    <th style="border: 1px solid black; padding: 5px; text-align: center; width: 55%;">Result Summary</th>
  </tr>

  <tr>
    <td style="border: 1px solid black; padding: 5px; text-align: center;"><strong>Friedman</strong></td>
    <td style="border: 1px solid black; padding: 5px; text-align: center;">Dual Slicing vs. InPreSS vs. Context</td>
    <td style="border: 1px solid black; padding: 5px;">X²r = 58.0364 (N = 55), <strong>p &lt; .00001</strong> → Significant at p &lt; .05</td>
  </tr>

  <tr>
    <td rowspan="3" style="border: 1px solid black; padding: 5px; text-align: center;"><strong>Wilcoxon</strong></td>
    <td style="border: 1px solid black; padding: 5px; text-align: center;">Dual Slicing vs. InPreSS</td>
    <td style="border: 1px solid black; padding: 5px;">z = -0.6074, <strong>p = .54186</strong> → Not significant. W = 697.5, Mean Diff = -0.64</td>
  </tr>

  <tr>
    <td style="border: 1px solid black; padding: 5px; text-align: center;">Dual Slicing vs. Context</td>
    <td style="border: 1px solid black; padding: 5px;">z = -5.7184, <strong>p &lt; .00001</strong> → Significant. W = 87.5, Mean Diff = 1.36</td>
  </tr>

  <tr>
    <td style="border: 1px solid black; padding: 5px; text-align: center;">InPreSS vs. Context</td>
    <td style="border: 1px solid black; padding: 5px;">z = -5.932, <strong>p &lt; .00001</strong> → Significant. W = 62, Mean Diff = 1.47</td>
  </tr>
</table>



### Compare Rankings Across Subjects:
<table style="border-collapse: collapse; width: 100%;">
  <tr>
    <th style="border: 1px solid black; padding: 5px; text-align: center; width: 12%;">Test</th>
    <th style="border: 1px solid black; padding: 5px; text-align: center; width: 33%;">Comparison</th>
    <th style="border: 1px solid black; padding: 5px; text-align: center; width: 55%;">Result Summary</th>
  </tr>

  <tr>
    <td rowspan="3" style="border: 1px solid black; padding: 5px; text-align: center;"><strong>Kruskal-Wallis</strong></td>
    <td style="border: 1px solid black; padding: 5px; text-align: center;">Dual Slicing across subjects</td>
    <td style="border: 1px solid black; padding: 5px;">p = .7918 → Not significant at p &lt; .05</td>
  </tr>

  <tr>
    <td style="border: 1px solid black; padding: 5px; text-align: center;">InPreSS across subjects</td>
    <td style="border: 1px solid black; padding: 5px;">p = .94343 → Not significant at p &lt; .05</td>
  </tr>

  <tr>
    <td style="border: 1px solid black; padding: 5px; text-align: center;">Context across subjects</td>
    <td style="border: 1px solid black; padding: 5px;">p = .69585 → Not significant at p &lt; .05</td>
  </tr>
</table>



---


### The raw data obtained in this study cannot be shared because of privacy issues. 