## UC11: Handle Notification for User Leaving the Group

This document provides a detailed description of the use case UC11: Handle Notification for User Leaving the Group. 

We describe the use case using the following format:

- A description  
- Primary actor(s)  
- Trigger(s)  
- Success scenario(s)  
- Failure scenario(s)

A description is a short summary of the use case. Primary actors(s) are the users or systems that interact with the use case. Trigger(s) are specific events that initiate the use case. A success scenario is a numbered sequence of steps in the normal flow of events in the system. A failure scenario describes what can go wrong in each step of the success scenario and how this is handled. A failure scenario has the same number as its corresponding success scenario.  For example, if a failure scenario corresponds to step 3, it will be numbered 3a; the next failure scenario corresponding to step 3 will be numbered 3b, etc.

### Description

The group owner taps a push notification indicating that a member left the group and is then redirected to the app to view the updated list of members in the group. 

### Primary Actors

- User (group owner)

### Trigger

- User (group owner) taps a push notification indicating that a member left the group.

### Success Scenario

1. The system opens the app and calls the [UC5: ‘View Details of a Group’](UC5_View_Details_of_a_Group.md), displaying the Group Details screen with the updated member list. 

### Failure Scenarios

1a. The system fails to launch the MovieSwipe application. 

- 1a1. User is informed that the app could not be opened. 
