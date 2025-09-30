from app.tools.user_db import get_user_profile, get_user_transactions

class SupportAgent:
    def __init__(self):
        self.tools = {
            "get_profile": get_user_profile,
            "get_transactions": get_user_transactions
        }

    def handle_support(self, message: str, user_id: str):
        profile = self.tools["get_profile"](user_id)
        txs = self.tools["get_transactions"](user_id)

        msg = message.lower()
        if "transferir" in msg or "transferência" in msg or "transfer" in msg:
            if not profile:
                return {"answer": "Não encontrei seu usuário. Verifique o user_id fornecido. Posso redirecionar para um atendente humano.", "sources": []}
            if profile.get("balance",0) <= 0:
                return {"answer": f"Olá {profile.get('name')}. Pelo nosso sistema, seu saldo atual é R$ {profile.get('balance'):.2f}. Não é possível efetuar transferências sem saldo. Deseja abrir um chamado?", "sources": []}
            return {"answer": f"Olá {profile.get('name')}. Seu saldo é R$ {profile.get('balance'):.2f}. As transferências podem falhar por limite ou por bloqueios de segurança. Recomendo checar seu extrato recente: {len(txs)} transações encontradas.", "sources": []}
        if "login" in msg or "entrar" in msg or "senha" in msg:
            return {"answer": "Se estiver com problemas de login, tente redefinir sua senha pelo app. Se a dificuldade persistir, solicite direcionamento para um atendente humano.", "sources": []}
        if txs:
            sample = txs[:3]
            lines = "\n".join([f"- {t['date']}: {t['type']} R$ {t['amount']} ({t['desc']})" for t in sample])
            return {"answer": f"Encontrei as seguintes transações recentes:\n{lines}\nSe precisar de detalhe, peça 'detalhar transações'.", "sources": []}
        return {"answer": "Não encontrei informações adicionais. Deseja que eu abra um chamado para um atendente humano?", "sources": []}
