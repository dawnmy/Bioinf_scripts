from random import randint
from numpy import sin
 
def decode(g):
    return [((g&0xfff) - 2048) * 0.001, ((g>>12) - 2048) * 0.001]
 
def function_g(g):
    x = decode(g)
    return function(x[0], x[1])
     
def function(x, y):
    return 100 * (sin(x) ** 2 - sin(y)) ** 2 + (1 - sin(x)) ** 2
 
def cmp(g1, g2):
    key = function_g(g1) - function_g(g2)
    if key > 0: return 1
    elif key < 0: return -1
    else: return 0
 
def GA(num = 30, round = 10):
    gene = [randint(0, (1<<24) - 1) for i in range(num)]
    rnd = 0
    while rnd < round:
        rnd += 1
        gene_c = [g ^ (1<<randint(0, 23))  for g in gene]
        gene_h = []
        for g1 in gene:
            for g2 in gene:
                mask = (1<<randint(1, 23)) - 1
                gene_h.append(g2 & ~mask | g1 & mask)
                gene_h.append(g1 & ~mask | g2 & mask)
        gene_tot = gene + gene_h + gene_c
        gene_tot.sort(cmp = cmp, reverse = True)
        gene = gene_tot[:num]
        print "round", rnd, ":", decode(gene[0]), function_g(gene[0])
    return decode(gene[0]) + [function_g(gene[0])]
     
if __name__ == '__main__':
    print GA(30, 10),
