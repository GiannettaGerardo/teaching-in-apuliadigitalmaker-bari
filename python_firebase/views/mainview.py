from my_firebase_client import FirebaseClient
from views.viewinterface import ViewInterface

class MainView:
  def __init__(self, client: FirebaseClient):
    self._client = client

  def printMenu(self):
    print("    Welcome")
    print(" ||----------------------------------------------------||")
    print(" ||                        Menù                        ||")
    print(" || Enter a number to choose an action.                ||")
    print(" || [1] Back                                           ||")
    print(" ||----------------------------------------------------||")
  
  def parse_input(self, value: int):
    if value == 1:
      return 0
    elif value == 2:
      return None
    #if client.isLoggedIn():
     # pass
  

  def render(self) -> (ViewInterface | None):
    return ViewInterface.inputLoop(self.printMenu, self.parse_input)