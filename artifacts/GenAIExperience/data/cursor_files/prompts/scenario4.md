# Scenario 4 

## Setup

### Project specificity:

* [Formal Use Case Specifications](../../zip/cursor_files.zip)

### Design granularity: 

* [`structure_frontend.mdc`](../granularity/structure_frontend.mdc)
* [`structure_backend.mdc`](../granularity/structure_backend.mdc)
* [`design_frontend.mdc`](../granularity/design_frontend.mdc)
* [`design_backend.mdc`](../granularity/design_backend.mdc)

### Additional Cursor Rules that are applied: 

* [`general_project_specification.mdc`](../additional_guidelines/general_project_specification.mdc)
* [`maintainability.mdc`](../additional_guidelines/maintainability.mdc)
* [`security.mdc`](../additional_guidelines/security.mdc)
* [`performance.mdc`](../additional_guidelines/performance.mdc)  
* [`testing.mdc`](../additional_guidelines/testing.mdc)

---

## Prompts (by-design-components)

### > Prompt 0: Base Prompt

> I want you to implement a collaborative movie selection app that helps groups decide what movie to watch together using an interactive swiping mechanism. 
> 
> Let’s start step-by-step. Please do not do anything before I ask. 


### > Prompt 0.1: Backend Structure

> Create ONLY the Node.js TypeScript backend structure - folders and placeholder files. Do not add implementation. I'll add features in separate prompts.  
> 
> @structure_backend.mdc 

### > Prompt 0.2: Frontend Structure

> Create ONLY the Android application frontend structure - folders and placeholder files. Do not add implementation. I'll add features in separate prompts.  
> 
> @structure_frontend.mdc

---

### > Prompt 1.0: Use Case X Base Prompt

> The formal use case specification for all project features are in `./formal_use_case_specifications/`.  
> * [If this is the first use case] So far, you have not implemented any use case yet.  
> * [If this is not the first use case] So far, you have already implemented use cases A,B,C.  
>
> You will now implement use case X. 
> The formal use case specification of the use case can be found in:
@./formal_use_case_specifications/ucx_<use_case_name>.md
>
> Let’s start step by step. Please do not do anything before I ask.


### > Prompt 1.1.0: Backend Base Prompt

> I want to implement the **backend** of the use case. You must ensure that the packages you use in the code are added as dependencies.
> Please do not do anything before I ask.

### > Prompt 1.1.1: Backend Model

> The details of backend design are described in @design_backend.mdc.
> Create/update the necessary models for the use case.
> You can create/update cross-cutting concerns whenever necessary.
> Please only do what I asked and nothing else.

### > Prompt 1.1.2: Backend Repository

> The details of backend design are described in @design_backend.mdc.
> Create/update the necessary repositories for the use case.
> You can create/update cross-cutting concerns whenever necessary.
> Please only do what I asked and nothing else.

### > Prompt 1.1.3: Backend Service

> The details of backend design are described in @design_backend.mdc.
> Create/update the necessary services for the use case.
> You can create/update cross-cutting concerns whenever necessary.
> Please only do what I asked and nothing else.


### > Prompt 1.1.4: Backend Controller

> The details of backend design are described in @design_backend.mdc.
> Create/update the necessary controllers for the use case.
> You can create/update cross-cutting concerns whenever necessary.
> Please only do what I asked and nothing else.

### > Prompt 1.1.5: Backend Route

> The details of backend design are described in @design_backend.mdc.
> Create/update the necessary routes for the use case.
> You can create/update cross-cutting concerns whenever necessary.
> Reiterate, and connect all layers: routes, controllers, services, repositories, and models. Ensure that all backend endpoints are fully-functional.
> Please only do what I asked and nothing else.


### > Prompt 1.1.6: Backend Tests

> Please generate tests for the **backend** of the app. Backend testing should focus on backend APIs. Run all tests and make sure the implementation passes all the tests for the API. Update the implementation and the interface file `backend/docs/<COMPONENT_NAME>.yml`, if needed.
> 
> Please only do what I asked and nothing else.



### > Prompt 1.2.1: E2E Tests

> The backend part needed for the use case has already been implemented. The backend API specifications for each backend component can be found in files named `backend/docs/`<COMPONENT_NAME>.yml`. 
> Please generate end-to-end user-level tests (in Android) for the use case based on the formal use case specifications.
> 
> Please only do what I asked and nothing else. 


### > Prompt 1.2.2: Frontend Base Prompt

> The backend part needed for the use case has already been implemented. 
> Now, I want to implement the **frontend** of the use case.
> You must ensure that the packages you use in the code are added as dependencies.
> Please do not do anything before I ask.


### > Prompt 1.2.3: Frontend UI Element

> The details of frontend design are described in @design_frontend.mdc.
> Create/update the necessary UI Elements for the use case. 
> You can create/update UI-layer or application-level cross-cutting concerns whenever necessary. 
> 
> Please only do what I asked and nothing else.


### > Prompt 1.2.4: Frontend State Holder

> The details of frontend design are described in @design_frontend.mdc.
> Create/update the necessary State Holders for the use case. 
> You can create/update UI-layer or application-level cross-cutting concerns whenever necessary. 
> 
> Please only do what I asked and nothing else.


### > Prompt 1.2.5: Frontend Repository

> The details of frontend design are described in @design_frontend.mdc.
> Create/update the necessary Repositories for the use case. 
> You can create/update UI-layer or application-level cross-cutting concerns whenever necessary. 
> 
> Please only do what I asked and nothing else.


### > Prompt 1.2.6: Frontend Data Source


> The details of frontend design are described in @design_frontend.mdc.
> Create/update the necessary Data Sources for the use case. 
> You can create/update UI-layer or application-level cross-cutting concerns whenever necessary. 
> Reiterate, and connect all layers: UI elements, state holders, repositories, and data sources. Ensure that the frontend is well integrated with the backend and the use case is fully-functional.
> 
> Please only do what I asked and nothing else.

---

### > Repeat Prompt 1.0 till Prompt 1.2.6 for all use cases
