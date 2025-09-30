USERS = {
    "client123": {"name": "João Silva", "status": "active", "balance": 150.00},
    "client789": {"name": "Maria Souza", "status": "active", "balance": 0.0},
}

TRANSACTIONS = {
    "client123": [
        {"id":"t1","type":"credit","amount":100,"date":"2025-08-01","desc":"Venda"},
        {"id":"t2","type":"debit","amount":50,"date":"2025-08-02","desc":"Saque"},
    ],
    "client789": [
        {"id":"t3","type":"credit","amount":0,"date":"2025-08-01","desc":"Tentativa falha"},
    ],
}

def get_user_profile(user_id):
    return USERS.get(user_id, None)

def get_user_transactions(user_id, limit=10):
    return TRANSACTIONS.get(user_id, [])[:limit]
