**Scenario 3: Observational Notes**


This scenario evaluates code generation using a feature-by-feature approach. While this provides Cursor with more freedom, e.g., the ability to build and verify the backend, it also results in code bloat and persistent quality issues.

---

**Code Generation Process**

**Generation Approach**

Going feature by feature to generate results in code similar to Scenario 2. Cursor has more freedom and sometimes tries building the backend to ensure there are no build issues.

**By-Feature Generation**
In this scenario we provided all the information needed to describe the app, which was better detailed than previous scenarios, and on top of that used by-feature generation which leads to more fine-grained tasks. Below are the observations in by-feature generation:

* Generation-wise, the backend seems less difficult for the model to generate code for, but for the frontend there seem to be more struggles. This can stem from both the fact that the model doesn't know much Kotlin/Android and also the inherently greater difficulty of frontend generation. If I had limited budget, I would use more prompts for the frontend and fewer prompts for the backend. Even though both are low quality and don't work, it seems the frontend is suffering more.

* The workflow of using AI is more natural and closer to what I would do myself, but the generated code is still unbearable, both in terms of size and the amount of issues happening each time.

* Some features seem to be implemented more easily by the model and some seem to be more difficult. This variability is expected, but what makes a feature easy or hard from an LLM perspective can be difficult to detect before actually prompting the model. For instance, features that include setting up something are more difficult for the model than other features. In the frontend, when implementing auth, the model has to think about setting up Retrofit to call the backend, which doesn't happen in the following features. In contrast, if the feature is mostly simple CRUD in the backend, it appears to be easier for the model. The difficulty effect, and anticipating it when balancing the prompts is a challenge for both the model and the person prompting the model. 

**Code Bloat**

There's more code generated, which is mostly unnecessary and useless. For example, multiple service files exist that are not at the same level of abstraction. For instance, we could have a movieService handling both recommendation and fetching of movies. Also, the database service could be distributed in different services:

<img src="data/scenario3/image1.png" alt="" width="300"><br>

---


**Security Vulnerabilities in Dependencies**

When running `npm install`, multiple security issues are reported:

```
91 packages are looking for funding
  run `npm fund` for details

8 vulnerabilities (3 low, 3 moderate, 1 high, 1 critical)

To address all issues, run:
  npm audit fix
```

Packages have even more security issues than previous scenarios.

**Successful Build**

Despite the security issues, the backend has no build issues:

```
npm run build

> movieswipe-backend@1.0.0 build
> tsc
```

---

**Backend Issues**

**Repeated Error Handling Pattern**

Multiple APIs follow the same pattern of error handling without abstraction:

```
 async getRecommendations(req: Request, res: Response): Promise<void> {
    try {
…
    } catch (error) {
      console.error('Get recommendations error:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to fetch recommendations'
      });
    }
  }

  async toggleFavorite(req: Request, res: Response): Promise<void> {
    try {
     …
    } catch (error) {
      console.error('Toggle favorite error:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to toggle favorite'
      });
    }
  }

  async getFavorites(req: Request, res: Response): Promise<void> {
    try {
      …
    } catch (error) {
      console.error('Get favorites error:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to fetch favorites'
      });
    }
  }
}
```

**Logic Bugs**

The code contains logic bugs. For instance, in `getMovieSelectionResults`:

```
 async getMovieSelectionResults(sessionId: string): Promise<{
    sessionId: string;
    groupId: string;
    selectedMovie: Movie;
    votingResults: Array<{
      movie: Movie;
      yesVotes: number;
      noVotes: number;
      totalVotes: number;
      approvalRate: number;
      score: number;
    }>;
    totalParticipants: number;
    totalVotesCast: number;
    endTime: Date;
    sessionDuration: number; // in minutes
  }> {
    const session = await VotingSessionModel.findById(sessionId);
    if (!session) {
      throw new Error('Voting session not found');
    }

    if (session.status !== 'completed') {
      throw new Error('Voting session is not completed');
    }

    if (!session.selectedMovie) {
      throw new Error('No movie has been selected for this session');
    }

    // Get group details to count participants
    const group = await this.groupService.getGroupById(session.groupId);
    if (!group) {
      throw new Error('Group not found');
    }

    const totalParticipants = group.members.length + 1; // +1 for owner
```

The code adds one for the owner, but in `createGroup`:

```
async createGroup(name: string, ownerId: string): Promise<IGroup> {
    const invitationCode = generateInvitationCode();
    
    const group = new GroupModel({
      name,
      ownerId,
      invitationCode,
      members: [{
        userId: ownerId,
        joinedAt: new Date(),
        preferences: []
      }],
      isActive: true
    });

    return await group.save();
  }
```

**The owner is already part of the members array, resulting in double-counting!**

**Incomplete Service Implementation**

The code returns popular movies instead of using the actual `movieRecommendationService.ts` that exists in the codebase:

```
 async getRecommendations(req: Request, res: Response): Promise<void> {
    try {
      const { groupId } = req.params;
      const { limit = 20 } = req.query;
      
      // For now, return popular movies as recommendations
      // This will be enhanced in the future with group preference-based recommendations
      const movies = await tmdbService.getPopularMovies(1);
      const limitedMovies = movies.slice(0, parseInt(limit as string));
      
      res.status(200).json({
        success: true,
        data: {
          movies: limitedMovies,
          groupId,
          note: 'Currently showing popular movies. Group-based recommendations coming soon.'
        }
      });
    } catch (error) {
      console.error('Get recommendations error:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to fetch recommendations'
      });
    }
  }
```

**Unimplemented Functions**

In `socketService`, there's an `authenticateUser` function that isn't implemented:

```
 private async authenticateUser(token: string): Promise<any> {
    // Implement JWT verification here
    // This is a placeholder - implement actual JWT verification
    return null;
  }
```

**Magic Numbers**

Hardcoded values without constants:

```
hasMore: movies.length === 20
```

**Type Safety Issues**

Incomplete typing and type safety issues:

```
const userId = (req as any).user.id;
```

**Code Duplication**

Extensive code duplication in controllers:

```
async createSession(req: Request, res: Response): Promise<void> {
    try {
      const { groupId } = req.body;
      const userId = (req as any).user.id;

      if (!groupId) {
        res.status(400).json({
          success: false,
          error: 'Group ID is required'
        });
        return;
      }

      const session = await votingService.createSession(groupId, userId);
      
      res.status(201).json({
        success: true,
        data: {
          id: (session as any)._id,
          groupId: session.groupId,
          status: session.status,
          movies: session.movies,
          votes: session.votes,
          startTime: session.startTime,
          endTime: session.endTime,
          selectedMovie: session.selectedMovie,
          createdAt: session.createdAt,
          updatedAt: session.updatedAt
        }
      });
    } catch (error) {
      console.error('Create session error:', error);
      res.status(500).json({
        success: false,
        error: error instanceof Error ? error.message : 'Failed to create voting session'
      });
    }
  }

  /**
   * GET /api/voting/sessions/active/:groupId
   * Get active voting session for a group
   */
  async getActiveSession(req: Request, res: Response): Promise<void> {
    try {
      const { groupId } = req.params;
      const userId = (req as any).user.id;

      const session = await votingService.getActiveSession(groupId);
      
      if (!session) {
        res.status(404).json({
          success: false,
          error: 'No active voting session found for this group'
        });
        return;
      }

      res.status(200).json({
        success: true,
        data: {
          id: (session as any)._id,
          groupId: session.groupId,
          status: session.status,
          movies: session.movies,
          votes: session.votes,
          startTime: session.startTime,
          endTime: session.endTime,
          selectedMovie: session.selectedMovie,
          createdAt: session.createdAt,
          updatedAt: session.updatedAt
        }
      });
    } catch (error) {
      console.error('Get active session error:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to fetch active session'
      });
    }
  }

  /**
   * POST /api/voting/sessions/:sessionId/start
   * Start a voting session
   */
  async startSession(req: Request, res: Response): Promise<void> {
    try {
      const { sessionId } = req.params;
      const userId = (req as any).user.id;

      const session = await votingService.startSession(sessionId, userId);
      
      res.status(200).json({
        success: true,
        data: {
          id: (session as any)._id,
          groupId: session.groupId,
          status: session.status,
          movies: session.movies,
          votes: session.votes,
          startTime: session.startTime,
          endTime: session.endTime,
          selectedMovie: session.selectedMovie,
          createdAt: session.createdAt,
          updatedAt: session.updatedAt
        },
        message: 'Voting session started successfully'
      });
    } catch (error) {
      console.error('Start session error:', error);
      res.status(500).json({
        success: false,
        error: error instanceof Error ? error.message : 'Failed to start voting session'
      });
    }
  }
```

The same result pattern and error handling is duplicated throughout.

**Persistent Security Issues**

The same security issue with fallback values persists:

```
export const appConfig: AppConfig = {
...
  jwtSecret: process.env.JWT_SECRET || 'your-super-secret-jwt-key',
...
};
```

**Performance Issues**

Performance issues when using sockets with large payloads:

```
// Sends full movies array (20 movies with all details) to all clients:
this.io.to(`group:${session.groupId}`).emit('session:started', {
  sessionId,
  movies: session.movies
});
```

---

**Frontend Issues**

**Faulty Owner Check Logic**

The frontend has obvious issues. For example, checking the first member in the group list to be the owner which is a fragile assumption:

```
if (group.ownerId == group.members.firstOrNull()?.userId) {
    Button(onClick = { viewModel.generateInviteCode(group.id) }) {
```

**Build Errors**

There are inconsistencies in the code resulting in build/compile errors like argument mismatches:

```
composable(Screen.Group.route) { GroupScreen(
    onVoteSession = { sessionId -> navController.navigate(Screen.VotingWithSession.createRoute(sessionId)) }
) }
```

```
@Composable
fun GroupScreen(
    viewModel: GroupViewModel = viewModel()
) {
```

There are also missing imports in some files.

**Incomplete Functionality**

While the functionality is more complete, some features are still missing. For example, the leave group implementation is incomplete.

**Magic Numbers and Hardcoding**

Magic numbers for swipe threshold:

```
if (swipeOffset > 200) {
    votingViewModel.vote("yes")
```

Other magic numbers and hardcoding:

```
valueRange = 1f..10f,
steps = 8
Color(0xFFE3F2FD) 
modifier = Modifier.height(180.dp)
```

**Unused Code**

Unused code for dependency injection:

```
package com.example.movieswipe.di

@Module
@InstallIn(SingletonComponent::class)
object AppModule {
    // Provide dependencies here
}
```

Unused imports throughout the code.

**Hardcoded Secrets**

Hardcoding secrets in config files:

```
object AuthConfig {
    // TODO: Replace with your actual Google OAuth client ID
    const val GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com"
    // TODO: Replace with your actual backend base URL
    const val BACKEND_BASE_URL = "http://10.0.2.2:3001/api" // Emulator localhost
}
```

**Manifest Misconfiguration**

Missing internet permission in the manifest:

```
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <application
        android:allowBackup="true"
        ...
```

**Insecure Token Storage**

JWT not encrypted when saved:

```
fun saveJwt(jwt: String) {
    prefs.edit().putString("jwt", jwt).apply()
}
```

**Blocking Network Calls**

Performing blocking network calls (highly detrimental to performance, may cause UI hangs):

```
val response = client.newCall(request).execute()
```

---

**Personal Take**

Easier to work with but still not quite there. The process of coming up with the prompts is way too demanding and still not enough for the model to generate the expected output. There are still a lot of things that the model has to decide for itself, which means just knowing what to do is not enough and we need to tell the model how to do things as well. As it seems, the model can't find the best way to do things on its own.
