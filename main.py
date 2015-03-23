# -*-coding: utf-8 -*-
import os
import sqlite3 as S3



class ReversePolishNotation:

	LEFT_ASSOC = 0
	RIGHT_ASSOC = 1
	OPERATORS = {
		"+" : (0, LEFT_ASSOC),
		"-" : (0, LEFT_ASSOC),
		"*" : (1, LEFT_ASSOC),
		"/" : (1, LEFT_ASSOC)
		}

	STACK = []
	TOTAL_STRING = []

	def isOperator(self, symbol):
		'''Function check does the element operator or not.

		:return: Does @symbol consists(True) in @OPERATORS or not(False)
		'''

		return symbol in self.OPERATORS.keys()


	def cmpRate(self, symbolFromString, topSymbolOfStack):
		'''Function compares the Rate between two operators.
		The higher the rating the earlier of the execution.

		:return: the numerical value of the difference of ratings operators 
		'''

		return (self.OPERATORS[symbolFromString][0]) - (
			self.OPERATORS[topSymbolOfStack][0])


	def isAssociative(self, symbolFromString, ASSOC):
		'''Function returnes associative of the operator.
		'''

		return self.OPERATORS[symbolFromString][1] == ASSOC


	def convertationAsVSSTD(self, string):
		'''This function convert the original entered function to convenient
		type for further work.

		:return: completed stack with Variables and Operators.
		'''
		
		for i in string:
			if self.isOperator(i) == True or i == "(" or i == ")":
				string = string.replace(i, " "+i+" ")
		string = string.split(" ")
		for i in string:
			if self.isOperator(i):  
				while len(self.STACK) != 0 and self.isOperator(self.STACK[-1]):
					if (self.cmpRate(i, self.STACK[-1]) <= 0) or (
						self.cmpRate(i, self.STACK[-1]) < 0):
						self.TOTAL_STRING.append(self.STACK.pop())
						continue
					break
				self.STACK.append(i)
			elif i == '(':
				self.STACK.append(i)
			elif i == ')':
				while len(self.STACK) != 0 and self.STACK[-1] != '(':
					self.TOTAL_STRING.append(self.STACK.pop())
				self.STACK.pop()
			elif i == "":
				continue
			else:
				self.TOTAL_STRING.append(i)
		while len(self.STACK) != 0:
			self.TOTAL_STRING.append(self.STACK.pop())
		return self.TOTAL_STRING


class FunctionEvaluation(ReversePolishNotation):

	STACK = []
	RESULT = 0
	LENGTH = len(STACK)
	MATH_ELEMENTS = ["+", "-", "*", "/", "(", ")"]


	def isOperand(self, element):
		'''Function check does the element math element or not.

		:return: Does @element consists(True) in @MATH_ELEMENTS or not(False)
		'''
		return element in self.MATH_ELEMENTS


	def equal(self, givven_string):
		'''Function replace the variable by its value from the database. 

		:return: the result of the function
		'''

		self.newString = ReversePolishNotation().convertationAsVSSTD(givven_string)
		database().createDatabase()
		for i in range(len(self.newString)):
			if self.newString[i] == "":
				'''If element is empty - continue
				'''
				continue
			else:
				'''Else...
				'''
				if not self.isOperand(self.newString[i]) and (
					database().checkVarDB(self.newString[i]) != 0):

					'''If element exists in the database, then just replace 
					by its value from the database.
					'''
					self.newString[i] = database().getValueOfVarDB(self.newString[i])
				elif not self.isOperand(self.newString[i]) and (
					database().checkVarDB(self.newString[i]) == 0):

					'''If element not exists in the database, then 
					enter the value of it and put to the database and at the 
					same time replace at the string.
					'''
					self.checkTrue = False
					while self.checkTrue == False:
						try:
							float(self.getValueFromConsole(self.newString[i]))
							self.checkTrue = True
						except ValueError:
							self.checkTrue = False
							print("Value Error, please try again.")
							
					'''Add to string from the Database 
					'''
					database().addVarAndValueToDB(self.newString[i],
						self.Value)
					self.newString[i] = self.Value
		self.string_total = self.newString
		self.checkString = ""
		for i in self.string_total:
			self.checkString += i
			self.checkString += " "
		print("Check the convertation of your function: " + "\""+
			self.checkString+"\"")
		for stringSymbol in self.string_total:
			if stringSymbol in ['-', '+', '*', '/']:
				op1 = self.STACK.pop()
				op2 = self.STACK.pop()
				if stringSymbol =='-': self.RESULT = op2 - op1
				if stringSymbol =='+': self.RESULT = op2 + op1
				if stringSymbol =='*': self.RESULT = op2 * op1
				if stringSymbol =='/': self.RESULT = op2 / op1
				self.STACK.append(self.RESULT)
			else:
				self.STACK.append(float(stringSymbol))
		return self.RESULT


	def getValueFromConsole(self, var):
		'''Get Value of a specific Variable from the console.

		:return: Value of the Variable which is passed to this function

		:raise: ValueError
		'''
		self.Value = input("%s not consists in DB, please enter its Value: " % var)
		return self.Value


class VSSTD:

	dictionaryVSSTD = {}
	intermediateDictionary = {}

	def parse(self, vsstd):
		'''Parsing of the string with Variables and its Values.

		:return: dictionary with keys - Variables and values - Values
		'''
		self.VSSTD = vsstd
		self.VSSTD = self.VSSTD.replace("=", ";").split(";")
		self.VSSTD.pop()
		for i in range(len(self.VSSTD)):
			self.VSSTD[i] = self.VSSTD[i].strip()
		for j in range(0, len(self.VSSTD), 2):
			self.dictionaryVSSTD.update(self.intermediateDictionary.fromkeys([self.VSSTD[j]], self.VSSTD[j+1]))
		return self.dictionaryVSSTD


class database:

	PATH = os.getcwd()

	def createDirForDB(self):
		'''Function creates a folder for database

		:return: nothing

		:raise: FileExistsError
		'''
		os.mkdir(self.PATH+"\\DB")


	def connectToDB(self):
		'''Function realize connection to database

		:return: nothing

		:raise: FileExistsError
		'''

		self.con = S3.connect(self.PATH+"\\DB\\"+"VSSTD.db")
		self.cur = self.con.cursor()


	def inputFirstVars(self):
		'''If database Not created user have to enter at least one Variable
		with its Value

		:return: nothing

		:raise: ValueError
		'''

		self.connectToDB()
		self.newVSSTD = input("Please, enter at least ONE Variable" +
			" like: '$A.EM=25.4;': ")
		self.newDictForDB = VSSTD().parse(self.newVSSTD)
		self.connectToDB()
		for currKey in self.newDictForDB:
			self.cur.execute("INSERT INTO vsstd VALUES('%s', '%s')" %
				(currKey, self.newDictForDB.get(currKey)))
		self.con.commit()


	def createDatabase(self):
		'''Creating database for work
		'''

		if os.path.exists(self.PATH+"\\DB") == True:
			self.connectToDB()
			self.con.commit()
		else:
			self.createDirForDB()
			self.connectToDB()
			self.cur.execute("CREATE TABLE vsstd (Var TEXT, Value TEXT)")
			self.inputFirstVars()
			self.con.commit()
	

	def addVarAndValueToDB(self, var, value):
		'''Function changes data of DB as adding it and its value to Database
		which get from the console.
		'''

		self.connectToDB()
		self.cur.execute("INSERT INTO vsstd VALUES('%s', '%s')" % (str(var), str(value)))
		self.con.commit()
		print(var,"=",value, " added to database")


	def checkVarDB(self, var):
		'''Function returned the string representation of the Var

		:return: the number of occurrences of the Variable 

		:raise: ValueError, FileExistsError
		'''

		self.connectToDB()
		self.count = self.cur.execute("SELECT COUNT (*) AS 'count' FROM vsstd WHERE Var = '%s'" % var).fetchall()[0][0]
		self.con.commit()

		return self.count


	def getValueOfVarDB(self, var):
		'''Function returned Value's string representation of the Var

		:return: Value of the Variable which passed to the function

		:raise: FileExistsError
		'''

		self.connectToDB()

		return self.cur.execute("SELECT * FROM vsstd WHERE Var = '%s'" % var).fetchall()[0][1]


if __name__ == "__main__":
	string = input("Enter the function: ")
	print("Result: ", FunctionEvaluation().equal(string))
	os.system("Pause")
