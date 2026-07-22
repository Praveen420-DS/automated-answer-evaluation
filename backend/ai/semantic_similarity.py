def score(answer,reference):
 a=set(answer.lower().split()); b=set(reference.lower().split())
 return len(a&b)/len(b) if b else 0
