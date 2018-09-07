import sqlite3

data = [
    {
        'id': 1, 
        'name': "CCHQ1",
        'tagColors' : {
            'INITIAL_VALUE': "badge-info",
            'SAVING': "badge-success",
            'CAR': "badge-warning",
            'HOBBIES': "badge-warning"
        },
        'periods' : [
            {
                'id': 1,
                'name': "period1",
                'operations' : [
                    { 'id': 1, 'date': "2018-06-26", 'amount': -123.26, 'tags' : ["INITIAL_VALUE"], 'checked': True}, 
                    { 'id': 2, 'date': "2018-06-27", 'amount':   26.08, 'tags' : ["REFUND", "HEALTH"], 'checked': False}, 
                    { 'id': 3, 'date': "2018-06-27", 'amount': 1149.42, 'tags' : ["SALARY"], 'checked': True}, 
                    { 'id': 4, 'date': "2018-06-28", 'amount':  -85.82, 'tags' : ["HOBBIES", "WITHDRAW"], 'checked': True}, 
                    { 'id': 5, 'date': "2018-06-29", 'amount':   -0.99, 'tags' : ["FREE"], 'checked': False}, 
                    { 'id': 6, 'date': "2018-06-30", 'amount':  -50.00, 'tags' : ["SAVING", "PEL"], 'checked': False}, 
                ]
            },
            {
                'id': 2,
                'name': "period2",
                'operations' : [
                    { 'id':  7, 'date': "2018-06-31", 'amount':  -540, 'tags' : ["RENT"], 'checked': True}, 
                    { 'id':  8, 'date': "2018-07-01", 'amount': 84.85, 'tags' : ["HELP", "PRIME_EMPLOI"], 'checked': False}, 
                    { 'id':  9, 'date': "2018-07-01", 'amount':  -7.6, 'tags' : ["HOBBIES", "CINEMA"], 'checked': True}, 
                    { 'id': 10, 'date': "2018-07-02", 'amount':  -5.6, 'tags' : ["FOOD", "SANDWICH"], 'checked': True}, 
                    { 'id': 11, 'date': "2018-07-08", 'amount':  -250, 'tags' : ["SAVING", "LIVA"], 'checked': False}, 
                    { 'id': 12, 'date': "2018-07-08", 'amount':  -50.00, 'tags' : ["SAVING", "PEL"], 'checked': False}, 
                ]
            }
        ]
    },
    {
        'id': 2, 
        'name': "CCHQ2",
        'tagColors' : {
            'INITIAL_VALUE': "badge-info",
            'SAVING': "badge-success",
            'CAR': "badge-warning",
            'HOBBIES': "badge-warning"
        },
        'periods' : [
            {
                'id': 3,
                'name': "period3",
                'operations' : [
                    { 'id': 13, 'date': "2018-06-26", 'amount': -123.26, 'tags' : ["INITIAL_VALUE"], 'checked': True}, 
                    { 'id': 14, 'date': "2018-06-27", 'amount':   26.08, 'tags' : ["REFUND", "HEALTH"], 'checked': False}, 
                    { 'id': 15, 'date': "2018-06-27", 'amount': 1149.42, 'tags' : ["SALARY"], 'checked': True}, 
                    { 'id': 16, 'date': "2018-06-28", 'amount':  -85.82, 'tags' : ["HOBBIES", "WITHDRAW"], 'checked': True}, 
                    { 'id': 17, 'date': "2018-06-29", 'amount':   -0.99, 'tags' : ["FREE"], 'checked': False}, 
                    { 'id': 18, 'date': "2018-06-30", 'amount':  -50.00, 'tags' : ["SAVING", "PEL"], 'checked': False}, 
                ]
            },
            {
                'id': 4,
                'name': "period4",
                'operations' : [
                    { 'id': 19, 'date': "2018-06-31", 'amount':    -540, 'tags' : ["RENT"], 'checked': True}, 
                    { 'id': 20, 'date': "2018-07-01", 'amount':   84.85, 'tags' : ["HELP", "PRIME_EMPLOI"], 'checked': False}, 
                    { 'id': 21, 'date': "2018-07-01", 'amount':    -7.6, 'tags' : ["HOBBIES", "CINEMA"], 'checked': True}, 
                    { 'id': 22, 'date': "2018-07-02", 'amount':    -5.6, 'tags' : ["FOOD", "SANDWICH"], 'checked': True}, 
                    { 'id': 23, 'date': "2018-07-08", 'amount':    -250, 'tags' : ["SAVING", "LIVA"], 'checked': False}, 
                    { 'id': 24, 'date': "2018-07-08", 'amount':  -50.00, 'tags' : ["SAVING", "PEL"], 'checked': False}, 
                ]
            }
        ]
    }
]




class AccountsStorage(object):

    def __init__(self):
        self.db = './antb_bank/db/data.db'


    def getAccounts(self) :
        connection = sqlite3.connect(self.db)
        c = connection.cursor()
        req = 'SELECT id, name from accounts WHERE deleted=0'
        res= [{'id': row[0], 'name' : row[1]} for row in c.execute(req)]
        connection.close()
        return res

    def getAccount(self, id):
        connection = sqlite3.connect(self.db)
        c = connection.cursor()
        req = 'SELECT id, name from accounts WHERE deleted=0 and id='+str(id)
        row = c.execute(req).fetchone()
        if row == None:
            return{}
        
        res = {'id': row[0], 'name' : row[1], 'periods':self.getPeriodsForAccount(row[0]),'tagColors' : {
            'INITIAL_VALUE': "badge-info",
            'SAVING': "badge-success",
            'CAR': "badge-warning",
            'HOBBIES': "badge-warning"
        }}

        connection.close()
        return res

    def getPeriodsForAccount(self, account_id):
        res = []
        connection = sqlite3.connect(self.db)
        c = connection.cursor()

        req = 'SELECT id, name FROM periods WHERE deleted=0 AND account_id='+str(account_id)
        rows = c.execute(req)
        for row in rows:
            res.append({'id': row[0], 'name':row[1], 'operations':self.getOperationsForPeriod(row[0])})

        connection.close()
        return res

    def getOperationsForPeriod(self, period_id):
        res = []
        connection = sqlite3.connect(self.db)
        c = connection.cursor()

        req = 'SELECT id, checked, date, amount FROM operations WHERE deleted=0 AND period_id='+str(period_id)
        rows = c.execute(req)
        for row in rows:
            res.append({'id': row[0], 'checked':bool(row[1]), 'date': row[2], 'amount':float(row[3]), 'tags': self.getTagsForOperation(row[0])})

        connection.close()
        return res

    def getTagsForOperation(self, operation_id):
        res = []
        connection = sqlite3.connect(self.db)
        c = connection.cursor()

        req = 'SELECT id, name, color FROM operation_tags JOIN tags ON operation_tags.tag_id=tags.id WHERE operation_tags.operation_id = '+str(operation_id)
        for row in c.execute(req):
            res.append(row[1])
        connection.close()
        return res

    def addAccount(self, name):
        account = {'id': len(data)+1, 'name' : name}
        data.append(account)
        return account

    def addOperation(self, account_id, period_id, date, amount, tags, checked):
        connection = sqlite3.connect(self.db)
        c = connection.cursor()
        check = 1 if checked else 0
        req = "INSERT INTO operations (date, amount, checked, period_id) VALUES ('"+str(date)+"',"+str(amount)+","+str(check)+","+str(period_id)+")"
        r = c.execute(req)
        print(r.lastrowid)
        return {'id':r.lastrowid, 'date':date, 'amount':amount, 'checked': checked, 'tags': tags}

    def updateOperation(self, account_id, period_id, operation_id, date, amount, tags, checked):
        account = self.getAccount(account_id)
        for period in account['periods'] :
            if period['id'] == period_id :
                for i in range(0,len(period['operations'])) :
                    operation = period['operations'][i]
                    if operation['id'] == operation_id :
                        period['operations'][i] = { 'id': operation_id, 'date': date, 'amount':  amount, 'tags' : tags, 'checked': checked}
                        return operation
        return {}

    def deleteOperation(self, account_id, period_id, operation_id) :
        def findOperation(operations, id):
            for i in range(0,len(operations)) :
                if operations[i]['id'] == id :
                    return operations[i]
            return -1

        account = self.getAccount(account_id)
        for period in account['periods'] :
            if period['id'] == period_id :
                operation = findOperation(period['operations'], operation_id)
                if operation == -1:
                    return False
                else:
                    period['operations'].remove(operation)
                    return True
                    