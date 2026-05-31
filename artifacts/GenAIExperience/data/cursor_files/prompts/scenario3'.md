# Scenario 3' 

## Setup

### Project specificity:

* [Formal Use Case Specifications](../../zip/cursor_files.zip)

### Design granularity: 

* [`structure_frontend.mdc`](../granularity/structure_frontend.mdc)
* [`structure_backend.mdc`](../granularity/structure_backend.mdc)


### Additional Cursor Rules that are applied: 

* [`general_project_specification.mdc`](../additional_guidelines/general_project_specification.mdc)
* [`maintainability.mdc`](../additional_guidelines/maintainability.mdc)
* [`security.mdc`](../additional_guidelines/security.mdc)
* [`performance.mdc`](../additional_guidelines/performance.mdc)  
* [`testing.mdc`](../additional_guidelines/testing.mdc)

---

## Prompts (by-use-case)

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


### > Prompt 1.1.1: Backend Implementation

> Please implement the **backend** part needed for the use case.
> 
> Please organize the generated code into coherent components, adding components or augmenting existing components, as necessary.  
>
> Please document new backend APIs you introduced using the OpenAPI Specification format. Make sure to have one API file per component, named `backend/docs/<COMPONENT_NAME>.yml`. Create or augment this file, as necessary. The generated API files will be used by the frontend of the application.  
> 
> Please ask me if you need any API keys, Client IDs for Google Authentication, database URLs, or any other setup information you do not have. 
> 
> Please only do what I asked and nothing else.

### > Prompt 1.1.2: Backend Tests

> Please generate tests for the **backend** of the app. Backend testing should focus on backend APIs. Run all tests and make sure the implementation passes all the tests for the API. Update the implementation and the interface file `backend/docs/<COMPONENT_NAME>.yml`, if needed.
> 
> Please only do what I asked and nothing else.

### > Prompt 1.2.1: E2E Tests

> The backend part needed for the use case has already been implemented. The backend API specifications for each backend component can be found in files named `backend/docs/`<COMPONENT_NAME>.yml`. 
> Please generate end-to-end user-level tests (in Android) for the use case based on the formal use case specifications.
> 
> Please only do what I asked and nothing else. 


### > Prompt 1.2.2: Frontend Implementation

> The backend part needed for the use case has already been implemented. The backend API specifications can be found in the file named `backend/docs/api.yml`. Please implement the **frontend** part of the use case based on the formal use case specifications. Please deploy the **frontend** app, connect it with the backend, and make sure that the implementation is functional. Please run all the tests and make sure the implementation passes all the tests you generated for the use case. 
> 
> Please only do what I asked and nothing else. 

---

### > Repeat Prompts 1.0 till Prompt 1.2.2 for all use cases
