## UC14: Vote for Movies 

This document provides a detailed description of the use case UC14: Vote for Movies.

We describe the use case using the following format:

- A description  
- Primary actor(s)  
- Trigger(s)  
- Success scenario(s)  
- Failure scenario(s)

A description is a short summary of the use case. Primary actors(s) are the users or systems that interact with the use case. Trigger(s) are specific events that initiate the use case. A success scenario is a numbered sequence of steps in the normal flow of events in the system. A failure scenario describes what can go wrong in each step of the success scenario and how this is handled. A failure scenario has the same number as its corresponding success scenario.  For example, if a failure scenario corresponds to step 3, it will be numbered 3a; the next failure scenario corresponding to step 3 will be numbered 3b, etc.

### Description

A user can join the voting session for a group they own or have joined. In the voting session, the group owner and group members indicate their movie interests by swiping right for “interested” or swiping left for “not interested” on each movie card. Each movie card displays movie metadata. The user can also exit the voting session they are in and have their voting results recorded, and then resume the voting session if they exited before swiping on all movies. 

### Primary Actor

- User

### Triggers

- User taps the “Join Voting Session” button on the Group Details screen.  
- User taps the “Resume Voting Session” button on the Group Details screen.

### Success Scenario

1. The system redirects User to the voting screen, with a movie card showing the first recommended movie (title, poster, genre, rating, length, and summary) that User has not yet swiped on. The screen also includes an “Exit Voting Session” button.   
2. If User taps the “Exit Voting Session” button, the system calls the [UC5: ‘View Details of a Group’](UC5_View_Details_of_a_Group.md), displaying the Group Details screen.  
3. Otherwise, User swipes right (interested) or left (not interested) on the displayed movie card.   
4. If there are additional movie cards left to vote on, the system advances to the next movie card after the user votes and step 2 repeats.   
5. If no movie cards are left, the system  presents a confirmation message for finishing voting for all movies and then calls the [UC5: ‘View Details of a Group’](UC5_View_Details_of_a_Group.md), displaying the Group Details screen.

### Failure Scenarios 

1a. The voting session is no longer active.

- 1a1. The system displays an error message "The voting session has ended."  
- 1a2. The system calls the [UC5: ‘View Details of a Group’](UC5_View_Details_of_a_Group.md), displaying the Group Details screen, with the updated voting session state.

2a. The system fails to exit the voting session. 

- 2a1. The system displays an error message "Failed to exit the voting session. Please try again.”  
- 2a2. The system continues to present the Voting screen with the current movie card. 

3a. User applies invalid swiping gestures such as up or down. 

- 3a1. The system displays an error message "Swipe right for ‘interested’ or left for ‘not interested’. No other swiping gesture allowed.".  
- 3a2. The system continues to present the Voting screen with the current movie card.
