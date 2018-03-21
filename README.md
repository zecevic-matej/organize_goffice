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
  fetch  fetch Google Drive data
  list   list Google Drive data
```
[Requirements.txt contains all necessary dependencies, however, which are all covered within the setup.py for click.]

##### Fetch:
```
Usage: goffice fetch [OPTIONS]

  Fetch a subset or all of the set default documents from Google Drive.

Options:
  -d, --docs TEXT  Each argument represents the name of a specific document to
                   be fetched.
  --help           Show this message and exit.
```
##### List:
```
Usage: goffice list [OPTIONS]

  List a subset or all of the available Google Drive files.

Options:
  -L, --limit INTEGER  Limit to number of files that should be displayed.
  -T, --type           Option that limits view to only documents and
                       spreadsheets.
  --help               Show this message and exit.
```

#### Note
Work in progress (early phase, currently able to fetch a set of documents).
Updated to having a CLI (using click) which will be extended. 
