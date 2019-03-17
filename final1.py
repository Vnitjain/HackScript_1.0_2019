# from tika import parser

# raw = parser.from_file('test2.pdf')
# print(raw['content'])
import textract
from dateutil import parser
import re
import json
# text = textract.process("test2.pdf").decode("utf-8")
text = textract.process("test3.png").decode("utf-8")
text = text.split("\n\n")
text = [i.split("\n") for i in text]
text1 = []

for i in text:
	temp = []
	for j in i:
		temp.append(j.lower().replace(" ",""))
	text1.append(temp)
# print(text)
text2 = []
for i in text1:
	text2 += i
# print(text2)
def find_index(text2,term):
	for i in range(len(text2)):
		for j in term:
			if(j in text2[i]):
				if(i==len(text2)):
					return 'N/A'
				else:
					return text2[i+1]
def doc_type(text):
	for i in text:
		for j in i:
			if(("purchase" in j) and ("order" in j)):
				return "PO"
			elif("invoice" in j):
				return "invoice"

def find_currency(text1):
	currency = []
	for i in text1:
		for j in i:
			currency.append(re.findall("[amount|total]+[()]+([a-z]+)[()]+",j))
	if(not(max([len(i) for i in currency]))):
		currency.append(['sgd'])
	dict1 = {'usd':"$","rupee":"Rs.","sgd":"$"}
	return sorted(currency)[-1][0],dict1[str(sorted(currency)[-1][0])]
#without string replace
# def find_total(text1,op):
# 	list_of_amounts = []
# 	for i in text1:
# 		for j in i:
# 			list_of_amounts.append(re.findall("["+op+"]+([0-9]+.[0-9]+)",j))
# 			if(not(list_of_amounts)):
# 				list_of_amounts.append(re.findall("["+op+"]([0-9]+.[0-9]+)",j))
# 	return max(list_of_amounts)

def find_total(text1,op):
	list_of_amounts = []
	for i in text1:
		for j in i:
			list_of_amounts.append(re.findall("[0-9]+[,]*[0-9]+[.][0-9]",j))
			if(not(list_of_amounts)):
				list_of_amounts.append(re.findall("[0-9]+[,]*[0-9]+[.][0-9]",j))
	# print(sorted(list_of_amounts))
	temp = []
	for i in list_of_amounts:
		for j in i:
			if(len(j)!=0):
				temp.append(float(j.replace(",","")))
	# print(max(temp))
	return max(temp)

def find_date(text):
	for i in text:
		for j in i:
			try:
				if(len(j)>=6):
					x = parser.parse(j)
					# print(x)
					# return x.day+"/"x.month+"/"x.year
			except:
				continue
def ponumber(text):
	pon = []
	inv = []
	for i in text:
		for j in i:
			pon.append(re.findall("[po]+[0-9]*[/][0-9a-z]*[/]*[0-9a-z]*",j))
			inv.append(re.findall("[inv]+[0-9]*[/][0-9a-z]*[/]*[0-9a-z]*",j))
	try:
		final_po = sorted(pon)[-1][0]
	except:
		final_po = None
	try:
		final_inv = sorted(inv)[-1][0]
	except:
		final_inv = None
	return final_po,final_inv

output_json = {

	"doctype":doc_type(text1),

	"orderingcompany":find_index(text2,['billto']),

	"suppliercompany":find_index(text2,['billto']),

	"shipto": find_index(text2,['shipto']),

	"ponum": ponumber(text1),

	"podate": find_date(text1),

	"totalamount": find_total(text,find_currency(text1)[1]),

	"currency":find_currency(text1)[0]
}
print(output_json)
with open('hs/df/invo1.json', 'w') as outfile:
    json.dump(output_json, outfile)
