from SPARQLWrapper import SPARQLWrapper,JSON
class ConnectEnd(object):
	def __init__(self, endpoint, sparqlString):
		self.endpoint=endpoint
		self.sparqlString=sparqlString

	def Connect(self):
	    sparql=SPARQLWrapper(self.endpoint) # The endpoint of Bio2RDF
	    sparql.setQuery(self.sparqlString)
	    sparql.setReturnFormat(JSON)
	    results = sparql.query().convert()
	    return results