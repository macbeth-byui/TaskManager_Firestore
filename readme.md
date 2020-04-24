# Overview
TaskManager is simple Python program that integrates with FireStore to store simple tasks including: category, status (open/closed), and status.

# Instructions
To run this program:
1) Need to create a Firebase account
2) Need to create a Firebase project.  The project name needs
   to be set in the `initialize_firestore` function.
3) Need to create a Firestore database in Firebase
4) Need to get a Serivce Account Key file (json file) and 
   set the name in the `initialize_firestore` function.  This file should not be stored in a public repository
5) Need to install firebase-admin (`pip install firebase-admin`)

# Useful Links
* https://firebase.google.com/docs/firestore/quickstart
* https://console.firebase.google.com/
* https://console.developers.google.com/
* https://cloud.google.com/docs/authentication/getting-started

# Commands
TaskManager has a simple command line interface.  The commands include the following:

* q,\<o|c|a\>,\<category|*\> - query (o=open, c=closed, a=all)
* c,\<id\> - close
* o,\<id\> - re-open
* i,\<category\>,\<description\> - insert
* d,\<id\> - delete
* u,\<id\>,\<category\>,\<description\> - update
* h - help
* x - exit

The selected query will be remembered until a new query is selected.  The updated list of tasks will be displayed after each command (except the help and exit commands).

Sample table output is shown below:

```
 ID     Category     Status   Description
---   ----------   --------   ------------------------------
  1       cse212       Open   Update Kuali with new outcomes
  2       cse310       Open   Create database example
```