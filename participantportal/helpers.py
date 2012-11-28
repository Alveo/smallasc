def read_model_property(model, key):
  """ This helper method is used to avoid having to explicitly specify
  keys and the 0'th index position each time we want to extract a value. """
  if key in model.properties():
    return model.properties()[key][0]
  else:
    return None