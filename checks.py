import numpy as np


def check_seq(arr, k):
    r,c = arr.shape
    rk, ck = k.shape
    sum_k = np.sum(k)
    if rk!=1 and ck!=1:
        iter_r = r - rk + 1
        iter_c = c - ck + 1
        for i in range(iter_r):
            for j in range(iter_c):
                res = arr[i:i+rk,j:j+ck] * k
                if np.sum(res) >= sum_k:
                    return True
    else:
        if rk==1:
            k = k[0]
        elif ck==1:
            k = k.T[0]
            arr = arr.T
        for row in arr:
            res = np.convolve(row, k, mode='valid')
            if np.any(res==sum_k):
                return True
    return False



def test_checks():
    n = 0
    for r in range(2,8):
        for c in range(2,8):
            for size_k in range(1, min(r, c)):
                kr = np.ones((1, size_k))
                kc = kr.T
                kd = np.eye(size_k)
                kdr = np.fliplr(kd)
                i = np.random.randint(0, r-size_k)
                j = np.random.randint(0, c-size_k)

                arr_r = np.zeros((r,c))
                arr_r[i,j:j+size_k]=1
                res_r = check_seq(arr_r, kr)
                assert res_r, f'{r=}, {c=}, {size_k=}'
                if size_k > 1:
                    res_r = check_seq(arr_r, kc)
                    assert not res_r, f'{r=}, {c=}, {size_k=}'
                    res_r = check_seq(arr_r, kd)
                    assert not res_r, f'{r=}, {c=}, {size_k=}'

                arr_c = np.zeros((r,c))
                arr_c[i:i+size_k,j]=1
                res_c = check_seq(arr_c, kc)
                assert res_c, f'{r=}, {c=}, {size_k=}'
                if size_k > 1:
                    res_c = check_seq(arr_c, kr)
                    assert not res_c, f'{r=}, {c=}, {size_k=}'
                    res_c = check_seq(arr_c, kd)
                    assert not res_c, f'{r=}, {c=}, {size_k=}'

                arr_d = np.zeros((r,c))
                arr_d[(np.arange(i,i+size_k),np.arange(j,j+size_k))]=1
                res_d = check_seq(arr_d, kd)
                assert res_d, f'{r=}, {c=}, {size_k=}'
                if size_k > 1:
                    res_d = check_seq(arr_d, kr)
                    assert not res_d, f'{r=}, {c=}, {size_k=}'
                    res_d = check_seq(arr_d, kc)
                    assert not res_d, f'{r=}, {c=}, {size_k=}'

                arr_dr = np.fliplr(arr_d)
                res_dr = check_seq(arr_dr, kdr)
                assert res_dr, f'{r=}, {c=}, {size_k=}'
                if size_k > 1:
                    res_dr = check_seq(arr_dr, kr)
                    assert not res_dr, f'{r=}, {c=}, {size_k=}'
                    res_dr = check_seq(arr_dr, kc)
                    assert not res_dr, f'{r=}, {c=}, {size_k=}'
                    res_dr = check_seq(arr_dr, kd)
                    assert not res_dr, f'{r=}, {c=}, {size_k=}'
                
                n += 1
    print('%d tests passed' % n)


if __name__=='__main__':
    test_checks()