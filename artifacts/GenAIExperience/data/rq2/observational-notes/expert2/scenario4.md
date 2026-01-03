**Scenario 4: Observational Notes**


This scenario evaluates code generation with more fine-grained prompting. While the resulting code is less bloated and easier to work with before reaching an unfixable state, quality issues persist across both frontend and backend.

---

**Reduced Code Bloat**

While the code still has issues, there's significantly less code bloat and more opportunity to fix problems before they become unmanageable.

**Good Structure**

The code is well-structured.

**By-Task + High-level Design**

Going more fine-grained than features and prompting by-use-case again helps the model, and this time the generated code is better aligned with our rules and setup. It feels like when the agent has fewer worries, it can better apply the rules and implement what is asked of it. Through the generation, there's less chance of seeing something generated out of place or unwanted. 

I think the main reason is that the task is well-defined and so small that it doesn't leave gaps for the model to fill (atomic in a sense). Generating requires more manual work of prompting and fixing, but that actually feels much better as now you can see a small amount of code generated, review it, understand it, and then fix it. 

The model still makes a lot of mistakes, but the mistakes are also small and fixable by just providing logs of errors to the model or explaining the issue. 

**Frontend vs. Backend**

It is still true that there are more things that can go wrong with the frontend. The improvement lies in the greater chance of being able to fix the things that go wrong.

---

**Backend Issues**

**Dead Code**

There's some dead code in session management. For example, `signOut` calls `revokeSessionByIdToken`, but `authenticateUser` never creates a session:

```
export const authenticateUser = async (idToken: string): Promise<AuthenticatedUser> => {
  const googlePayload = await verifyGoogleToken(idToken);
  
  let user = await getUserByGoogleId(googlePayload.sub);
  
  if (!user) {
    const userData: CreateUserData = {
      googleId: googlePayload.sub,
      email: googlePayload.email,
      name: googlePayload.name,
      ...(googlePayload.picture && { profilePictureUrl: googlePayload.picture }),
    };
    user = await createUser(userData);
  }

  return {
    id: user.id,
    email: user.email,
    name: user.name,
    ...(user.profilePictureUrl && { profilePictureUrl: user.profilePictureUrl }),
  };
};

export const signOut = async (idToken: string): Promise<void> => {
  // ID tokens are stateless JWT tokens that cannot be revoked via Google's revocation endpoint.
  // They expire naturally. Attempting to revoke an ID token may fail, so we skip this step.
  // The revocation endpoint is primarily for access tokens and refresh tokens.
  
  // Attempt to revoke the session in our database if it exists
  // Note: It's okay if the session doesn't exist - it might have never been created or already expired
  // Sign out is still considered successful even without a session record
  const revokedSession = await revokeSessionByIdToken(idToken);
  // If revokedSession is null, it means the session didn't exist, which is acceptable
};
```

**Magic Numbers**

Magic numbers without constants or documentation:

```
 score += movie.vote_average * 0.1;
```

**Repeated Code Patterns**

The same issue with repeated code patterns persists:

```
export const startVotingSessionController = async (req: Request, res: Response): Promise<void> => {
  const groupId = req.params.groupId as string | undefined;
  const userId = req.query.userId as string | undefined;

  if (!userId) {
    res.status(401).json({ error: 'User authentication required' });
    return;
  }

  if (!groupId) {
    res.status(400).json({ error: 'Group ID is required' });
    return;
  }

  try {
    const result = await startVotingSession(groupId, userId);

    if (!result.notificationSent) {
      res.status(200).json({
        ...result.groupDetails,
        message: 'You started the voting session successfully but members could not be notified. You might want to contact them directly.',
      });
      return;
    }

    res.status(200).json(result.groupDetails);
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'An unexpected error occurred';

    if (errorMessage === 'This group has been deleted.') {
      res.status(404).json({ error: errorMessage });
      return;
    }

    if (errorMessage === 'Only the group owner can start a voting session.') {
      res.status(403).json({ error: errorMessage });
      return;
    }

    if (errorMessage === 'A voting session is already in progress for this group.') {
      res.status(400).json({ error: errorMessage });
      return;
    }

    if (errorMessage === 'Failed to load movies. Please try again.') {
      try {
        const groupDetails = await getGroupDetails(groupId, userId);
        res.status(200).json({
          ...groupDetails,
          error: 'Failed to load movies. Please try again.',
        });
      } catch (detailsError) {
        res.status(500).json({ error: 'Failed to load movies. Please try again.' });
      }
      return;
    }

    if (errorMessage === 'Failed to start voting session. Please try again.') {
      res.status(500).json({ error: errorMessage });
      return;
    }

    res.status(500).json({ error: 'Failed to start voting session. Please try again.' });
  }
};

export const getNextMovieToVoteOnController = async (req: Request, res: Response): Promise<void> => {
  try {
    const groupId = req.params.groupId as string | undefined;
    const userId = req.query.userId as string | undefined;

    if (!userId) {
      res.status(401).json({ error: 'User authentication required' });
      return;
    }

    if (!groupId) {
      res.status(400).json({ error: 'Group ID is required' });
      return;
    }

    const result = await getNextMovieToVoteOn(groupId, userId);
    
    res.status(200).json(result);
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'An unexpected error occurred';
    
    if (errorMessage === 'This group has been deleted.') {
      res.status(404).json({ error: errorMessage });
      return;
    }
    
    if (errorMessage === 'The voting session has ended.') {
      res.status(400).json({ error: errorMessage });
      return;
    }
    
    if (errorMessage === 'You are no longer a member of this group.') {
      res.status(403).json({ error: errorMessage });
      return;
    }
    
    if (errorMessage === 'Failed to load next movie. Please try again.') {
      res.status(500).json({ error: errorMessage });
      return;
    }

    res.status(500).json({ error: 'An unexpected error occurred' });
  }
};
```

The code style is also error-prone, missing a `return` statement would result in different behavior.

**Sequential API Calls in Loops**

There's a for loop where fetch is called sequentially, which is detrimental to performance. Either batch requests or parallel requests should be used instead:

```
   for (const { movie } of scoredMovies) {
      if (selectedMovies.length >= TARGET_MOVIES) {
        break;
      }

      const movieDetails = await fetchMovieDetailsFromTmdb(movie.id);
      if (movieDetails && movieDetails.runtime) {
        const selectedMovie = convertTmdbMovieToSelectedMovie(movieDetails);
        selectedMovies.push(selectedMovie);
      } else {
        const selectedMovie = convertTmdbMovieToSelectedMovie(movie);
        selectedMovies.push(selectedMovie);
      }
    }
```

**Missing Caching**

There's no caching when getting movies or genres:

```
export const getGenres = async (): Promise<Genre[]> => {
  try {
    let genres = await getAllGenres();

    // TMDB typically returns around 19-20 genres for movies
    // If we have fewer than 10, refresh from TMDB to ensure we have all genres
    const MIN_EXPECTED_GENRES = 10;
    if (genres.length === 0 || genres.length < MIN_EXPECTED_GENRES) {
      try {
        const tmdbGenres = await fetchGenresFromTmdb();
        try {
          await upsertGenres(tmdbGenres);
          genres = await getAllGenres();
        } catch (dbError) {
          console.error('Error saving genres to database:', dbError);
          throw new Error('Failed to load movie genres. Please try again.');
        }
      } catch (tmdbError) {
        if (tmdbError instanceof Error) {
          if (tmdbError.message.includes('Failed to load movie genres')) {
            throw tmdbError;
          }
        }
        throw new Error('Failed to load movie genres. Please try again.');
      }
    }

    return genres.map((genre: GenreDocument) => ({
      id: genre.genreId,
      name: genre.name,
    }));
  } catch (error) {
    if (error instanceof Error) {
      if (error.message.includes('Failed to load movie genres')) {
        throw error;
      }
    }
    throw new Error('Failed to load movie genres. Please try again.');
  }
};
```

---


**Hardcoded Secrets**

Hardcoded secret for Google authentication:

```
        val gso = GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
            .requestIdToken("your_google_client_id") // please update with your google client ID
            .requestEmail()
            .build()
```

**Repeated Error Handling**

Error handling is repeated extensively without abstraction:

```
class UserDataSourceImpl : UserDataSource {
    private val retrofit = Retrofit.Builder()
        .baseUrl(Constants.BASE_URL)
        .addConverterFactory(GsonConverterFactory.create())
        .build()

    private val apiService = retrofit.create(UserApiService::class.java)

    override suspend fun signIn(idToken: String): Result<AuthenticatedUser> {
        return try {
            val request = SignInRequest(idToken)
            val user = apiService.signIn(request)
            Result.success(user)
        } catch (e: HttpException) {
            val errorMessage = try {
                val errorBody = e.response()?.errorBody()?.string()
                val gson = Gson()
                val errorResponse = gson.fromJson(errorBody, ErrorResponse::class.java)
                errorResponse.error ?: getDefaultErrorMessage(e.code())
            } catch (parseException: Exception) {
                Log.e("UserDataSource", "Failed to parse error response", parseException)
                getDefaultErrorMessage(e.code())
            }
            Log.e("UserDataSource", "HTTP error: ${e.code()}, message: $errorMessage")
            Result.failure(Exception(errorMessage))
        } catch (e: IOException) {
            Log.e("UserDataSource", "Network error", e)
            Result.failure(Exception("Google authentication service temporarily unavailable. Please try again."))
        } catch (e: Exception) {
            Log.e("UserDataSource", "Unexpected error", e)
            Result.failure(Exception("Authentication service temporarily unavailable. Please try again."))
        }
    }

    override suspend fun signOut(idToken: String): Result<Unit> {
        return try {
            val request = SignOutRequest(idToken)
            apiService.signOut(request)
            Result.success(Unit)
        } catch (e: HttpException) {
            val errorMessage = try {
                val errorBody = e.response()?.errorBody()?.string()
                val gson = Gson()
                val errorResponse = gson.fromJson(errorBody, ErrorResponse::class.java)
                errorResponse.error ?: getDefaultSignOutErrorMessage(e.code())
            } catch (parseException: Exception) {
                Log.e("UserDataSource", "Failed to parse error response", parseException)
                getDefaultSignOutErrorMessage(e.code())
            }
            Log.e("UserDataSource", "HTTP error: ${e.code()}, message: $errorMessage")
            Result.failure(Exception(errorMessage))
        } catch (e: IOException) {
            Log.e("UserDataSource", "Network error", e)
            Result.failure(Exception("Authentication service temporarily unavailable, cannot sign out. Please try again."))
        } catch (e: Exception) {
            Log.e("UserDataSource", "Unexpected error", e)
            Result.failure(Exception("Authentication service temporarily unavailable, cannot sign out. Please try again."))
        }
    }

    private fun getDefaultErrorMessage(code: Int): String {
        return when (code) {
            503 -> "Google authentication service temporarily unavailable. Please try again."
            401 -> "Authentication unsuccessful. Please try again."
            else -> "Authentication service temporarily unavailable. Please try again."
        }
    }

    private fun getDefaultSignOutErrorMessage(code: Int): String {
        return when (code) {
            503 -> "Authentication service temporarily unavailable, cannot sign out. Please try again."
            400 -> "Session not found or already revoked"
            else -> "Authentication service temporarily unavailable, cannot sign out. Please try again."
        }
    }

    override suspend fun registerFcmToken(userId: String, fcmToken: String): Result<Unit> {
        return try {
            val request = RegisterFcmTokenRequest(userId, fcmToken)
            apiService.registerFcmToken(request)
            Result.success(Unit)
        } catch (e: HttpException) {
            val errorMessage = try {
                val errorBody = e.response()?.errorBody()?.string()
                val gson = Gson()
                val errorResponse = gson.fromJson(errorBody, ErrorResponse::class.java)
                errorResponse.error ?: "Failed to register FCM token. Please try again."
            } catch (parseException: Exception) {
                Log.e("UserDataSource", "Failed to parse error response", parseException)
                "Failed to register FCM token. Please try again."
            }
            Log.e("UserDataSource", "HTTP error: ${e.code()}, message: $errorMessage")
            Result.failure(Exception(errorMessage))
        } catch (e: IOException) {
            Log.e("UserDataSource", "Network error", e)
            Result.failure(Exception("Failed to register FCM token. Please try again."))
        } catch (e: Exception) {
            Log.e("UserDataSource", "Unexpected error", e)
            Result.failure(Exception("Failed to register FCM token. Please try again."))
        }
    }
}
```

**Duplicated Components**

Sometimes the same component is defined twice instead of being reusable. For example, `GenreCheckBoxItem` exists in both `GenrePreferencesScreen` and `JoinGroupGenrePreferencesScreen`:

<img src="data/scenario4/image1.png" alt="" width="400"><br>

**Empty Files**

There are multiple empty files that were never implemented.

**Unused Dependencies**

`CreateGroupViewModel` has `UserRepository` injected but never uses it:

```
class CreateGroupViewModel(
    private val movieRepository: MovieRepository,
    private val votingGroupRepository: VotingGroupRepository,
    private val userRepository: UserRepository
) : ViewModel() {
    private val _uiState = MutableStateFlow(CreateGroupUiState())
    val uiState: StateFlow<CreateGroupUiState> = _uiState.asStateFlow()

    fun openGroupNameDialog() {
        _uiState.value = _uiState.value.copy(
            showGroupNameDialog = true,
            groupName = "",
            groupNameError = null
        )
    }

    fun closeGroupNameDialog() {
        _uiState.value = _uiState.value.copy(
            showGroupNameDialog = false,
            groupName = "",
            groupNameError = null
        )
    }

    fun updateGroupName(name: String) {
        _uiState.value = _uiState.value.copy(
            groupName = name,
            groupNameError = null
        )
    }

    fun validateAndProceedToGenres() {
        val trimmedName = _uiState.value.groupName.trim()
        
        if (trimmedName.isEmpty()) {
            _uiState.value = _uiState.value.copy(
                groupNameError = "Group name is required and must be 3-30 alphanumeric characters."
            )
            return
        }
        
        if (trimmedName.length < 3 || trimmedName.length > 30) {
            _uiState.value = _uiState.value.copy(
                groupNameError = "Group name is required and must be 3-30 alphanumeric characters."
            )
            return
        }
        
        if (!trimmedName.matches(Regex("^[a-zA-Z0-9]+$"))) {
            _uiState.value = _uiState.value.copy(
                groupNameError = "Group name is required and must be 3-30 alphanumeric characters."
            )
            return
        }
        
        _uiState.value = _uiState.value.copy(
            showGroupNameDialog = false,
            showGenrePreferencesScreen = true,
            groupName = trimmedName,
            groupNameError = null,
            genresError = null
        )
        
        loadGenres()
    }

    fun loadGenres() {
        if (_uiState.value.genres.isNotEmpty()) {
            return
        }
        
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(
                isLoadingGenres = true,
                genresError = null
            )
            
            try {
                val genresList = movieRepository.getGenres()
                _uiState.value = _uiState.value.copy(
                    genres = genresList,
                    isLoadingGenres = false,
                    genresError = null
                )
            } catch (e: Exception) {
                val errorMessage = when {
                    e.message?.contains("Failed to load movie genres", ignoreCase = true) == true -> {
                        "Failed to load movie genres. Please try again."
                    }
                    else -> {
                        "Failed to load movie genres. Please try again."
                    }
                }
                _uiState.value = _uiState.value.copy(
                    isLoadingGenres = false,
                    genresError = errorMessage
                )
            }
        }
    }

    fun retryLoadGenres() {
        _uiState.value = _uiState.value.copy(
            genres = emptyList(),
            genresError = null
        )
        loadGenres()
    }

    fun toggleGenreSelection(genreId: Int) {
        val currentSelected = _uiState.value.selectedGenres.toMutableSet()
        if (currentSelected.contains(genreId)) {
            currentSelected.remove(genreId)
        } else {
            currentSelected.add(genreId)
        }
        _uiState.value = _uiState.value.copy(
            selectedGenres = currentSelected,
            createGroupError = null
        )
    }

    fun goBackToGroupNameDialog() {
        _uiState.value = _uiState.value.copy(
            showGenrePreferencesScreen = false,
            showGroupNameDialog = true,
            createGroupError = null
        )
    }

    fun createGroup(userId: String) {
        if (_uiState.value.selectedGenres.isEmpty()) {
            _uiState.value = _uiState.value.copy(
                createGroupError = "Genre selection is required. Please choose at least two preferred movie genres."
            )
            return
        }
        
        if (_uiState.value.selectedGenres.size < 2) {
            _uiState.value = _uiState.value.copy(
                createGroupError = "Genre selection is required. Please choose at least two preferred movie genres."
            )
            return
        }
        
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(
                isLoadingCreateGroup = true,
                createGroupError = null,
                userId = userId
            )
            
            try {
                val genreList = _uiState.value.selectedGenres.toList()
                val createdGroup = votingGroupRepository.createGroup(
                    name = _uiState.value.groupName,
                    ownerId = userId,
                    genrePreferences = genreList
                )
                
                _uiState.value = _uiState.value.copy(
                    isLoadingCreateGroup = false,
                    showGenrePreferencesScreen = false,
                    groupName = "",
                    selectedGenres = emptySet(),
                    createGroupError = null,
                    createdGroupId = createdGroup.id
                )
            } catch (e: Exception) {
                val errorMessage = when {
                    e.message?.contains("Group name is required", ignoreCase = true) == true -> {
                        "Group name is required and must be 3-30 alphanumeric characters."
                    }
                    e.message?.contains("Genre selection is required", ignoreCase = true) == true -> {
                        "Genre selection is required. Please choose at least two preferred movie genres."
                    }
                    e.message?.contains("Failed to create group", ignoreCase = true) == true -> {
                        "Failed to create group. Please try again."
                    }
                    else -> {
                        "Failed to create group. Please try again."
                    }
                }
                _uiState.value = _uiState.value.copy(
                    isLoadingCreateGroup = false,
                    createGroupError = errorMessage
                )
            }
        }
    }

    fun retryCreateGroup() {
        val userId = _uiState.value.userId
        if (userId != null) {
            createGroup(userId)
        }
    }

    fun resetState() {
        _uiState.value = CreateGroupUiState()
    }

    fun clearGroupNameError() {
        _uiState.value = _uiState.value.copy(groupNameError = null)
    }

    fun clearGenresError() {
        _uiState.value = _uiState.value.copy(genresError = null)
    }

    fun clearCreateGroupError() {
        _uiState.value = _uiState.value.copy(createGroupError = null)
    }
}
```

**Missing Caching and Lazy Loading**

The frontend also lacks caching or lazy loading for images and other heavy data.

**Complex LaunchedEffect Logic**

`LaunchedEffect` with heavy and complex logic, which is not a good practice:

```
               LaunchedEffect(authUiState.isAuthenticated, attemptingSilentSignIn, hasNotificationIntent) {
                    // IMPORTANT: If we have a notification intent and are attempting silent sign-in, do NOT navigate here
                    // Let the notification navigation LaunchedEffects handle it
                    if (hasNotificationIntent && attemptingSilentSignIn) {
                        Log.d("FCM", "Skipping default navigation - notification intent detected and attempting silent sign-in: $navigateTo")
                        return@LaunchedEffect
                    }
                    
                    // IMPORTANT: If we have a notification intent, do NOT navigate here
                    // Let the notification navigation LaunchedEffects handle it
                    if (hasNotificationIntent) {
                        Log.d("FCM", "Skipping default navigation - notification intent detected: $navigateTo")
                        return@LaunchedEffect
                    }
                    
                    if (authUiState.isAuthenticated) {
                        // Only navigate to GroupList if we're not handling a notification
                        if (!handledNotificationNavigation) {
                            // Only navigate if we're not already on the correct screen
                            val currentRoute = navController.currentDestination?.route
                            val isOnGroupDetails = currentRoute?.startsWith("group_details/") == true
                            if (currentRoute != Screen.GroupList.route && 
                                currentRoute != Screen.GroupDetails("{groupId}").route &&
                                !isOnGroupDetails) {
                                navController.navigate(Screen.GroupList.route) {
                                    popUpTo(Screen.Authentication.route) { inclusive = true }
                                }
                            }
                        }
                        // Register FCM token after successful sign-in
                        authUiState.userId?.let { userId ->
                            // Store userId in SharedPreferences for notification service access
                            val prefs = getSharedPreferences("movieswipe_prefs", Context.MODE_PRIVATE)
                            prefs.edit().putString("current_user_id", userId).apply()
                            Log.d("FCM", "Stored userId in SharedPreferences: $userId")
                            
                            registerFcmToken(userId)
                        }
                    } else if (!authUiState.isLoading && !attemptingSilentSignIn && !authUiState.signOutSuccess) {
                        // Only navigate to Authentication if we're not already there, not attempting silent sign-in, and not signing out successfully
                        // (when sign out succeeds, we close the app instead of navigating)
                        val currentRoute = navController.currentDestination?.route
                        if (currentRoute != Screen.Authentication.route) {
                            navController.navigate(Screen.Authentication.route) {
                                popUpTo(Screen.GroupList.route) { inclusive = true }
                            }
                        }
                    }
                }
```

---
**Personal Take**

Overall, while the code is easier to get functional and less bloated, there are still multiple quality issues. **More fine-grained prompting doesn't seem to resolve the underlying code quality problems.**

While going by-task is overall better than by-feature, I can see that grouping tasks to cover more than just one feature can be beneficial in some cases. However, this only feels like it works for the backend, where the model seems to be better prepared for certain prompts. For instance, asking the model to implement different parts of CRUD routes one by one is less convenient for it than just asking for the whole CRUD at once. 

In the frontend, a similar pattern exists but to a lesser extent. Doing sign in and sign out together seems more suited for the model than doing them separately. These are things that developers understand when seeing the generation and can optimize for later, but to start with, having a more fine-grained setup is always safer than a coarse-grained one.

I belive the generic frameworks on how to use agentic tools should be toward more specification and more granularity but developers should keep an eye out for specific optimizations based on their own use cases.

