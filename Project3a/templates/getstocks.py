import jinja2

class getstock():
    
    def Stockchoice():
       import csv
       with open('stocks.csv', newline='') as f:
          reader = csv.reader(f)
          data = list(reader)
          
       n = 1
       choicelist = [] 
       for x in data:
          for w in x:
            choicelist.append(w)
       print(choicelist)
          
       return choicelist
    

    
    Stockchoice()
    