### Scenario 1: Observational Notes
This scenario evaluates the code generation when both frontend and backend are generated together in a single prompt. The observations highlight issues related to code structure (architecture), completeness, unnecessary code, security, and quality.

---
### Generation
Most of the time is spent on the backend and the frontend code is incomplete, frontend contains partially implemented code and includes references that the model did not generate.

For backend: It is nearly complete but the structure is not good, controllers and routes are not separated, the only parts that is mostly missing is about live updates. It took me a some time to make backend buildable and runnable. The MongoDB server that was set up doesn’t work because, during generation, it didn’t ask me for the server URI. As a result, it now tries to connect to something that doesn’t exist. 

For frontend: None of the backend apis are used (they are defined using retrofit but never used) there are only views. Code is just some views definition without any logic and it has a lot of build issues. Fixing one error would introduce many more.

### Run & Build
Backend runs but doesn't build.
ESLint not configured correctly.
Frontend project doesn't sync and run.
Dependencies: Glide is deprecated (not important, minor)

### Bugs
[Major] Shows start and end session button to every member in the group.


[Minor] Should only notify owner that a user has joined a group, not all the group members.

<img src="data/scenario1/image.png" alt="" width="600"><br>


[Minor] It should not broadcast votings of a member to other members of the group.

<img src="data/scenario1/image-1.png" alt="" width="600"><br>


[Minor] It should not broadcast to all if someone left the voting session.

<img src="data/scenario1/image-2.png" alt="" width="600"><br>


[Minor] Should return error if you pass a non-member to be removed from the group.

<img src="data/scenario1/image-3.png" alt="" width="600"><br>


[Minor] Should remove this API or add sessionId when getting user’s group info. Or remove sessionId from the api params.

<img src="data/scenario1/image-4.png" alt="" width="600"><br>


[Major] No error handling for when save group fails.

<img src="data/scenario1/image-5.png" alt="" width="600"><br>


[Major] No validation for the groupId while creating session.

<img src="data/scenario1/image-6.png" alt="" width="600"><br>


[Major] Does not check if user id is valid.

<img src="data/scenario1/image-7.png" alt="" width="600"><br>


[Major] Does not check if API key doesn’t exist.


<img src="data/scenario1/image-8.png" alt="" width="600"><br>


Missing some parts of the third-party authentication configuration.

### Security
**Security vulnerability** Multer package with the version in the link below is in the dependencies:

https://security.snyk.io/package/npm/multer/1.4.5-lts.1

### Logical Issues
To get the user preferences, it has a property maxRating whereas it should be minRating. No user will say I don’t want the rate to be more than 7! → bug

It assumes that we have multiple session for each group.

### Hard-coded values
Uses a predefined list of genres. 

It is consistent with TMDB list for now but if TMDB updates it’s genre list then there will be inconsistencies.
It also get genres from TMDB in movie recommendation service.

<img src="data/scenario1/image-9.png" alt="" width="600"><br>
<img src="data/scenario1/image-10.png" alt="" width="600"><br>


Use magic numbers in code

<img src="data/scenario1/image-11.png" alt="" width="600"><br>
<img src="data/scenario1/image-12.png" alt="" width="600"><br>
<img src="data/scenario1/image-13.png" alt="" width="600"><br>


Hardcoded states

<img src="data/scenario1/image-39.png" alt="" width="600"><br>


### Naming Issues
It’s not clear what is decoded. -> `decodedUser`

<img src="data/scenario1/image-14.png" alt="" width="600"><br>


It is not clear what is the difference between these two.

<img src="data/scenario1/image-15.png" alt="" width="600"><br>


Not clear what progress is referring to. → `votingProgress` or `votingStatus`

<img src="data/scenario1/image-16.png" alt="" width="600"><br>


This methods adds or updates vote.

<img src="data/scenario1/image-17.png" alt="" width="600"><br>


### Unnecessary code
It’s not clear what userPreferences is and what use it has, also when calling this function the code passes null for this parameter!

<img src="data/scenario1/image-18.png" alt="" width="600"><br>
<img src="data/scenario1/image-19.png" alt="" width="600"><br>


No need for logout API since we use JWT.

<img src="data/scenario1/image-20.png" alt="" width="600"><br>


No need for password-related functions since we use OAuth.

<img src="data/scenario1/image-21.png" alt="" width="600"><br>
<img src="data/scenario1/image-22.png" alt="" width="600"><br>


`MinYear`, `MaxYear`, and `MaxRating` is defined in user schema but never used.


Redundant info

<img src="data/scenario1/image-24.png" alt="" width="600"><br>


Owner is a member of the group. No need to check for it separately.

<img src="data/scenario1/image-25.png" alt="" width="600"><br>



### Boilerplate code
Used in socket.ts and 2 times in auth.ts.

<img src="data/scenario1/image-26.png" alt="" width="600"><br>


In all routes instead of middleware.

<img src="data/scenario1/image-27.png" alt="" width="600"><br>


In create, get, join group and get user’s groups.

<img src="data/scenario1/image-28.png" alt="" width="600"><br>


Leave group and remove member from group could be one API. Or at least should move the duplicate code into a shared function.

<img src="data/scenario1/image-28.png" alt="" width="600"><br>
<img src="data/scenario1/image-29.png" alt="" width="600"><br>


`/profile` exists in both auth and user routes.


### Typing issues
Use of any. 15 found with search query of : any.

<img src="data/scenario1/image-30.png" alt="" width="600"><br>


Incomplete typing

<img src="data/scenario1/image-31.png" alt="" width="600"><br>


### Inconsistencies
`/profile`, `/verify`, and `/preferences` do not return the same user object.

<img src="data/scenario1/image-32.png" alt="" width="600"><br>


Returning group owner’s info instead of group members can cause inconsistencies.

<img src="data/scenario1/image-33.png" alt="" width="600"><br>


[ONLY AI] Wrong comment

<img src="data/scenario1/image-34.png" alt="" width="600"><br>



### Design
The API logic should be handled in controllers.

<img src="data/scenario1/image-35.png" alt="" width="600"><br>


Handle auth token in view model

<img src="data/scenario1/image-41.png" alt="" width="600"><br>


### Efficiency
Can check first then create movies and avoid copying and pushing to array.

<img src="data/scenario1/image-36.png" alt="" width="600"><br>
    

### Unused Code
Unused handler functions

<img src="data/scenario1/image-40.png" alt="" width="600"><br>


Unused imports

<img src="data/scenario1/image-37.png" alt="" width="600"><br>


Most of the defined APIs are not used.

Inconsistency between BE and FE API.

<img src="data/scenario1/image-38.png" alt="" width="600"><br>
