[![Build Status](https://travis-ci.com/AtomsForPeace/aiojena.svg?branch=master)](https://travis-ci.com/AtomsForPeace/aiojena)

# aiojena

An asynchronous python wrapper on top of aiosparql specifically for [Apache Jena](https://jena.apache.org/).

```python
from aiojena.client import JenaClient


# One showcase function with all the main features:
async def showcase():
    jena_client = JenaClient("<your_sparql_endpoint>")
    
    # Add a label to a URI using the udpate function
    # The first argument is the query string and the second argument is the params
    await jena_client.update(
        """
        INSERT DATA {{
          <https://test.com> <http://www.w3.org/2000/01/rdf-schema#:label> {label}  .
        }}
        """, {
            'label': 'This is a label'
        }
    )
    
    # Get the label of a URI using the query function
    results = await jena_client.query(
        """
        SELECT ?label
        WHERE {{
          <https://test.com> <http://www.w3.org/2000/01/rdf-schema#:label> ?label  .
        }}
        """
    )
    len(results) == 1  # True
    # The result is returned as a python str object 
    results[0]['label'] == 'This is a label'  # True
        
    # Dealing with URI objects with rdflib.URIRef
    from rdflib import URIRef
    test_uri_object = URIRef('https://test.com')
    results = await jena_client.query(
        """
        SELECT ?label
        WHERE {{
          {test_uri_object} <http://www.w3.org/2000/01/rdf-schema#:label> ?label  .
        }}
        """, {
            'test_uri_object': test_uri_object
        }
    )
    len(results) == 1  # True
    results[0]['label'] == 'This is a label'  # True
    
    # Passing tuples and finding the subject from our first example
    from rdflib import URIRef
    rdfs_label = URIRef('http://www.w3.org/2000/01/rdf-schema#:label')
    test_labels = ('This is a label', 'This is also a label')
    results = await jena_client.query(
        """
        SELECT ?subject
        WHERE {{
          ?subject {rdfs_label} ?label  .
          FILTER(?label IN {test_labels})
        }}
        """, {
            'rdfs_label': rdfs_label,
            'test_labels': test_labels
        }
    )
    len(results) == 1  # True
    results[0]['subject'] == URIRef('https://test.com')  # True

```

## To test
Have a test instance of Fuseki running. Be aware that testing requires modification and deletion of the RDF store. Set the address of Fuseki in the testing.cfg. 

```
pip install -r test-requirements.txt
pip install -r requirements.txt
```
Run pytest tests/
