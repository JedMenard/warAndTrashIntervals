from warAndTrash import play
from math import sqrt

def main(n, randomFile):
    t = 1.645
    try:
        random = open(randomFile, 'r')
    except IOError:
        print "Unable to open file."
        exit(1)

    for i in range(int(n)):
        Nbar, _, Lbar = play('war', random)
        Nbar = 1. if Nbar > 700 else 0.
        Lbar = 1. if Lbar > 0.8 else 0.
        count = 1
        vN = 0
        vL = 0

        while (count < 40 or 1./5 < (t / sqrt(count - 1))):
            N, _, L = play('war', random)
            N = 1 if N > 700 else 0
            L = 1 if L > 0.8 else 0
            
            count += 1
            
            dN = N - Nbar
            dL = L - Lbar
            
            vN += ((count - 1.)/count) * dN**2
            vL += ((count - 1.)/count) * dL**2

            Nbar += dN/count
            Lbar += dL/count


        Nw = sqrt(vN/count)/5
        Lw = sqrt(vL/count)/5

        print "OUTPUT :war-last: {} {} {}".format(Lbar - Lw, Lbar, Lbar + Lw)
        print "OUTPUT :war-n: {} {} {}".format(Nbar - Nw, Nbar, Nbar + Nw)



        Nbar, _, Lbar = play('trash', random)
        Nbar = 1. if Nbar > 125 else 0.
        Lbar = 1. if Lbar > 0.8 else 0.
        count = 1
        vN = 0
        vL = 0

        while (count < 40 or 1./5 < (t / sqrt(count - 1))):
            N, _, L = play('trash', random)
            N = 1 if N > 125 else 0
            L = 1 if L > 0.8 else 0
            
            count += 1
            
            dN = N - Nbar
            dL = L - Lbar
            
            vN += ((count - 1.)/count) * dN**2
            vL += ((count - 1.)/count) * dL**2

            Nbar += dN/count
            Lbar += dL/count


        Nw = sqrt(vN/count)/5
        Lw = sqrt(vL/count)/5

        print "OUTPUT :trash-last: {} {} {}".format(Lbar - Lw, Lbar, Lbar + Lw)
        print "OUTPUT :trash-n: {} {} {}".format(Nbar - Nw, Nbar, Nbar + Nw)
        
        






























if __name__ == '__main__':
    main(1, '../random/uniform-0-1-00.dat')
