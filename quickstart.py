from __future__ import print_function
import httplib2
import os
import sys, io
#print(sys.stdout.encoding)
reload(sys)
sys.setdefaultencoding("utf-8")
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaIoBaseDownload
import click

@click.group()
def cli():
    pass
    #click.echo("Hello World!")

# important:
# have code like this
# enable API rights like in tutorial
# have google api client installed
# python2.7 etc.

# set data names
def_docs = ['accounts', 'timeline', 'masters', 'finance']
# set pagesize
N = 10

# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/drive']
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

@click.command()
@click.option('--docs','-d', multiple=True, default=def_docs)
def fetch(docs):
#def main():
    """
    Allows for fetching of Google Drive docs
    """
    if docs != def_docs:
        click.echo("Fetching following docs:")
        click.echo(docs)
    else:
        click.echo("Fetching default docs.")


    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    results = service.files().list(
        pageSize=N,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
			print('{0} ({1})'.format(item['name'], item['id']))
			if item['name'] in docs: 
				file_id = item['id'] #items[0]['id'] #'1ZdR3L3qP4Bkq8noWLJHSr_iBau0DNT4Kli4SxNc2YEo'
				request = service.files().export_media(fileId=file_id,
															 mimeType='application/pdf')
				fh = io.FileIO(str(item['name']) + ".pdf", "w") #BytesIO()
				downloader = MediaIoBaseDownload(fh, request)
				done = False
				while done is False:
					status, done = downloader.next_chunk()
					print("Download %d%%." % int(status.progress() * 100))

@click.command()
def update():
    'TODO: a function for updating'
    click.echo('Finished updating.')

cli.add_command(fetch)
cli.add_command(update)

if __name__ == '__main__':
    cli()

