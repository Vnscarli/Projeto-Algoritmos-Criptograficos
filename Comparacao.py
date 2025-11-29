import time
from LWE import LWEAlgo
from Paillier import PaillierAlgo

def compare_algo(iteracoes):
    val1 = 43
    val2 = 5
    
    lwe = LWEAlgo(n=512, message_size=10000)
    paillier = PaillierAlgo(key_size=512)
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
    
    print("\nTentando quebrar o LWE com excesso de somas...")
    acc_lwe = lwe.encrypt(0)
    limit = 2000 
    val_add = 100
    failed = False
    
    for i in range(1, limit):
        acc_lwe = lwe.add(acc_lwe, lwe.encrypt(val_add))
        if i % 100 == 0:
            res = lwe.decrypt(acc_lwe)
            expected = i * val_add
            if res != expected:
                print(f"LWE FALHOU na iteração {i}. Esperado: {expected}, Obteve: {res}")
                failed = True
                break
    if not failed:
        print(f"LWE aguentou {limit} somas sem falhar (com os parâmetros atuais)!")
    else:
        print("Paillier aguentaria essas somas infinitamente (até estourar 2048 bits).")

if __name__ == "__main__":
    compare_algo(1000)