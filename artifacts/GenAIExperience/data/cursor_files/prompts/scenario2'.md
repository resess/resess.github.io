# Scenario 2'

## Setup

### Project specificity:

* Main app features, saved as [`app_features.md`](../specificity/app_features.md)

### Design granularity: 

* [`structure_frontend.mdc`](../granularity/structure_frontend.mdc)
* [`structure_backend.mdc`](../granularity/structure_backend.mdc)


### Additional Cursor Rules that are applied: 

* [`general_project_specification.mdc`](../additional_guidelines/general_project_specification.mdc)

---

## Prompts (by-feature)

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

### > Prompt 1.0: Feature X Base Prompt

> The project feature list is in @app_features.md.
> * [If this is the first feature] So far, you have not implemented any feature yet. 
> * [If this is not the first feature] So far, you have already implemented features A,B,C.
>
> You will now implement feature X.
> 
> Let's start step by step. Please do not do anything before I ask.


### > Prompt 1.1.1: Backend Implementation

> Please implement the **backend** part needed for the feature. 
> 
> Please organize the generated code into coherent components, adding components or augmenting existing comopnents, as necessary. 
> Please document backend APIs you introduced using the OpenAPI Specification format, in the file named `backend/docs/api.yml`. The generated API file will be used by the frontend of the application. 
> 
> Please ask me if you need any API keys, Client IDs for Google Authentication, database URLs, or any other setup information you do not have. 
>
> Please only do what I asked and nothing else.

### > Prompt 1.1.2: Backend Tests

> Please generate tests for the backend part of the app. Backend testing should focus on backend APIs. Run all tests and make sure the implementation passes all the tests for the API. Update the implementation and the interface file `backend/docs/api.yml`, if needed.  
> 
> Please only do what I asked and nothing else.


### > Prompt 1.2.1: E2E Tests

> The backend part needed for the feature has already been implemented. The backend API specifications can be found in the file named `backend/docs/api.yml`. Please generate end-to-end user-level tests (in Android) for the app. 
> 
> Please only do what I asked and nothing else. 

### > Prompt 1.2.2: Frontend Implementation 

> The backend part needed for the feature has already been implemented. The backend API specifications can be found in the file named `backend/docs/api.yml`. Please implement the **frontend** part of the application based on the feature description. Please deploy the frontend app, connect it with the backend, and make sure that the implementation is functional. Please run all the tests and make sure the implementation passes all the tests you generated for the feature.  
> 
> Please only do what I asked and nothing else. 

--- 

### > Repeat Prompts 1.0 till Prompt 1.2.2 for all features
