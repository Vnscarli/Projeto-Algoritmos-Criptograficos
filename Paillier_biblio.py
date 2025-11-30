from phe import paillier

class Paillier_biblio:
    def __init__(self):
        self.public_key = None
        self.private_key = None
    
    def gerar_chaves(self):
        self.public_key, self.private_key = paillier.generate_paillier_keypair()
        return self.public_key, self.private_key
    
    def encripty_text(self, text):
        encrypted_text = self.public_key.encrypt(text)
        return encrypted_text
    
    def soma_text(self, cipher1, cipher2):
        encrypt_soma = cipher1 + cipher2
        return encrypt_soma
    
    def decrypt_text(self, enc_text):
        plain_text = self.private_key.decrypt(enc_text)
        return plain_text
    
if __name__ == "__main__":
    pai = Paillier_biblio()
    pai.gerar_chaves()
    
    a = 94
    b = 6
    
    encrypt_a = pai.encripty_text(a)
    encrypt_b = pai.encripty_text(b)
    
    soma_enc = pai.soma_text(encrypt_a, encrypt_b)
    
    soma_dec = pai.decrypt_text(soma_enc)
    
    print(soma_dec==a+b)
    print(soma_dec)
    print(a+b)
    
        