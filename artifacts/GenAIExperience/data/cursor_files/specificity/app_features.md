# Description

The name of the app is MovieSwipe. In the app, a user can create a group and invite other users to join the group via an invitation code. The group owner can also delete the group. Upon joining a group, users are asked to specify what genres of movies they like (comedy, horror, action, etc.). The group owner can then start a voting session and the app shows 10 movie recommendations that group members can swipe right for “interested” or left for “not interested”. MovieSwipe’s smart recommendation system looks at everyone’s choices and finds the best match that most people will be happy with. When voting ends, the app shows the winning movie with its details to everyone in the group.

We intend the app to use Google authentication, the TMDB external API to retrieve a set of movies by genre, Firebase Cloud Messaging to notify group members when the owner starts and ends the voting session via push notification, and Socket.IO to automatically update the user interface in several places (live updates), e.g., when a member joins or leaves a group.


# Features

* 1. Manage Authentication: A user must sign up for the app on the first use and then sign in for each session using Google Authentication Service. An authenticated user can sign out or delete their account altogether.

* 2. Manage Groups: A user can create a group and become its owner. When creating a group, the group owner provides the group name and specifies their movie genre preferences. The list of genres is retrieved from the TMDB API. After creating the group, the group owner can view group details such as the group name, a unique invitation code for member recruitment, and their role in the group (“owner”). The group owner can also delete groups they own. Any user can view a list of active groups they own or have joined and details about these groups. Once a user joins or leaves a group, the list of members is automatically updated on every open screen.

* 3. Manage Group Membership: A user can join a group using the invitation code shared by the group owner and become a group member. When joining, the user must specify their movie genre preferences, selecting from the list of genres specified for the group by its owner. The user can leave the group at any time, if they wish.

* 4. Manage Voting Session: The group owner can start a voting session, triggering the app to generate a list of 10 recommended movies, based on all members’ genre preferences. Once the list is ready, the app sends, via Firebase Cloud Messaging, real-time notifications to all members announcing the start of the voting session. Group members can tap the notification to be redirected to the app to join the voting session. The group owner can end the voting session, triggering the app to analyze votes and determine the winning movie. The app then sends push notifications to all group members via Firebase Cloud Messaging. When group members tap the notification, the app displays the winning movie, along with the details of the movie.

* 5. Vote for Movie: In the voting session, each group member indicates their movie preferences by swiping right for “interested” or left for “not interested” on each movie card. Movie cards display movie metadata. Users can exit the voting session and have their voting results recorded, then resume the voting session if they exited before ranking all movies.