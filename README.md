# organize_goffice
Feel free to use and modify this to organize your Google "Office" (Docs, Sheets, etc.) a bit easier.

#### Setup
Create a virtual environment, activate it and finally install the CLI using:
```
$ virtualenv venv
$ . venv/bin/activate
$ pip install --editable .
```
After that you will be able to run following command:
```
Usage: goffice [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  fetch   Allows for fetching of Google Drive docs
  update  TODO: a function for updating
```
[Requirements.txt contains all necessary dependencies, however, which are all covered within the setup.py for click.]

#### Note
Work in progress (early phase, currently able to fetch a set of documents).
Updated to having a CLI (using click) which will be extended. 
