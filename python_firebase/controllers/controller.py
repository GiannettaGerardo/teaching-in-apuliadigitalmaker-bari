import datetime, calendar
from firebase_client import FirebaseClient

class Controller:
  def __init__(self, client: FirebaseClient):
    self._client = client
    
    self.cDay = datetime.datetime.now().day
    self.cMonth = datetime.datetime.now().month
    self.cYear = datetime.datetime.now().year
    self.daysOfTheWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    num_days = calendar.monthrange(self.cYear, self.cMonth)[1]
    days = [datetime.date(self.cYear, self.cMonth, day) for day in range(1, num_days+1)]
    self.table = []
    for day in days:
      completeString = self.printDay(day)
      if self.cDay == day.day:
        completeString = "*** "+completeString+" ***"
      self.table.append([completeString])

  def printDay(self, day) -> str:
    return str(day.day) + " " + self.changeDayNumberInDayName(day.isoweekday())
  
  def changeDayNumberInDayName(self, number: int) -> str:
    if number < 1 or number > 7:
      return "Monday"
    return self.daysOfTheWeek[number - 1]
  
  def printTable(self):
    print("  Current month-year: "+str(self.cMonth)+"-"+str(self.cYear)+"\n")
    for row in self.table:
      print("  " + row[0], end=" ")
      if (len(row) > 1):
        print(row[1])
      else:
        print("")
      print("")