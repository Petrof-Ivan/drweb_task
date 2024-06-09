## drweb_task

The project uses SQLAlchemy and SQLite database to store authorization credentials and hashes.

The server starts at localhost and provides an address http://127.0.0.1:5000/api/ for API use.

## How to run
You might want to use a virtual environment first.

Then:

```pip install -r requirements.txt```

`python server.py`

## Examples testing with cURL

Post request example (upload):

`curl -i -X POST -H "Content-Type: multipart/form-data" -u "user:1234" -F "file=@tz.txt" http://127.0.0.1:5000/api/`

Get request example (download):

`curl -X GET -o "" -F "data=" http://127.0.0.1:5000/api/`

`curl -X GET -o "f70404b77adaf978f2015a8f927cef4976a2769c1e869352cde67ec18423cce7" -F "data=f70404b77adaf978f2015a8f927cef4976a2769c1e869352cde67ec18423cce7" http://127.0.0.1:5000/api/`

Delete request example:

`curl -i -X DELETE -F "data=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" -u "user1:1234" http://127.0.0.1:5000/api/`

Please, replace entities with actual values.
