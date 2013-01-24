from urlparse import urlparse

def read_model_property(model, key):
  """ This helper method is used to avoid having to explicitly specify
  keys and the 0'th index position each time we want to extract a value. """
  if key in model.properties():
    return model.properties()[key][0]
  else:
    return None

def get_site_id_from_url(site_url):
  components = urlparse(site_url)
  path_components = components.path.split('/')
  return path_components[len(path_components) - 1]