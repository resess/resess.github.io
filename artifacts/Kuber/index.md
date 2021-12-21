---
layout: default
title: Home
nav_order: 1
description: 
permalink: /
---

## Kuber: Cost-Efficient Microservice Deployment Planner

The microservice-based architecture – a SOA-inspired principle of dividing backend systems into independently deployed components that communicate with each other using language-agnostic APIs – has gained increased popularity in industry. Realistic microservice-based applications contain hundreds of services deployed on a cloud. As cloud providers typically offer a variety of virtual machine (VM) types, each with its own hardware specification and cost, picking a proper cloud configuration for deploying all microservices in a way that satisfies performance targets while minimizing the deployment costs becomes challenging.

Existing work focuses on identifying the best VM types for recurrent (mostly high-performance computing) jobs in an economical manner. Yet, identifying the best VM type for the myriad
of all possible service combinations and further identifying the optimal subset of combinations that minimizes deployment cost is an intractable problem for applications with a large number of
services. To address this problem, we propose an approach, called Kuber, which utilizes a set of strategies to efficiently sample the necessary subset of service combination and VM types to explore.
Comparing Kuber with baseline approaches shows that Kuber is able to find the best deployment with the lowest search cost.

---

This repository contains artifacts used to perform the experiments defined within the paper. We tried our best to anonymize all information which can be related back to the authors of the paper.
