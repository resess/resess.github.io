# Scenario 2

## Setup

### MovieSwipe description: 

* Main app features, saved as [`app_features.md`](../description/app_features.md)

### MovieSwipe design: 

* [`structure_frontend.mdc`](../design/structure_frontend.mdc)
* [`structure_backend.mdc`](../design/structure_backend.mdc)


### Additional Cursor Rules that are applied: 

* [`general_project_specification.mdc`](../additional_guidelines/general_project_specification.mdc)

---

## Prompts

### > Prompt 0: Base Prompt

> I want you to implement a collaborative movie selection app that helps groups decide what movie to watch together using an interactive swiping mechanism. Let’s start step-by-step. Please do not do anything before I ask. 


### > Prompt 0.1: Backend Structure

> Create ONLY the Node.js TypeScript backend structure - folders and placeholder files. No implementation. I'll add features in separate prompts.  
@structure_backend.mdc 

### > Prompt 0.2: Frontend Structure

> Create ONLY the Android application frontend structure - folders and placeholder files. No implementation. I'll add features in separate prompts.  
> 
> @structure_frontend.mdc

---

### > Prompt 1: Backend Implementation

> Please Implement the **backend** part of the application. Please organize the generated code into coherent components.  Please document backend APIs you introduced using the OpenAPI Specification format, in the file named `backend/docs/api.yml`. The generated API file will be used by the frontend of the application.  Please ask me if you need any API keys, Client IDs for Google Authentication, database URLs, or any other setup information you do not have.  Please generate tests for the **backend** part of the app. Backend testing should focus on backend APIs.  Run all tests and make sure the implementation passes all the tests for the API. Update the implementation and the interface file `backend/docs/api.yml`, if needed.  
> 
> @app_features.md


---

### > Prompt 2: Frontend Implementation

> The backend has already been implemented. The backend API specifications can be found in the file named `backend/docs/api.yml`. Please generate end-to-end user-level tests for the feature based on the feature description.  Please Implement the **frontend** part of the application based on the application description. Please deploy the **frontend** app, connect it with the backend, and make sure that the implementation is functional. Please run all the tests and make sure the implementation passes all the tests you generated.  
> 
> @app_features.md
