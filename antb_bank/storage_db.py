import sqlite3

class AccountsStorage(object):

    def __init__(self):
        self.db = './antb_bank/db/data.db'

    def log(self, msg):
        print("ERR : "+msg)

    def query(self, query, *args):
        con = None
        data = None
        
        try:
            con = sqlite3.connect(self.db)
            cur = con.cursor()
            cur.execute(query, tuple(args))
            data = cur.fetchall()
            if not data:
                con.commit()
        except sqlite3.Error as e:
            self.log("Database error: %s" % e)
        except Exception as e:
            self.log("Exception in _query: %s" % e)
        finally:
            if con:
                con.close()
        return (cur.lastrowid, data) 

    def getAccounts(self) :
        req = 'SELECT id, name FROM accounts WHERE deleted=0'
        data = self.query(req)
        if not data or not data[1]:
            return None
        return [{'id': row[0], 'name' : row[1]} for row in data[1]]

    def getAccount(self, account_id):
        req = 'SELECT id, name FROM accounts WHERE deleted=0 and id=?'
        data = self.query(req, account_id)

        if not data or not data[1]:
            return None
        
        periods = self.getPeriodsForAccount(data[1][0][0])
        if periods == None:
            return None
        return {'id': data[1][0][0], 'name' : data[1][0][1], 'periods': periods }
    

    def getPeriodsForAccount(self, account_id):
        res = []
        req = 'SELECT id, name FROM periods WHERE deleted=0 AND account_id=?'
        data = self.query(req, account_id)
        if not data :
            return None

        for row in data[1]:
            operations = self.getOperationsForPeriod(row[0])
            if operations == None :
                return None
            res.append({'id': row[0], 'name':row[1], 'operations':operations})
        return res

    def getOperationsForPeriod(self, period_id):
        res = []
        req = 'SELECT id, checked, date, amount FROM operations WHERE deleted=0 AND period_id=?'
        data = self.query(req, period_id)

        if not data:
            return None

        for row in data[1]:
            tags = self.getTagsForOperation(row[0])
            if tags == None:
                return None
            res.append({'id': row[0], 'checked':bool(row[1]), 'date': row[2], 'amount':float(row[3]), 'tags':tags})
        return res

    def getTagsForOperation(self, operation_id):
        res = []
        req = 'SELECT id, name, color FROM operation_tags JOIN tags ON operation_tags.tag_id=tags.id WHERE operation_tags.operation_id = ?'

        data = self.query(req, operation_id)

        if not data:
            return None

        for row in data[1]:
            res.append({'id':row[0], 'name': row[1], 'color': row[2]})
        return res

    def addAccount(self, name):
        req = "INSERT INTO accounts (name) VALUES (?)"
        data = self.query(req, name)
        
        if not data:
            return None

        return {'id': data[0], 'name' : name}

    def addOperation(self, account_id, period_id, date, amount, tags, checked):
        req = "INSERT INTO operations (date, amount, checked, period_id) VALUES (?,?,?,?)"
        data = self.query(req, date, amount, 1 if checked else 0, period_id)
        if not data:
            return None

        req = "INSERT INTO period_operations (operation_id, period_id) VALUES (?,?)"
        data2 = self.query(req, data[0], period_id)
        if not data2:
            return None
        self.addOperationTags(data[0], tags)
        return {'id':data[0], 'date':date, 'amount':amount, 'checked': checked, 'tags': tags}


    def addOperationTags(self, operation_id, tags):
        for tag in tags:
            req = "SELECT id FROM tags WHERE name=?"
            data = self.query(req, tag['name'])
            if not data:
                return None
            if (len(data[1]) > 0):
                req = "INSERT OR IGNORE INTO operation_tags (operation_id, tag_id) VALUES (?,?)"
                data = self.query(req, operation_id, data[1][0][0])
                if not data:
                    return None
            else :
                self.addOperationTag(operation_id, tag)
        return True


    def addOperationTag(self, operation_id, tag):
        req = "INSERT INTO tags (name, color) VALUES (?,?)"
        data = self.query(req, tag['name'], tag['color'])
        if not data:
            return None
        
        req = "INSERT INTO operation_tags (operation_id, tag_id) VALUES (?,?)"
        self.query(req, operation_id, data[0])
        

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
                    