import numpy as np

def bandA(a):
    p = [.1, .2]
    return 1 if np.random.random() < p[a-1] else 0

def bandB(a):
    p = [.8, .9]
    return 1 if np.random.random() < p[a-1] else 0

def act(Q, e):
    if np.random.random() < e:
        return np.random.randint(1, 3)
    return np.argmax(Q) + 1

def run():
    n = 1000
    e = 0.1
    
    QA = np.zeros(2)
    NA = np.zeros(2)
    rA = np.zeros(n)
    aA = np.zeros(n)
    
    QB = np.zeros(2)
    NB = np.zeros(2)
    rB = np.zeros(n)
    aB = np.zeros(n)
    
    for t in range(n):
        aA[t] = a = act(QA, e)
        rA[t] = r = bandA(a)
        NA[a-1] += 1
        QA[a-1] += (r - QA[a-1])/NA[a-1]
        
        aB[t] = a = act(QB, e)
        rB[t] = r = bandB(a)
        NB[a-1] += 1
        QB[a-1] += (r - QB[a-1])/NB[a-1]
    
    print(f'Bandit A:\nReward: {np.mean(rA):.3f}\nValues: {QA}\nCounts: {NA}\n')
    print(f'Bandit B:\nReward: {np.mean(rB):.3f}\nValues: {QB}\nCounts: {NB}')

if __name__ == '__main__':
    np.random.seed(42)
    run()