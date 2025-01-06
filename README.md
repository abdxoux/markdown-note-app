# Markdown Note App

## Overview
The Markdown Note App is a simple application that allows users to create, save, and manage notes in Markdown format. The app provides a user-friendly GUI for note-taking and previewing Markdown content.

## Features
- User authentication (login and registration)
- Create, save, and delete notes
- Preview notes in Markdown format
- User-friendly GUI

## Dependencies
- `customtkinter`
- `sqlite3`
- `hashlib`
- `datetime`
- `markdown`

## Architecture

The Markdown Note App follows a modular architecture with the following main components:

1. **GUI Layer**: Handles the user interface and user interactions.
    - `AppGUI.py`: Contains the `MarkdownAppGUI` class which manages the main application window, user authentication, and note management.

2. **Authentication Layer**: Manages user authentication and session handling.
    - `authenticate.py`: Contains the `Auth` class which handles user login, registration, and logout functionalities.

3. **Data Layer**: Manages data storage and retrieval.
    - `database.py`: Contains functions for interacting with the SQLite database, including saving, retrieving, and deleting notes.
    - `DatabaseManager.py`: Manages the database connection and operations.
    - `UserManager.py`: Manages user-related database operations.
    - `NoteManager.py`: Manages note-related database operations.

4. **Utilities**: Provides utility functions and helpers.
    - `hash_password`: A function for hashing passwords.
    - `markdown`: A library for converting Markdown content to HTML.

### File Structure 
### Diagram


markdown-note-app/
│
├── database.py
├── AppGUI.py
├── main.py
└── markdown_app.db
