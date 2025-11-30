import tenseal as ts

class lwe_biblio:
    def __init__(self, poly_modulus_degree = 4096, plain_modulus=1032193):
        self.poly_modulus_degree = poly_modulus_degree
        self.plain_modulus=plain_modulus
        self.context = None
        self.N = poly_modulus_degree
    
    def lwe_keygen(self):
        self.context = ts.context(
            ts.SCHEME_TYPE.BFV, #BFV pois iremos trabalhar em 1D e valores inteiros
            poly_modulus_degree = self.poly_modulus_degree,
            plain_modulus = self.plain_modulus
        )
    
    def encrypt_text(self, vetor):
        if self.context == None:
            raise Exception("Contexto não gerado")
        
        cipher = ts.bfv_vector(self.context, vetor)
        return cipher
    
    def soma(self, cipher1, cipher2):
        return cipher1 + cipher2
    
    def decrypt_text(self, cipher):
        return cipher.decrypt()

if __name__ == "__main__":    
    lwe = lwe_biblio()
    lwe.lwe_keygen()
    a = [7]
    b = [25]

    cifrado_a = lwe.encrypt_text(a)
    cifrado_b = lwe.encrypt_text(b)

    cifrado_soma = lwe.soma(cifrado_a, cifrado_b)
    
    
   
    resultado_final = lwe.decrypt_text(cifrado_soma)

    valido = (resultado_final[0] == a[0] + b[0]) and \
             (resultado_final[-1] == a[-1] + b[-1])
    
    print(f"Validação matemática: {'SUCESSO' if valido else 'FALHA'}")
    print(resultado_final)