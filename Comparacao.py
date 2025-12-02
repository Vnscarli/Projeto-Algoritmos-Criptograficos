import time
from LWE import LWEAlgo
from Paillier import PaillierAlgo
import random

def compare_algo(iteracoes):
    val1 = random.randint(1, 1000)
    val2 = random.randint(1, 1000)
    
    lwe = LWEAlgo(n=1175, q=2**32, message_size=10000)
    paillier = PaillierAlgo(key_size=3072)
    start = time.perf_counter()
    lwe.keygen()
    lwe_keygen_time = (time.perf_counter() - start) / iteracoes
    
    start = time.perf_counter()
    paillier.keygen()
    pai_keygen_time = (time.perf_counter() - start) / iteracoes
    
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
    
    limit = 1000
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
    compare_algo(100)