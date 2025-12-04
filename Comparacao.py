import time
from LWE import LWEAlgo
from Paillier import PaillierAlgo
import random

def compare_algo(iteracoes, n_lwew, q_lwe, key_paillier):
    val1 = random.randint(1, 1000)
    val2 = random.randint(1, 1000)
    
    lwe = LWEAlgo(n=n_lwew, q=q_lwe, message_size=100000)
    paillier = PaillierAlgo(key_size=key_paillier)
    start = time.perf_counter()
    lwe.keygen()
    lwe_keygen_time = (time.perf_counter() - start) 
    
    start = time.perf_counter()
    paillier.keygen()
    pai_keygen_time = (time.perf_counter() - start) 
    
    start = time.perf_counter()
    for _ in range(iteracoes):
        lwe.encrypt(val1)
    lwe_enc_time = (time.perf_counter() - start) / iteracoes
    
    start = time.perf_counter()
    for _ in range(iteracoes):
        paillier.encrypt(val1)
    pai_enc_time = (time.perf_counter() - start) / iteracoes
    
    c1_lwe = lwe.encrypt(val1)
    c2_lwe = lwe.encrypt(val2)
    c1_pai = paillier.encrypt(val1)
    c2_pai = paillier.encrypt(val2)
    
    start = time.perf_counter()
    for _ in range(iteracoes):
        lwe.add(c1_lwe, c2_lwe)
    lwe_add_time = (time.perf_counter() - start) / iteracoes
    
    start = time.perf_counter()
    for _ in range(iteracoes):
        paillier.add(c1_pai, c2_pai)
    pai_add_time = (time.perf_counter() - start) / iteracoes
    
    c_sum_lwe = lwe.add(c1_lwe, c2_lwe)
    c_sum_pai = paillier.add(c1_pai, c2_pai)
    
    start = time.perf_counter()
    for _ in range(iteracoes):
        lwe.decrypt(c_sum_lwe)
    lwe_dec_time = (time.perf_counter() - start) / iteracoes
    
    start = time.perf_counter()
    for _ in range(iteracoes):
        paillier.decrypt(c_sum_pai)
    pai_dec_time = (time.perf_counter() - start) / iteracoes
    
    print("\n" + "="*40)
    print(f"{'Operação':<15} | {'LWE (ms)':<10} | {'Paillier (ms)':<10} | {'Vencedor'}")
    print("-" * 55)
    
    def to_ms(t): return f"{t*1000:.4f}"
    
    print(f"{'Key_gen':<15} | {to_ms(lwe_keygen_time):<10} | {to_ms(pai_keygen_time):<10} | {'LWE' if lwe_keygen_time < pai_keygen_time else 'Paillier'}")
    print(f"{'Encriptação':<15} | {to_ms(lwe_enc_time):<10} | {to_ms(pai_enc_time):<10} | {'LWE' if lwe_enc_time < pai_enc_time else 'Paillier'}")
    print(f"{'Soma (+)':<15} | {to_ms(lwe_add_time):<10} | {to_ms(pai_add_time):<10} | {'LWE' if lwe_add_time < pai_add_time else 'Paillier'}")
    print(f"{'Decriptação':<15} | {to_ms(lwe_dec_time):<10} | {to_ms(pai_dec_time):<10} | {'LWE' if lwe_dec_time < pai_dec_time else 'Paillier'}")
    print("="*40)
    
    print("\nTentando quebrar o LWE com excesso de somas:")
    
    limit = 2000
    failed = False
    acc = random.randint(1, 10)
    acc_lwe = lwe.encrypt(acc)
    
    
    for i in range(1, limit):
        y = random.randint(1, 10)
        acc_lwe = lwe.add(acc_lwe, lwe.encrypt(y))
        expected = acc + y
        acc = lwe.decrypt(acc_lwe)
        
        if acc != expected:
            print(f"LWE FALHOU na iteração {i}. Esperado: {expected}, Obteve: {acc}")
            failed = True
            break
    
    if not failed:
        print(f"LWE aguentou {limit} somas sem falhar (com os parâmetros atuais)!")
    else:
        print("Paillier aguentaria essas somas infinitamente.")

if __name__ == "__main__":
    iteracoes = 1000
    n_lwe1 = 2400 #Equivalente à 128.5 bits
    q_lwe1 = 2**64
    keySize_Paillier = 3072 #Equivalente à 128 bits
    print(f"Rodando a comparação {iteracoes} vezes para os seguintes algoritmos:")
    print()
    print(f"* Paillier com tamanho da chave de {keySize_Paillier}.")
    print(f"* LWE com n={n_lwe1} e q={q_lwe1}.")
    compare_algo(iteracoes=iteracoes, n_lwew=n_lwe1, q_lwe=q_lwe1, key_paillier=keySize_Paillier)
    
    n_lwe2 = 1175 #Equivalente à 130.1 bits
    q_lwe2 = 2**32
    print(f"Rodando a comparação {iteracoes} vezes para os seguintes algoritmos:")
    print()
    print(f"* Paillier com tamanho da chave de {keySize_Paillier}.")
    print(f"* LWE com n={n_lwe2} e q={q_lwe2}.")
    compare_algo(iteracoes=iteracoes, n_lwew=n_lwe2, q_lwe=q_lwe2, key_paillier=keySize_Paillier)
    