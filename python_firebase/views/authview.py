from firebase_client import FirebaseClient
from views.viewinterface import ViewInterface
from views.mainview import MainView
from getpass import getpass

class AuthView:
  def __init__(self, client: FirebaseClient):
    self._client = client

  def printMenu(self):
    if self._client.isLoggedIn():
      print("    Welcome " + self._client.getEmail())
      print(" ||----------------------------------------------------||")
      print(" ||                Authentication menù                 ||")
      print(" || Enter a number to choose an action.                ||")
      print(" || [1] Back                                           ||")
      print(" || [2] Logout                                         ||")
      print(" || [3] Go to the main menù                            ||")
      print(" ||----------------------------------------------------||")
    else:
      print("    Welcome")
      print(" ||----------------------------------------------------||")
      print(" ||                Authentication menù                 ||")
      print(" || Enter a number to choose an action.                ||")
      print(" || [1] Back                                           ||")
      print(" || [2] SignUp                                         ||")
      print(" || [3] SignIn                                         ||")
      print(" ||----------------------------------------------------||")
  
  def parse_input(self, value: int):
    if value == 1:
      return 0
    elif value == 2:
      if self._client.isLoggedIn():
        self._client.logout()
      else:
        if self._sign(self._client.signUp, "Error. User not created..."):
          return MainView(self._client)
    elif value == 3:
      if self._client.isLoggedIn():
        return MainView(self._client)
      elif self._sign(self._client.signIn, "Incorrect credentials..."):
        return MainView(self._client)
      
  def _sign(self, clientFunction, errorMessage) -> bool:
    """Generic function to implement both signUp and signIn."""
    print("Enter email: ", end="")
    email = input()
    password = getpass("Enter password: ")
    try:
      clientFunction(email, password)
      return True
    except:
      print(errorMessage)
    return False


  def render(self) -> (ViewInterface | None):
    return ViewInterface.inputLoop(self.printMenu, self.parse_input)
