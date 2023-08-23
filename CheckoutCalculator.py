import ocr
import re

text = ocr.ExtractText('img3.jpg')

def CalculateCheckoutSheet(itemValueDict):
    cashReceived = float(input('Enter Cash Received: '))

    creditCardSales = itemValueDict[total] - itemValueDict[cashOwed]
    cashTips = cashReceived - itemValueDict[cashOwed]

    cashTipPercent = cashTips / itemValueDict[cashOwed]
    creditTipPercent = itemValueDict[tips] / creditCardSales
    grossTips = cashTips + itemValueDict[tips]
    grossTipPercent = grossTips / itemValueDict[total]

    bartender = grossTips * 0.05
    runner = grossTips * 0.13
    netTips = grossTips - bartender - runner
    

# find select lines in text

# total sales (cash + credit)
totalStart = text.find('TOTAL')
totalEnd = text.find('(=)', totalStart)
total = text[totalStart:totalEnd]
# extra preprocessing needed for total to get rid of , if value is over 1000
total = total.replace(',', '')

# credit card tips
tipsStart = text.find('Charge Tips')
tipsEnd = text.find('\n', tipsStart)
tips = text[tipsStart:tipsEnd]

# cash owed
cashStart = text.find('CASH OWED')
cashEnd = text.find('(=)', tipsStart)
cashOwed = text[cashStart:cashEnd]

strings = [total, tips, cashOwed]
itemValueDict = {}

# extract numbers from three strings above
for s in strings:
    v = (re.findall("\d+\.\d+", s))
    v = ''.join(v) # convert list to string
    v = float(v) #convert string to float
    itemValueDict[s] = v
    print(type(v))

# start calculating
CalculateCheckoutSheet(itemValueDict)
