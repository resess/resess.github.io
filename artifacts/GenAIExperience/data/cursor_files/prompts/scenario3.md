# Scenario 3 

## Setup

### MovieSwipe description: 

* [Formal Use Case Specifications](../../zip/cursor_files.zip)

### MovieSwipe Design: 

* [`structure_frontend.mdc`](../design/structure_frontend.mdc)
* [`structure_backend.mdc`](../design/structure_backend.mdc)


### Additional Cursor Rules that are applied: 

* [`general_project_specification.mdc`](../additional_guidelines/general_project_specification.mdc)
* [`maintainability.mdc`](../additional_guidelines/maintainability.mdc)
* [`security.mdc`](../additional_guidelines/security.mdc)
* [`performance.mdc`](../additional_guidelines/performance.mdc)  
* [`testing.mdc`](../additional_guidelines/testing.mdc)

---

## Prompts

### > Prompt 0: Base Prompt

> I want you to implement a collaborative movie selection app that helps groups decide what movie to watch together using an interactive swiping mechanism. Let’s start step by step. Please do not do anything before I ask. 

### > Prompt 0.1: Backend Structure

> Create ONLY the Node.js TypeScript backend structure - folders and placeholder files. No implementation. I'll add features in separate prompts.  
> 
> @structure_backend.mdc

### > Prompt 0.2: Frontend Structure

> Create ONLY the Android application frontend structure - folders and placeholder files. No implementation. I'll add features in separate prompts.  
> 
> @structure_frontend.mdc

---

### > Prompt 1.0: Feature X Base Prompt 

> The formal use case specification for all project features are in `./formal_use_case_specifications/`.  
> * <If this is the first feature> So far, you have not implemented any feature yet.  
> * <If this is not the feature> So far, you have already implemented features X-Y.  
>
>You will now implement feature Z. Let’s start step by step. Please do not do anything before I ask.

### > Prompt 1.1.1: Feature X Backend Implementation

> Please Implement the **backend** part needed for the “Feature X: \<FEATURE_NAME\>”  feature. 
> This feature consists of X use cases (UC):
> * UCX: <USE_CASE_NAME> 
> * UCX: <USE_CASE_NAME> 
> * ... 
> 
> The formal use case specification of the feature can be found in 
> * `./formal_use_case_specifications/ucx_<USE_CASE_NAME>.md`
> * `./formal_use_case_specifications/ucx_<USE_CASE_NAME>.md`
> * ...
> 
> Please organize the generated code into coherent components, adding components or augmenting existing components, as necessary.  
>
> Please document new backend APIs you introduced using the OpenAPI Specification format. Make sure to have one API file per component, named `backend/docs/<COMPONENT_NAME>.yml`. Create or augment this file, as necessary. The generated API files will be used by the frontend of the application.  
> 
> Please ask me if you need any API keys, Client IDs for Google Authentication, database URLs, or any other setup information you do not have. 

### > Prompt 1.1.2: Feature X Backend Tests

> Please generate tests for the **backend** part of the app. Backend testing should focus on backend APIs. Run all tests and make sure the implementation passes all the tests for the API. Update the implementation and the interface file `backend/docs/<COMPONENT_NAME>.yml`, if needed.


### > Prompt 1.2.1: Feature X Frontend Implementation 

> The formal use case specification of the “Feature X: \<FEATURE_NAME\>”  feature can be found in: 
> * `./formal_use_case_specifications/ucx_<USE_CASE_NAME>.md`
> * `./formal_use_case_specifications/ucx_<USE_CASE_NAME>.md`
> * ...
> 
> The backend has already been implemented. The backend API specifications for each backend component can be found in files named `backend/docs/`<COMPONENT_NAME>.yml`. Please generate end-to-end user-level tests for the feature based on the feature description. 


### > Prompt 1.2.2: Feature X Frontend Tests

> Please Implement the **frontend** part of the feature based on the formal use case specification. Please deploy the **frontend** app, connect it with the backend, and make sure that the implementation is functional. Please run all the tests and make sure the implementation passes all the tests you generated for the feature. 

---

### > Repeat Prompt 1.0 till Prompt 1.2.2 for all features
