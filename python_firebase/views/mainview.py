import os
from firebase_client import FirebaseClient
from views.viewinterface import ViewInterface
from controllers.controller import Controller

class MainView:
  def __init__(self, client: FirebaseClient):
    self._controller = Controller(client)

  def printMenu(self):
    print("    Welcome " + self._controller._client.getEmail())
    print(" ||----------------------------------------------------||")
    print(" ||                     Main menù                      ||")
    print(" || Enter a number to choose an action.                ||")
    print(" || [1] Back                                           ||")
    print(" || [2] Show orders of this month                      ||")
    print(" || [3] Insert new order by day number                 ||")
    print(" || [4] Delete order by day number and order number    ||")
    print(" ||----------------------------------------------------||")
  
  def parse_input(self, value: int):
    if value == 1:
      return 0
    elif value == 2:
      self._controller.printTable()
      return None
    elif value == 3:
      return None
    elif value == 4:
      return None
  

  def render(self) -> (ViewInterface | None):
    return ViewInterface.inputLoop(self.printMenu, self.parse_input)