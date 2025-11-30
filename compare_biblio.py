import time
import random
from LWE_biblio import lwe_biblio
from Paillier_biblio import Paillier_biblio

class Compare_algo:
    def __init__(self, iteracoes = 100, poly_modylus_degree=4096):
        self.iteracoes = iteracoes
        self.poly_modulus_degree = poly_modylus_degree
        
        self.pai = Paillier_biblio()
        self.lwe = lwe_biblio(poly_modulus_degree=self.poly_modulus_degree)
    
    def time_paillier(self):
        start = time.perf_counter()
        self.pai.gerar_chaves()
        end = time.perf_counter()
        temp_keygen = end - start
        
        tempos_enc = []
        tempos_somas = []
        tempos_dec = []
        
        for _ in range(self.iteracoes):
            v1 = random.randint(1, 1000)
            v2 = random.randint(1, 1000)
            
            start = time.perf_counter()
            c1 = self.pai.encripty_text(v1)
            end = time.perf_counter()
            tempos_enc.append(end-start)
            
            c2 = self.pai.encripty_text(v2)
            
            #Soma
            start = time.perf_counter()
            c_soma = self.pai.soma_text(c1, c2)
            end = time.perf_counter()
            tempos_somas.append(end-start)
            
            #Decrypt
            start = time.perf_counter()
            plain_text = self.pai.decrypt_text(c_soma)
            end = time.perf_counter()
            tempos_dec.append(end-start)
        
        avg_enc = sum(tempos_enc) / self.iteracoes
        avg_soma = sum(tempos_somas) / self.iteracoes
        avg_dec = sum(tempos_dec) / self.iteracoes
        
        return temp_keygen, avg_enc, avg_soma, avg_dec
    
    def time_lwe(self):
        start = time.perf_counter()
        self.lwe.lwe_keygen()
        end = time.perf_counter()
        tempo_keygen = end-start
        
        tempos_enc = []
        tempos_somas = []
        tempos_dec = []
        
        for _ in range(self.iteracoes):
            v1 = [random.randint(1, 1000)]
            v2 = [random.randint(1, 1000)]
            
            start = time.perf_counter()
            c1 = self.lwe.encrypt_text(v1)
            end = time.perf_counter()
            tempos_enc.append(end-start)
            
            c2 = self.lwe.encrypt_text(v2)
            
            #Soma
            start = time.perf_counter()
            c_soma = self.lwe.soma(c1, c2)
            end = time.perf_counter()
            tempos_somas.append(end-start)
            
            #Decrypt
            start = time.perf_counter()
            plain_text = self.lwe.decrypt_text(c_soma)
            end = time.perf_counter()
            tempos_dec.append(end-start)
            
            avg_enc = sum(tempos_enc) / self.iteracoes
            avg_soma = sum(tempos_somas) / self.iteracoes
            avg_dec = sum(tempos_dec) / self.iteracoes
            
        return tempo_keygen, avg_enc, avg_soma, avg_dec
    
    def comparacao_relatorio(self):
        pai_key, pai_enc, pai_sum, pai_dec = self.time_paillier()
        lwe_key, lwe_enc, lwe_sum, lwe_dec = self.time_lwe()
        
        print(f"Comparação de tempo dos algoritmos com {self.iteracoes} iterações:")
        print("-"*100)
        print(f"{'Operação (Tempo Médio)':<25} | {'Paillier (Escalar)':<20} | {'LWE (Vetorial)':<20} | {'Melhor Tempo':<15}")
        print("-" * 95)

        
        print(f"{'Geração de Chaves':<25} | {f'{pai_key:.4f} s':<20} | {f'{lwe_key:.4f} s':<20} | {'LWE' if lwe_key < pai_key else 'Paillier':<15}")
        
        print(f"{'Encriptação':<25} | {f'{pai_enc:.6f} s':<20} | {f'{lwe_enc:.6f} s':<20} | {'LWE' if lwe_enc < pai_enc else 'Paillier':<15}")
        
        print(f"{'Soma Homomórfica':<25} | {f'{pai_sum:.6f} s':<20} | {f'{lwe_sum:.6f} s':<20} | {'LWE' if lwe_sum < pai_sum else 'Paillier':<15}")
        
        print(f"{'Decriptação':<25} | {f'{pai_dec:.6f} s':<20} | {f'{lwe_dec:.6f} s':<20} | {'LWE' if lwe_dec < pai_dec else 'Paillier':<15}")
        
        print("=" * 95)

if __name__ == "__main__":
    comparar = Compare_algo(iteracoes=100, poly_modylus_degree=4096)
    
    comparar.comparacao_relatorio()