import time

class Date:
  def dateFormatted(self, format = '2022-01-01 %H:%M:%S'):
    datetime = time.localtime()
    formatted = time.strftime(format, datetime)
    return formatted