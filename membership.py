
class Membership(object):
  def __init__(self, database):
    self.db = database
    self.__children = set()

    # parent code?
    self.__parent = None
  def join(self, addr, uuids):
    self.__children.add(addr)
    self.db.addChild(addr, uuids)

  def leave(self, addr):
    self.db.leaveChild(addr)
    self.__children.remove(addr)

  def children(self):
    return self.__children

  def parent(self):
    return self.__parent

  def find(self, uuid):
    return self.db.find(uuid)


