from problem import FScoreStepDetection



def precision(detected_steps,steps):
    n=len(detected_steps)
    p=0
    counted=list()
    for s in detected_steps:
        temp=(s[1]+s[0])/2
        for j in range(len(steps)):
            k=steps[j]
            if (k[0]<=temp<=k[1])&(k not in counted):
                p=p+1
                counted.append(k)
                break
    if (n==0):
        return 0
    else:
        return p/n


def recall(detected_steps,steps):
    
    return precision(steps,detected_steps)

def f_score1(detected_steps,steps):
    p=precision(detected_steps,steps)
    r=recall(detected_steps,steps)
    fscore = FScoreStepDetection()([steps], [detected_steps])
    if (p+r==0):
        return 0
    return(2*p*r/(p+r))

def f_score(detected_steps,steps):
    fscore = FScoreStepDetection()([steps], [detected_steps])
    return fscore