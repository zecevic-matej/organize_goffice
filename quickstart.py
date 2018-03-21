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
@click.pass_context
def cli(ctx):
    ctx.obj = {}
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    ctx.obj['SERVICE'] = service
    pass

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

@click.command(short_help='fetch Google Drive data')
@click.option('--docs','-d', multiple=True, default=def_docs, help='Each argument represents the name of a specific document to be fetched.')
@click.pass_context
def fetch(ctx, docs):
#def main():
    'Fetch a subset or all of the set default documents from Google Drive.'
    if docs != def_docs:
        click.echo("Fetching following docs:")
        click.echo(docs)
    else:
        click.echo("Fetching default docs.")

    service = ctx.obj['SERVICE']


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

@click.command(short_help='list Google Drive data')
@click.option('--limit','-L', type=int, help='Limit to number of files that should be displayed.')
@click.option('--type', '-T', is_flag=True, help='Option that limits view to only documents and spreadsheets.')
@click.pass_context
def list(ctx, limit, type):
    'List a subset or all of the available Google Drive files.'
    click.echo('LISTING GOOGLE DRIVE DOCUMENTS.')
    service = ctx.obj['SERVICE']
    if limit:
        results = service.files().list(pageSize=limit, fields="nextPageToken, files(id, name, mimeType)").execute()
    else:
        results = service.files().list(fields="nextPageToken, files(id, name, mimeType)").execute()
    items = results.get("files", [])
    if not items:
        print("No files found.")
    else:
        print("Files:")
        for item in items:
            if type and ('document' in item['mimeType'] or 'spreadsheet' in item['mimeType']):
                print('{0} ({1}) [{2}]'.format(item['name'], item['id'], item['mimeType']))
            elif type:
                continue
            else:
                print('{0} ({1}) [{2}]'.format(item['name'], item['id'], item['mimeType']))


cli.add_command(fetch)
cli.add_command(list)

if __name__ == '__main__':
    cli()

