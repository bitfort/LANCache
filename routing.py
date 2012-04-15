

class Router(object):
  def __init__(membership):
    self.membership = membership
  def route(uuid):
    d = self.membership.find(uuid)
    if d is not None:
      return d

    p = self.membership.parent()
    if p is None:
      return None
    return p.route(uuid)
    

