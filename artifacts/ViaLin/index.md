---
layout: default
title: Home
nav_order: 1
description: 
permalink: /
---

## <span style="font-variant:small-caps;font-family:'Times New Roman', Times, serif;">ViaLin</span>: Path-Aware Dynamic Taint Analysis for Android



Dynamic taint analysis – a program analysis technique that checks whether information flows between particular source and sink locations in the program, has numerous applications in security, program comprehension, and software testing. Specifically, in mobile software, taint analysis is often used to determine whether mobile apps contain stealthy behaviors that leak user-sensitive information to unauthorized third-party servers. While a number of dynamic taint analysis techniques for Android software have been recently proposed, none of them is able to report the complete information propagation path, only reporting flow endpoints, i.e., sources and sinks of the detected information flows. This design optimizes for runtime performance and allows the techniques to run efficiently on a mobile device. Yet, it impedes the applicability and usefulness of the techniques: an analyst using the tool would need to manually identify information propagation paths, e.g., to determine whether appropriate sanitization occurred before the information is released, which is a challenging task in large real-world applications.

In this paper, we address this problem by proposing a dynamic taint analysis technique that reports accurate taint propagation paths. We implement it in a tool, ViaLin, and evaluate it on a set of existing benchmark applications and on 16 large Android applications from the Google Play store. Our evaluation shows that ViaLin accurately detects taint flow paths and, at the same time, is able to run on a mobile device with a relatively low time and memory overhead.

Please use the menu on the let to navigate the supplementary material

---

