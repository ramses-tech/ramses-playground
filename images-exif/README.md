# `Images-EXIF`

Example project that consumes images urls and stores them along with EXIF and GPS data.
Project uses mongodb.

## Instalation

```
$ pip install -r requirements.txt
$ cp local.ini.template local.ini
```

## Run
```
$ pserve local.ini
```

## Adding mock data

```
$ nefertari.post2api -f ./mock/Images.json -u http://localhost:6543/api/images
```

This will load about 20 small pictures or Ramses with GPS tags around the world.


## Usage

Project presents a API endpoints ``/api/images`` and ``/api/iamges/{id}``.

Create new image:
POST ``/api/images``. Fields: url, name(optional), location(optional).
If fields "name" or "location" are not present, they are populated using image name/metadata. Field "exif" is populated from image medatadata even if it is present in request. To allow fields "exif", "location" to be populated, image must contain EXIF metadata along with GPS metadata.

List all images:
GET ``/api/images``

List one image:
GET ``/api/images/{id}``

Images objects can also be updated(PATCH, PUT) and deleted(DELETE). Field "url" can not be changed.


## Web usage example

To see simple API usage example:
1. Open ``index.html`` in editor and replace ``YOUR_API_KEY`` with your Google Maps API key.
2. Open ``index.html`` in browser.

Images that have ``location`` field populated will be displayed as markers on the map. Markers show thumbnail of image on click. Thumbnail is a link that leads to original image.
To see image name and creation date/time, hover over the marker.

Regular ramses/nefertari query string params may be used - ``_limit``, ``_sort``, etc. E.g. to increase marker limit to 100, open ``index.html?_limit=100``. No more than 20 first images are displayed initially.