import sqlite3

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
            res.append({'id':row[0], 'name': row[1], 'color': row[2]})
        connection.close()
        return res

    def addAccount(self, name):
        account = {'id': len(data)+1, 'name' : name}
        data.append(account)
        return account

    def addOperation(self, account_id, period_id, date, amount, tags, checked):
        print("test")
        connection = sqlite3.connect(self.db)
        c = connection.cursor()
        check = 1 if checked else 0
        req = "INSERT INTO operations (date, amount, checked, period_id) VALUES ('"+str(date)+"',"+str(amount)+","+str(check)+","+str(period_id)+")"
        r = c.execute(req)
        id = r.lastrowid
        print(">>"+str(id))
        req = "INSERT INTO period_operations (operation_id, period_id) VALUES ("+str(id)+","+str(period_id)+")"
        c.execute(req)
        connection.commit()
        connection.close()
        self.addOperationTags(r.lastrowid, tags)


        return {'id':id, 'date':date, 'amount':amount, 'checked': checked, 'tags': tags}


    def addOperationTags(self, operation_id, tags):
        for tag in tags:
            connection = sqlite3.connect(self.db)
            c = connection.cursor()
            req = "SELECT id FROM tags WHERE name='"+tag["name"]+"'"
            c.execute(req)
            rows = c.fetchall()
            if (len(rows) > 0):
                req = "INSERT OR IGNORE INTO operation_tags (operation_id, tag_id) VALUES ("+str(operation_id)+','+str(rows[0][0])+')'
                c.execute(req)
                connection.commit()
                connection.close()
            else :
                connection.close()
                self.addOperationTag(operation_id, tag)


    def addOperationTag(self, operation_id, tag):
        connection = sqlite3.connect(self.db)
        c = connection.cursor()
        req = "INSERT INTO tags (name, color) VALUES ('"+str(tag['name'])+"','"+str(tag['color'])+"')"
        tag_id = c.execute(req).lastrowid
        req = "INSERT INTO operation_tags (operation_id, tag_id) VALUES ("+str(operation_id)+','+str(tag_id)+')'
        c.execute(req)
        connection.commit()
        connection.close()

    def updateOperation(self, account_id, period_id, operation_id, date, amount, tags, checked):
        check = 1 if checked else 0

        connection = sqlite3.connect(self.db)
        c = connection.cursor()
        req = "UPDATE operations SET date='"+str(date)+"', amount="+str(amount)+", checked='"+str(check)+"' WHERE id="+str(operation_id)
        id = c.execute(req).lastrowid
        connection.commit()
        connection.close()
        if id != -1:
            self.addOperationTags(operation_id, tags)
            return {'id':operation_id, 'date':date, 'amount':amount, 'checked': checked, 'tags': tags}  
        return {}

    def deleteOperation(self, account_id, period_id, operation_id) :
        connection = sqlite3.connect(self.db)
        c = connection.cursor()
        req = "DELETE FROM operations WHERE id="+str(operation_id)
        c.execute(req)
        req = "DELETE FROM operation_tags WHERE operation_id="+str(operation_id)
        c.execute(req)
        req = "DELETE FROM period_operations WHERE operation_id="+str(operation_id)+" AND period_id="+str(period_id)
        c.execute(req)
        connection.commit()
        connection.close()
                    