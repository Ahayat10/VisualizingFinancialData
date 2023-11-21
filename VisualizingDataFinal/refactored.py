import csv
from queue import PriorityQueue
from datetime import datetime
import calendar
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
class Transactions:

    def __init__(self, date, transaction, category, amount):
        self.date = date
        self.transaction = transaction
        self.category = category
        self.amount = amount
    
    #this allows for two instances of the class to be compared using less than operator
    def __lt__(self, other):
        #Compare Transactions based on their priority
        return datetime.strptime(self.date, "%m/%d/%y") < datetime.strptime(other.date, "%m/%d/%y")

class TransactionsManager:

    def __init__(self,entries):
        self.entries = entries
        self.priority_queue = PriorityQueue()
        self.category = {} #dictionary for all category types
        #self.cat_sums = []
        #self.cat_prio_sums = []
        self.monthlybill = [] #Used for bar graph bill
        self.monthlypaid = [] #Used for bar graph paid
        self.daybill = [] #extracts indivudal bill amts on days
        self.bill_dates = [] #Extracts individual bill dates on days
        self.daypaid = [] #extracts indivudal bill paid amts on days
        self.paid_dates = [] #Extracts individual paid dates on days
        self.type = ["Merchandise", "Gas/Automotive","Dining","Health Care", "Payment/Credit",
                    "Internet","Fee/Interest Charge","Entertainment","Others"]
        #self.priority = priority
        #self.print_entries()
        self.categorize()
        #self.add_transactions(priority)
    
    def categorize(self): #Generates lists and stores all info from csv
        
        for catType in self.type:
            self.category[catType] = [] #creates an empty list for each category type

        for entry in self.entries: #iterates through each entry from file
            entered = False
            
            for catType in self.type: #iterates through each type

                if catType in entry.category: #checks if type is equal to the entries category type
                    self.category[catType].append(entry) #adds the entry to the respective category type
                    entered = True
                    if entry.category != "Payment/Credit": #Determines individual days
                        self.daybill.append(entry.amount)
                        self.bill_dates.append(entry.date)

                    if entry.category == "Payment/Credit":
                        self.daypaid.append(entry.amount)
                        self.paid_dates.append(entry.date)
                    break #breaks so the entry is not duplicated and added to "others" category
            if entered == False:
                self.category["Others"].append(entry) #if entry is not added to a category, add to others.
        

                # self.daybill.append(entry.amount)
                # self.bill_dates.append(entry.date)
    def print_entries(self): #Print all data entries in order of intake
        for entry in self.entries:
            print(entry.date, entry.transaction, entry.category, entry.amount)

    def print_sorted(self): #Print all data entries sorted by category
        for category, entries in self.category.items():
            print(category)
            for entry in entries:
                print(entry.date, entry.transaction, entry.category, entry.amount)
            print()

    def extract_Cat(self): #Finds the sum of money in the statement given for each category (ALL months)
        moneys = 0
        cat_sums = []
        for category, entries in self.category.items():
            #print(category)
            for entry in entries:
                moneys = moneys + entry.amount
            cat_sums.append("{:.2f}".format(moneys))
            moneys = 0
        return cat_sums

    def extract_Month(self): #Extracts total moneys paid and unpaid for the year
        for i in range(1, 13):
            bill = 0
            paid = 0
            for category, entries in self.category.items():
                for entry in entries:
                    date_object = datetime.strptime(entry.date, "%m/%d/%y")
                    month = date_object.month #Extracts specific dates
                    if month == i and entry.category != "Payment/Credit":
                        bill += entry.amount #Finds the sum of all bill
                    if month == i and entry.category == "Payment/Credit":
                        paid += entry.amount #Finds the sum of all paid
            self.monthlybill.append(bill)
            self.monthlypaid.append(paid)

    def search_range_cat(self): #priority attribute of printing transactions for a specific category in a specified date range
        '''cat = "Entertainment"
        startDate = "07/1/22"
        endDate = "8/13/22"'''
        startDate = input("Specify a beginning date (MM/DD/YY): ")
        endDate = input("Specify an end date (MM/DD/YY): ")
        print(self.type)
        cat = input("Specify a category: ")

        if cat in self.category:
            transactions_in_category = self.category[cat] #the transactions in the requested category
            start_date = datetime.strptime(startDate, "%m/%d/%y")
            end_date = datetime.strptime(endDate, "%m/%d/%y")

            #adds only those transactions that fall between the requested date range
            for transaction in transactions_in_category:
                transaction_date = datetime.strptime(transaction.date, "%m/%d/%y")
                if start_date <= transaction_date <= end_date:
                    self.priority_queue.put(transaction) 

    def search_month(self): #priority attribute for printing transactions for a specified month
        #month = "12/2022"
        month = input("Enter the month and year in the format (MM/YYYY): ")
        month,year = month.split("/")
        start_date = datetime(int(year), int(month), 1)
        end_date = datetime(int(year), int(month), calendar.monthrange(int(year), int(month))[1]) #use calender to find the last day of month

        #loop to add to priority queue if transaction falls within the month specified
        for entry in self.entries:
            entryDate = datetime.strptime(entry.date, "%m/%d/%y")
            
            if start_date <= entryDate <= end_date:
                self.priority_queue.put(entry)

        #self.extract_Cat_priority()
    def printPriorityPie(self): #print all transactions that fall within the priority, method used if printing pie graph
        category_sums = {}
        if not self.priority_queue.empty():
            print("\nTransactions for specified priority")
            while not self.priority_queue.empty():
                    transaction = self.priority_queue.get()
                    print(transaction.date, transaction.transaction, transaction.category, transaction.amount) #prints everything in queue
                    if transaction.category in category_sums:
                        category_sums[transaction.category] += transaction.amount
                    else:
                        category_sums[transaction.category] = transaction.amount
                    #totalAmount = totalAmount + transaction.amount
            #print("Total amount paid: ", '%.2f'%totalAmount)
        else:
            print("No transactions found within the specified date range")  
        list_sums = [category_sums.get(category, 0) for category in self.type]
        
        return list_sums
    def printPriorityLine(self): #print all transactions that fall within the priority, method used for line graph
        list_amt =[]
        list_dates = []
        if not self.priority_queue.empty():
            print("\nTransactions for specified priority")
            while not self.priority_queue.empty():
                    transaction = self.priority_queue.get()
                    print(transaction.date, transaction.transaction, transaction.category, transaction.amount)
                    list_amt.append(transaction.amount)
                    list_dates.append(transaction.date)
        return list_amt, list_dates
    
    def printpie(self,values): #general pie printing method
        self.extract_Cat()
        labels = self.type
        #values = self.cat_sums #Expects the total
        fig = px.pie(values=values, names=labels)
        fig.show() 

    def printBAR(self): #Work on getting total amount of bill and billpayment
        months = list(calendar.month_name)[1:]
        self.extract_Month()
        values = self.monthlybill  # Example values for each month
        values1 = self.monthlypaid
        #print(values,"Length:",len(values))
        #print(values1,"Length:",len(values1))

        trace1 = go.Bar(x=months, y=values, name='Bill')
        trace2 = go.Bar(x=months, y=values1, name='Paid')

        data = [trace1, trace2] #list of traces so both graphs can be represented at the same time
        
        layout = go.Layout(title='Bill and Paid')
        fig1 = go.Figure(data=data, layout=layout)
        #fig1.update_layout(barmode='stack', xaxis={'categoryorder':'total ascending'})
        fig1.show()
        #prints regular line graph for all bills
    def printLine(self): #monthly
        # line graph
        #self.extract_billdays()  # Call the method to populate bill dates and amounts

        months = list(calendar.month_name)[1:]

        fig2 = go.Figure()

        fig2.add_trace(go.Scatter(x=self.bill_dates, y=self.daybill, mode='lines', name='Balance'))

        fig2.update_layout(title='Balance Evolution over Time',
                        xaxis_title='Date',
                        yaxis_title='Balance')

        fig2.show()
#prints the line for prioritized data
    def printLinePrio(self,x,y): #monthly
        # line graph
        #self.extract_billdays()  # Call the method to populate bill dates and amounts

        fig2 = go.Figure()

        fig2.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Balance'))

        fig2.update_layout(title='Spending on category',
                        xaxis_title='Date',
                        yaxis_title='Balance')

        fig2.show()
#return N priorities in the queue
    def returnN(self):
        n = int(input("Enter desired amount of top entries: "))
        if not self.priority_queue.empty():
            print("Top", n, "entries within priority")
            topTransactions = []
            while not self.priority_queue.empty() and n>0:
                transaction = self.priority_queue.get()
                print(transaction.date, transaction.transaction, transaction.category, transaction.amount)
                topTransactions.append(transaction)
                n=n-1
            
            #loop to add back the retrieved transactions to the loop
            for transaction in topTransactions:
                self.priority_queue.put(transaction)
        #return top_transactions

    def printPriority(self):
        if not self.priority_queue.empty():
            print("\nTransactions for specified priority")
            while not self.priority_queue.empty():
                    transaction = self.priority_queue.get()
                    print(transaction.date, transaction.transaction, transaction.category, transaction.amount)
        else:
            print("Nothing in priority Queue")


#Method to parse file and create multiple Transactions objects 
def readTransactions(csv_file):
    data = []
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        
        next(csv_reader) #skips first row of file

        for row in csv_reader:
            date = row[0] #extract date value
            transaction = row[3] #extract transaction description
            category = row[4] #extract category type
            if row[5] != '':
                amount = float(row[5]) #extract amount
            if category == "Payment/Credit":
                amount = float(row[6])
            
            #print(row)

            obj = Transactions(date,transaction,category,amount) #creates an object for each entry 
            data.append(obj) #appends the entry to a list
            #print(obj.date,obj.transaction,obj.category,obj.amount)
    data = sorted(data, key=lambda entry: datetime.strptime(entry.date, "%m/%d/%y"))
    return TransactionsManager(data)


transactions = readTransactions("/your/path/M.csv")


while True:
            print("Welcome to the statement analyzer")
            print("Options:")
            print("1. Print all transactions sorted by category")
            print("2. Print transactions by category in a date range and Line chart")
            print("3. Print transactions for a specific month and pie chart")
            print("4. Print pie chart of transaction categories for all months")
            print("5. Print bar chart of monthly bills and payments for all months")
            print("6. Print line graph of balance evolution over time")
            print("7. Sorted csv uncategorized")
            print("8. Add date range and cat priority w/o graph, return N and print all priorities matched") #adding priorities only to queue doesnt work
            print("9. Add priority month only w/o graph, return N and print all priorities matched") #adding priorities only to queue doesnt work
            #print("10. Add date range and cat priority w/o graph") #adding priorities only to queue doesnt work
            #print("11. Add priority month only w/o graph") #adding priorities only to queue doesnt work
            print("0. Exit")
            choice = input("Enter your choice (0-9): ")

            if choice == "0":
                print("Exiting the statement analyzer. Goodbye!")
                break
            elif choice == "1":
                transactions.print_sorted()
            elif choice == "2":
                transactions.search_range_cat()
                prio_list = transactions.printPriorityLine()
                x = prio_list[1]
                y = prio_list[0]
                transactions.printLinePrio(x,y)
            elif choice == "3":
                transactions.search_month()
                #transactions.printPriority()
                prio_list = transactions.printPriorityPie()
                transactions.printpie(prio_list)
                #transactions.printPriority()

            elif choice == "4":
                values = transactions.extract_Cat()
                transactions.printpie(values) #prints pie of all data intake
            elif choice == "5":
                transactions.printBAR() #prints bar with paid and upaid for all data intake
            elif choice == "6":
                transactions.printLine() #prints a line chart with all data intake
            elif choice == "7":
                transactions.print_entries() #prints all data uncategorized
            #elif choice == "8":
                #transactions.printPriority()
            elif choice == "8":
                transactions.search_range_cat()
                transactions.returnN()
                transactions.printPriority()
            elif choice == "9":
                transactions.search_month()
                transactions.returnN()
                transactions.printPriority()
            else:
                print("Invalid choice. Please try again.")
            print("--------------------------------------------------------------------------------------------")
