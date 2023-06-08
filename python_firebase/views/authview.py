from my_firebase_client import FirebaseClient
from views.viewinterface import ViewInterface
from views.mainview import MainView

class AuthView:
  def __init__(self, client: FirebaseClient):
    self._client = client

  def printMenu(self):
    print("    Welcome")
    print(" ||----------------------------------------------------||")
    print(" ||                        Menù                        ||")
    print(" || Enter a number to choose an action.                ||")
    print(" || [1] Back                                           ||")
    print(" || [2] SignUp                                         ||")
    print(" || [3] SignIn                                         ||")
    print(" ||----------------------------------------------------||")
  
  def parse_input(self, value: int):
    if value == 1:
      return 0
    elif value == 2:
      if self._sign(self._client.signUp, "Error. User not created..."):
        return MainView(self._client)
    elif value == 3:
      if self._sign(self._client.signIn, "Incorrect credentials..."):
        return MainView(self._client)
      
  def _sign(self, clientFunction, errorMessage) -> bool:
    print("Enter email: ", end="")
    email = input()
    print("Enter password: ", end="")
    password = input()
    try:
      clientFunction(email, password)
      return True
    except:
      print(errorMessage)
      return False


  def render(self) -> (ViewInterface | None):
    return ViewInterface.inputLoop(self.printMenu, self.parse_input)