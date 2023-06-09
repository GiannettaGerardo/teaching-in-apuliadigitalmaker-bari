from views.viewinterface import ViewInterface
from views.authview import AuthView
from firebase_client import FirebaseClient

class ViewStack:
  """Class that implement a secured stack for only ViewInterface instances."""
  def __init__(self, firstView: ViewInterface=None):
    self._viewStack = []
    if firstView != None:
      if not isinstance(firstView, ViewInterface):
        raise ValueError('ViewInterface allowed only')
      self._viewStack.append(firstView)
  
  def push(self, value: ViewInterface):
    if not isinstance(value, ViewInterface):
      raise ValueError('ViewInterface allowed only')
    self._viewStack.append(value)
  
  def pop(self) -> ViewInterface:
    return self._viewStack.pop()
  
  def get(self) -> ViewInterface:
    return self._viewStack[-1]
  
  def isEmpty(self) -> bool:
    return len(self._viewStack) == 0


def main():
  """ViewStack based algorithm."""
  try:
    client = FirebaseClient(".\\configuration\\config.json")
    viewStack = ViewStack(AuthView(client))
    while not viewStack.isEmpty():
      currentView = viewStack.get()
      newView = currentView.render()
      if newView != None:
        viewStack.push(newView)
      else:
        viewStack.pop()
  except KeyboardInterrupt:
    pass
  print("Exit in progress...")

if __name__ == "__main__":
  main()