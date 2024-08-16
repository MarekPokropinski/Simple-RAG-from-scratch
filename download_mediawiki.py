import requests

url = 'https://vampire-survivors.fandom.com/api.php'
target_directory = "vs_data"

def query(request):
    request['action'] = 'query'
    request['format'] = 'json'
    last_continue = {}
    while True:
        # Clone original request
        req = request.copy()
        # Modify it with the values returned in the 'continue' section of the last result.
        req.update(last_continue)
        # Call API
        result = requests.get(url, params=req).json()
        if 'error' in result:
            raise Exception(result['error'])
        if 'warnings' in result:
            print(result['warnings'])
        if 'query' in result:
            yield result['query']
        if 'continue' not in result:
            break
        last_continue = result['continue']


q = query({'generator': 'allpages'})
all_pages = list(q)
result = {}
for d in all_pages:
    result.update(d['pages'])
titles = [
    value['title']
    for value in result.values()
]

pages_data = [
    list(query({'titles': title, 'prop': 'revisions', 'rvprop':'content', 'rvslots':'main'}))
    for title in titles
]

pages_content = {}
for page in pages_data:
    title = list(page[0]['pages'].values())[0]['title']
    content = list(page[0]['pages'].values())[0]['revisions'][0]['slots']['main']['*']
    if content.lower().startswith('#redirect '): continue
    pages_content[title] = content

for page in pages_content:
    filename = page.replace('/', ' ')  # remove / from filenames. For more robust solution should remove all invalid characters for file name
    with open(f'{target_directory}/{filename}', 'w') as f:
        f.write(pages_content[page])