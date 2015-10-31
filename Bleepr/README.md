## Requirements
- python 2.7 or 3.4
- virtualenv
- (Posgresql)
- Elasticsearch

## Installation
```
$ pip install -r requirements.txt
$ cp local.ini.template local.ini
$ nano local.ini
```
(edit [twitter] and [paypal] sections)

## Run the API
```
$ pserve local.ini
```

## In another terminal
```
$ python get_tha_bleeps.py
```
