
# This search application uses an RDF store as it's repository
# And in this instance we use SPARQL to query the repository or
# endpoint. The information below is the configuration data for
# the RDF store

# Original Sparql endpoint address
SPARQL_ENDPOINT_ADDR = "115.146.93.47"
# SPARQL_ENDPOINT = "http://115.146.94.199/openrdf-sesame/repositories/bigasc"
SPARQL_ENDPOINT = "http://%s/openrdf-sesame/repositories/bigasc" % (SPARQL_ENDPOINT_ADDR)