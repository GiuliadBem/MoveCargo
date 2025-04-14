from modelos.pessoa import Pessoa
import hashlib

class Login:
    @classmethod
    def authenticate(cls, usuario: Pessoa, password: str, sessao):
        hashed_input = hashlib.sha256(password.encode()).hexdigest()
        if usuario.senha == hashed_input:
            sessao.login(usuario)  # Update session
            return True
        return False