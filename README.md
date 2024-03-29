# Quickstart

## Usage

To start the application, run the following command:

```bash
docker compose up --build
```

Then, go to http://localhost:8000/sdcc_compiler/ to view the application.

## Cleanup

```bash
docker compose down
docker volume rm awwprojekt_media awwprojekt_static
```

To remove images, first list them using:

```bash
docker images
```

Then, remove them using:

```bash
docker rmi <image_id>
```

## Admin info

Superuser
- username: alek
- password: alek

User 1
- username: ironman
- password: tonystark

User 2
- username: hulk
- password: brucebanner

## User actions

1. Click on a file / directory to select it
2. Click on it again to unselect it
3. Double-click on a file to open it in editor

## File operations
If no file / directory is selected, the default parent is root directory.

## Sections
To view the sections of a file, first open it in the editor.

## Compilation
- To compile a file, you have to open it in the editor first.
- Then you can choose compilation options in the tab menu.
- After choosing processor architecture, the dependent options will be updated accordingly.
- Click on the compile button to compile the file, and view it in code fragment on the right.
- Then, you will be able to download the output.asm file.