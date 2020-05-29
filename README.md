# Advanced System Design - Cortex Project
Welcome to the Github page of the Advanced System Design project by Raghad Zeidan.
Quickstart explanation:
  The final project includes a client, which streams cognition snapshots to a server, 
  which then publishes them to a message queue, where multiple parsers read the snapshot,
  parse various parts of it, and publish the parsed results, which are then saved to a database.
  The result in the database is then reflected by an API, CLI and GUI.

In order to receive full documentation of the function, sphinx functionality has been added and
can be accessed by running:
    "python -m http.server" inside cortex/docs/_build/html repository
  
  
