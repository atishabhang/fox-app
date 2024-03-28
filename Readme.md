# FOX Python App


1. Run `fetch_emails.py` to get all emails from gmail account.
2. Run `process_emails.py` to do operations based on rules mentioned in `rules.json`

Dockerfile is provided but since browser is not accessible in docker, library gives the `could not locate runnable browser python docker` 


### `fetch_emails.py`

* It fetches all emails from gmail account and stores it in `sqliteDB`
* To allow fetching the emails, user have to authorize the program to allow fetching the emails using OAuth2.
* `sqliteDB` file called `emails.db` is created after program successfully fetch emails.
* structure of Email object is as following.

```CPP
struct Email{
    id              string
    sender          string
    subject         string
    received_at     string
}
```


### `process_emails.py`

* It fetches records from `emails.db` sqliteDB
* Decide the operations to perform on each email by analysing `rules.json`
* Make request to `Gmail API` using google apis.


#
### Running in docker
```Dockerfile
docker build -t happy-fox .
docker run happy-fox fetch_emails.py
docker run happy-fox process_emails.py
```