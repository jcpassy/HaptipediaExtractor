# Haptipedia Extractor
A python wrapper for extracting metadata, text, section titles, figures, and references from Haptic Device Research Papers.
Uses PDFFigures2.0 for extraction of figures and figure captions and GROBID for extraction of references, section text and titles.
Also has a cross-reference function to find connections between given paper inputs (which papers cited each other and how many times, shared authors and references between papers).

For More Information:
https://haptipediaextractor.readthedocs.io/en/latest/


## Prereqs
1. Python 3.7+

## Dependencies

### GROBID
Grobid is used to extract metadata, text and citations from PDF files. Grobid should be running as a service somwhere. (See Grobid's Github project for more complete installation instructions.)

### PDFFigures2.0
Pdffigures2.0 is used to extract figures, tables and captions from PDF files. It should be installed as directed by the pdffigures2 Github page. The path to the pdffigures2 binary can be configured in ConfigPaths.py

## Installation

1. Clone the repo on the machine
2. Create and activate your virtual environment
3. Install the python dependencies:
    ```
    $ cd HaptipediaExtractor
    $ pip install -r requirements.txt
    ```
4. Have GROBID running in the background somewhere

## Usage

From the root directory, run
```
$ python3 src/main.py -i /path/to/folder/with/pdfs -o /path/to/output -d /path/to/pdffigures2
```

## Dockerization

It is easier to run the application in a Docker container.

You can build the Docker image from the `Dockerfile` using `docker-compose`:
```
$ docker-compose build
```

and then start a container:
```
docker-compose up -d
```

To stop the container
```
docker-compose down
```

The addresses [http://localhost:8080](http://localhost:8080) and [http://localhost:8081](http://localhost:8081) should then be accessible (more details on the GROBID official documentation).

Finally, you can attach a shell to the container and run the extractor:
```
root@containerid $ cd /src/HaptipediaExtractor
root@containerid $ python3 src/main.py -i /container/path/to/folder/container/pdf -o /path/to/output/folder -d /path/to/pdffigures2
```

for instance, if you use the default environment variables:

```
root@containerid $ python3  src/main.py -i /tmp/haptipedia/input -o /tmp/haptipedia/output -d /work/src/pdffigures2
```

## Tests

You can run the extracition test inside the container by doing:

```
root@containerid $ python3 -m unittest
```
