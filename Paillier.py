import secrets
import math
import random


def miller_rabin(n, k=40):
    if n == 2 or n == 3: return True
    if n % 2 == 0 or n < 2: return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = secrets.randbelow(n - 4) + 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else: return False
    return True

def achar_primo(nbits):
    while True:
        p = secrets.randbits(nbits)
        p |= (1<<(nbits-1)) | 1
        if miller_rabin(p): 
            return p

class PaillierAlgo:
    def __init__(self, key_size=3072):
        self.keysize = key_size
        self.n = None
        self.lam = None
        self.mu = None
        self.n_sq = None
    
    def keygen(self):
        prime_len = self.keysize // 2
        p = achar_primo(prime_len)
        q = achar_primo(prime_len)
        while p == q:
            q = achar_primo(prime_len)
        
        self.n = p * q
        self.n_sq = self.n * self.n
        self.lam = abs(p-1) * abs(q-1) // math.gcd(p-1, q-1)
        self.mu = pow(self.lam, -1, self.n)
        
    
    def encrypt(self, m):
        if self.n is None:
            raise ValueError("Chaves não geradas!")
        r = random.randint(1,self.n - 1)
        gm = (1 + m * self.n) % self.n_sq
        rn = pow(r, self.n, self.n_sq)
        c = (gm * rn) % self.n_sq
        return c
    
    def decrypt(self, c):
        if self.n is None:
            raise ValueError("Chaves não encontradas!")
        u = pow(c, self.lam, self.n_sq)
        l_u = (u - 1) // self.n
        m = (l_u * self.mu) % self.n
        return m
    
    def add(self, cipher1, cipher2):
        return (cipher1 * cipher2) % self.n_sq
    
if __name__ == "__main__":
    paillier = PaillierAlgo(key_size=3072)
    paillier.keygen()
    
    m1 = 54
    m2 = 43
    
    c1 = paillier.encrypt(m1)
    c2 = paillier.encrypt(m2)
    
    c_sum = paillier.add(c1, c2)
    d_sum = paillier.decrypt(c_sum)
    print(f"A soma de {m1} e {m2} decriptada é {d_sum} (={m1+m2})")