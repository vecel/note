# Notecli

A `notecli` is a simple command-line interface (CLI) for managing personal notes. With `note` command, you can easily create, store, and tag your notes directly from your terminal.

## Description
The `notecli` application is a tool to manage notes, ideas and thoughts related to project. It creates a repository file in the directory where the command was called (similar to `git`). The app offers a simple interface to add, edit, delete and list notes. It allows you to add tags and statuses to enhance clarity and readability of notes. You can create custom statuses with own display styles and priorities.

## Installation

To install the application run:

```bash
pip install notecli
```

Then call the CLI via `note` command:

```bash
note --version
```

You should see output:

```bash
notecli v0.1.1
```

To see all available commands and options run:

```bash
note --help
```

## Usage
First go to the directory where you want to store notes and call:

```bash
note init
```

>
> **Tip:** You can have many repositories, for example one for each project you are working on.
>

Then add your first note:

```bash
note add "Hello notecli!"
```
 
 To see this note run:

 ```bash
 note list
 ```

 You should see the output like this:

 ```bash
                                       Your Notes                                           
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ ID ┃ Content                                     ┃ Status       ┃ Tags          ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ 1  │ Hello notecli!                              │ -            │ -             │
└────┴─────────────────────────────────────────────┴──────────────┴───────────────┘
 ```

 You can add a note with custom tags, to do so run:

 ```bash
 note add "Hello tags!" -t firsttag,cool
 ```

You will create new note with content "Hello tags!" with two tags: **#firsttag** and **#cool**.

To create custom status call *status* command:

```bash
note status --add COMPLETED --style "bold green" --priority 2
```

This will add new status you can assign to notes. It will be displayed with bold green style. Notes with this status will be displayed above others because of priority, all notes are sorted by priority with descending order.

Now create another note and make use of newly created status:

```bash
note add "Hello status!" -s COMPLETED
```

When you run `note list` you should see following output:

```bash
                                    Your Notes                                              
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ ID     ┃ Content                          ┃ Status           ┃ Tags             ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ 1      │ Hello status!                    │ COMPLETED        │ -                │
│ 2      │ Hello notecli!                   │ -                │ -                │
│ 3      │ Hello tags!                      │ -                │ #firsttag #cool  │
└────────┴──────────────────────────────────┴──────────────────┴──────────────────┘
```

>
> **Attention:** As you can see COMPLETED status is white here, it is because of markdown styling. You should see it as bold, green text. Tags should be violet in your console. 
>