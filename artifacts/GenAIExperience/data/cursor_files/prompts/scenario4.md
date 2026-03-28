# Scenario 4 

## Setup

### MovieSwipe description: 

* [Formal Use Case Specifications](../../zip/cursor_files.zip)

### MovieSwipe Design: 

* [`design_frontend.mdc`](../design/design_frontend.mdc)
* [`design_backend.mdc`](../design/design_backend.mdc)

### Additional Cursor Rules that are applied: 

* [`general_project_specification.mdc`](../additional_guidelines/general_project_specification.mdc)
* [`maintainability.mdc`](../additional_guidelines/maintainability.mdc)
* [`security.mdc`](../additional_guidelines/security.mdc)
* [`performance.mdc`](../additional_guidelines/performance.mdc)  
* [`testing.mdc`](../additional_guidelines/testing.mdc)

---

## Prompts

### > Prompt 0

> I want you to implement a collaborative movie selection app that helps groups decide what movie to watch together using an interactive swiping mechanism. Let’s start step by step. PLEASE DO NOT DO ANYTHING BEFORE I ASK.

### > Prompt 0.1: Backend Structure

> Create ONLY the Node.js TypeScript backend structure - folders and placeholder files. No implementation. I'll add features in separate prompts.  
>
> @design_backend.mdc


### > Prompt 0.2: Frontend Structure

> Create ONLY the Android application frontend structure - folders and placeholder files. No implementation. I'll add features in separate prompts.  
>
> @design_frontend.mdc

---

### > Prompt 1.0: Use Case X Base Prompt

> I want you to implement a collaborative movie selection app that helps groups decide what movie to watch together using an interactive swiping mechanism. I want to implement the ‘[USE CASE]’ use case. 
> 
> [FORMAL USE CASE DESCRIPTION] 
> 
> Let’s start step by step. PLEASE DO NOT DO ANYTHING BEFORE I ASK.


### > Prompt 1.1.0: Backend Base Prompt

> I want to implement the **backend** of the [USE CASE] use case. You must ensure that the packages you use in the code are added as dependencies. PLEASE DO NOT DO ANYTHING BEFORE I ASK.

### > Prompt 1.1.1: Backend Model for Domain X

> Create/update the necessary models for the [DOMAIN] domain of [USE CASE]. 
The details of backend domains and the design is described in @design_backend.mdc.
You can create/update cross-cutting concerns whenever necessary.
PLEASE ONLY DO WHAT I ASKED AND NOTHING ELSE.

### > Prompt 1.1.2: Backend Repositories for Domain X

> Create/update the necessary repositories for the [DOMAIN] domain of [USE CASE] use case.
The details of backend domains and design is described in @design_backend.mdc.
You can create/update cross-cutting concerns whenever necessary.
PLEASE ONLY DO WHAT I ASKED AND NOTHING ELSE.

### > Prompt 1.1.3: Backend Services for Domain X

> Create/update the necessary services for the [DOMAIN] domain of [USE CASE] use case.
The details of backend domains and design is described in @design_backend.mdc.
You can create/update cross-cutting concerns whenever necessary.
PLEASE ONLY DO WHAT I ASKED AND NOTHING ELSE.

### > Prompt 1.1.4: Backend Controllers for Domain X

> Create/update the necessary controllers for the [DOMAIN] domain of [USE CASE] use case.
The details of backend domains and design is described in @design_backend.mdc.
You can create/update cross-cutting concerns whenever necessary.
PLEASE ONLY DO WHAT I ASKED AND NOTHING ELSE.


### > Prompt 1.1.5: Backend Routes for Domain X

> Create/update the necessary routes for the [DOMAIN] domain of [USE CASE] use case.
The details of backend domains and design is described in @design_backend.mdc.
You can create/update cross-cutting concerns whenever necessary.
Reiterate, and connect all layers: routes, controllers, services, repositories, and models. Ensure that all backend endpoints are fully-functional.
PLEASE ONLY DO WHAT I ASKED AND NOTHING ELSE.

### > Repeat Prompts 1.1.1 - 1.1.5 for Each Domain Relevant To This Use Case


### > Prompt 1.2.0: Frontend Base Prompt

> Now, I want to implement the **frontend** of the [USE CASE] use case.
The backend of the [USE CASE] has been implemented. 
You must ensure that the packages you use in the code are added as dependencies.
PLEASE DO NOT DO ANYTHING BEFORE I ASK.

### > Prompt 1.2.1: Frontend UI Elements for Domain X

> Create/update the necessary UI Elements for the [DOMAIN] domain of [USE CASE] use case. 
The details of frontend domains and design are described in @design_frontend.mdc.
You can create/update UI-layer or application-level cross-cutting concerns whenever necessary. PLEASE ONLY DO WHAT I ASKED AND NOTHING ELSE.


### > Prompt 1.2.2: Frontend State Holders for Domain X

Create/update the necessary state holders for the [DOMAIN] domain of [USE CASE] use case.
The details of frontend domains and design are described in @design_frontend.mdc.
You can create/update UI-layer or application-level cross-cutting concerns whenever necessary.
PLEASE ONLY DO WHAT I ASKED AND NOTHING ELSE.


### > Prompt 1.2.3: Frontend Repositories for Domain X

> Create/update the necessary repositories for the [DOMAIN] domain of [USE CASE] use case.
The details of frontend domains and design are described in @design_frontend.mdc.
You can create/update UI-layer or application-level cross-cutting concerns whenever necessary.
PLEASE ONLY DO WHAT I ASKED AND NOTHING ELSE.

### > Prompt 1.2.4: Frontend Data Sources for Domain X

> Create/update the necessary data sources for the [DOMAIN] domain of [USE CASE] use case.
The details of frontend domains and design are described in @design_frontend.mdc.
You can create/update UI-layer or application-level cross-cutting concerns whenever necessary.
Reiterate, and connect all layers: UI elements, state holders, repositories, and data stores. Ensure that the frontend is well integrated with the backend and the [USE CASE] use case is fully-functional.
PLEASE ONLY DO WHAT I ASKED AND NOTHING ELSE.

### > Repeat Prompts 1.2.1 - 1.2.4 for Each Domain Relevant To This Use Case

---

### > Repeat Prompt 1.0 till Prompt 1.2.4 for all use cases
