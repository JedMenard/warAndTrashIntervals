from warAndTrash import play
from math import sqrt

def main(n, randomFile):
    t = 1.645
    try:
        random = open(randomFile, 'r')
    except IOError:
        print "Error opening file."
        exit(1)

    totalWarNbar = 0
    totalWarLbar = 0
    totalTrashNbar = 0
    totalTrashLbar = 0

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

        totalWarNbar += Nbar
        totalWarLbar += Lbar


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

        totalTrashNbar += Nbar
        totalTrashLbar += Lbar


        Nw = sqrt(vN/count)/5
        Lw = sqrt(vL/count)/5

        print "OUTPUT :trash-last: {} {} {}".format(Lbar - Lw, Lbar, Lbar + Lw)
        print "OUTPUT :trash-n: {} {} {}".format(Nbar - Nw, Nbar, Nbar + Nw)


    warNp = totalWarNbar / n
    warNs = sqrt(warNp*(1-warNp))
    warN2w = 2*warNs/5
    
    warLp = totalWarLbar / n
    warLs = sqrt(warLp*(1-warLp))
    warL2w = 2*warLs/5
    
    trashNp = totalTrashNbar / n
    trashNs = sqrt(trashNp*(1-trashNp))
    trashN2w = 2*trashNs/5
    
    trashLp = totalTrashLbar / n
    trashLs = sqrt(trashLp*(1-trashLp))
    trashL2w = 2*trashLs/5

    print "War N: pHat = {}, sHat = {}, 2w = {}".format(warNp, warNs, warN2w)
    print "War L: pHat = {}, sHat = {}, 2w = {}".format(warNp, warNs, warN2w)
    print "Trash N: pHat = {}, sHat = {}, 2w = {}".format(warNp, warNs, warN2w)
    print "Trash L: pHat = {}, sHat = {}, 2w = {}".format(warNp, warNs, warN2w)
        






























if __name__ == '__main__':
    main(1, '../random/uniform-0-1-00.dat')
