import calendar
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
    print(" || [4] Delete order by day number and order Id        ||")
    print(" ||----------------------------------------------------||")

  def _insertOrder(self) -> tuple[dict, int]:
    num_days = calendar.monthrange(self._controller.cYear, self._controller.cMonth)[1]
    while True:
      data = {}
      try:
        print("Enter the day number: ", end="")
        day = int(input())
        if day < 1 or day > num_days:
          raise ValueError()
        
        print("Enter customer: ", end="")
        data["customer"] = input()

        print("Enter worked hours: ", end="")
        data["hours"] = int(input())
        if data["hours"] < 1 and data["hours"] > 24:
          raise ValueError()
        
        return (data, day) 
      except ValueError:
        print("Error: invalid data. Retry...\n")

  def _deleteOrder(self) -> tuple[int, str]:
    num_days = calendar.monthrange(self._controller.cYear, self._controller.cMonth)[1]
    while True:
      try:
        print("Enter the day number: ", end="")
        day = int(input())
        if day < 1 or day > num_days:
          raise ValueError()

        print("Enter the order Id: ", end="")
        orderId = input()

        return (day, orderId)
      except ValueError:
        print("Error: invalid data. Retry...\n")
  
  def parse_input(self, value: int):
    if value == 1:
      return 0
    elif value == 2:
      table = self._controller.getTable()
      for row in table:
        print("  " + row, end="\n\n")
    elif value == 3:
      (data, day) = self._insertOrder()
      self._controller.insertOrder(data, day)
    elif value == 4:
      (day, orderId) = self._deleteOrder()
      self._controller.deleteOrder(day, orderId)
    return None
  

  def render(self) -> (ViewInterface | None):
    return ViewInterface.inputLoop(self.printMenu, self.parse_input)