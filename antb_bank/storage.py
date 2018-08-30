
data = [
    {
        'id': 1, 
        'name': "CCHQ1",
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
        'periods' : [
            {
                'id': 3,
                'name': "period1",
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
                'name': "period2",
                'operations' : [
                    { 'id': 19, 'date': "2018-06-31", 'amount':  -540, 'tags' : ["RENT"], 'checked': True}, 
                    { 'id': 20, 'date': "2018-07-01", 'amount': 84.85, 'tags' : ["HELP", "PRIME_EMPLOI"], 'checked': False}, 
                    { 'id': 21, 'date': "2018-07-01", 'amount':  -7.6, 'tags' : ["HOBBIES", "CINEMA"], 'checked': True}, 
                    { 'id': 22, 'date': "2018-07-02", 'amount':  -5.6, 'tags' : ["FOOD", "SANDWICH"], 'checked': True}, 
                    { 'id': 23, 'date': "2018-07-08", 'amount':  -250, 'tags' : ["SAVING", "LIVA"], 'checked': False}, 
                    { 'id': 24, 'date': "2018-07-08", 'amount':  -50.00, 'tags' : ["SAVING", "PEL"], 'checked': False}, 
                ]
            }
        ]
    }
]


class AccountsStorage(object):
    def getAccounts(self) :
        return [ {'id': account['id'], 'name' : account['name']} for account in data ]

    def getAccount(self, id):
        for account in data :
            if account['id'] == id:
                return account
        return {}

    def addAccount(self, name):
        account = {'id': len(data)+1, 'name' : name}
        data.append(account)
        return account