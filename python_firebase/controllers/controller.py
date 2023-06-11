import datetime, calendar
from firebase_client import FirebaseClient
import json as jsonModule

class Controller:
  def __init__(self, client: FirebaseClient):
    self._client = client
    
    self.cDay = datetime.datetime.now().day
    self.cMonth = datetime.datetime.now().month
    self.cYear = datetime.datetime.now().year
    self.daysOfTheWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    num_days = calendar.monthrange(self.cYear, self.cMonth)[1]
    days = [datetime.date(self.cYear, self.cMonth, day) for day in range(1, num_days+1)]
    self.daysOfMonth = []
    for day in days:
      completeString = self._getDayOfMonthAndWeekAsStr(day)
      if self.cDay == day.day:
        completeString = "***** "+completeString+" *****"
      self.daysOfMonth.append(completeString)

  def _getDayOfMonthAndWeekAsStr(self, day) -> str:
    return str(day.day) + " " + self._changeDayOfWeekNumberInName(day.isoweekday())
  
  def _changeDayOfWeekNumberInName(self, number: int) -> str:
    if number < 1 or number > 7:
      return "Monday"
    return self.daysOfTheWeek[number - 1]
  
  def getTable(self) -> list[str]:
    responseDict = self._getOrderOfThisMonth()
    daysIndex = 1
    result = ["Current month-year: "+str(self.cMonth)+"-"+str(self.cYear)]
    if responseDict is None:
      for row in self.daysOfMonth:
        result.append(row)
      return result
    
    for row in self.daysOfMonth:
      strIndex = str(daysIndex)
      if strIndex in responseDict:
        ordersDict = responseDict[strIndex]
        result.append(row + ": " + jsonModule.dumps(ordersDict, indent=2))
      else:
        result.append(row)
      daysIndex += 1
    return result
  
  def insertOrder(self, data: dict, day: int) -> None:
    databaseCursor = str(self.cYear)+"/"+str(self.cMonth)+"/"+str(day)
    self._client.post(data, databaseCursor)

  def _getOrderOfThisMonth(self) -> dict:
    databaseCursor = str(self.cYear)+"/"+str(self.cMonth)
    return self._client.get(databaseCursor)
  
  def deleteOrder(self, day: int, orderId: str):
    databaseCursor = str(self.cYear)+"/"+str(self.cMonth)+"/"+str(day)
    if orderId != "":
      databaseCursor = databaseCursor+"/"+orderId
    self._client.delete(databaseCursor)