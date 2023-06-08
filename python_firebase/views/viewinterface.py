import abc
from collections.abc import Callable

class ViewInterface(metaclass=abc.ABCMeta):
  """Interface for the views."""
  @classmethod
  def __subclasshook__(cls, subclass):
    return (hasattr(subclass, 'render') and 
            callable(subclass.render))
  
  def inputLoop(printMenu: Callable, parseInput: Callable):
    """
    Implement the main loop for all the input parsing.\n
    ``parseInput`` is a function and must return:
    - 0 : means return 'Back'
    - None : means 'do nothing'
    - ViewInterface instance : means return 'the instance'
    """
    while True:
      try:
        printMenu()
        print(">> ", end="")
        value = int(input())
        result = parseInput(value)
        if result == 0:
          return None
        elif isinstance(result, ViewInterface):
          return result
      except ValueError:
        print("Invalid number. Retry...")
      print("")