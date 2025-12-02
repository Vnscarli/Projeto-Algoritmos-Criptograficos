import numpy as np


class LWEAlgo:
    def __init__(self, n=1175, q=2**32, sigma = 3.0, message_size=100000):
        self.n = n
        self.q = q
        self.sigma = sigma
        self.message_size = message_size
        self.delta = int(self.q // self.message_size)
        
        self.s = None
        self.A = None
        self.public_b = None
        
    def keygen(self):
        self.s = np.random.randint(0, self.q, self.n, dtype=np.int64)
        
        self.A = np.random.randint(0, self.q, (self.n, self.n), dtype=np.int64)
        
        e = np.random.normal(0, self.sigma, self.n).astype(np.int64)
        self.public_b = (np.dot(self.A, self.s) + e) % self.q
        
        return (self.s, self.A, self.public_b)
    
    def encrypt(self, m):
        if self.s is None:
            raise ValueError("Chaves não geradas!")
        
        a = np.random.randint(0, self.q, self.n, dtype=np.int64)
        
        error = int(np.random.normal(0, self.sigma))
        #
        
        dot_product = np.dot(a, self.s) % self.q
        
        scaled_m = (m * self.delta) % self.q
        
        b = (dot_product + error + scaled_m) % self.q
        
        return (a, b)
    
    def decrypt(self, ciphertext):
        if self.s is None:
            raise ValueError("Chave não encontrada!")
        
        a, b = ciphertext
        
        dot_product = np.dot(a, self.s) % self.q
        
        noisy_m = (b - dot_product) % self.q
        
        if noisy_m > self.q / 2:
            noisy_m -= self.q
        
        m_approx = round(noisy_m / self.delta)
        
        return int(m_approx)
    
    def add(self, cipher1, cipher2):
        return ((cipher1[0] + cipher2[0]) % self.q, (cipher1[1] + cipher2[1]) % self.q)
    
if __name__ == "__main__":
    lwe = LWEAlgo(n=512, q=2**32, sigma=3.0, message_size=1000)
    
    lwe.keygen()
    
    mensagem1 = 34
    mensagem2 = 42
    ct1 = lwe.encrypt(mensagem1)
    ct2 = lwe.encrypt(mensagem2)
    
    cipher_sum = lwe.add(ct1, ct2)
    
    decrypt_sum = lwe.decrypt(cipher_sum)
    
    print(f"Mensagem 1: {mensagem1}")
    print(f"Mensagem 2: {mensagem2}")
    print(f"Soma normal: {mensagem1+mensagem2}")
    print(f"Soma decifrada: {decrypt_sum}")