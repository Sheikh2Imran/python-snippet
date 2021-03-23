# producer / initial source
def producer(sentence, next_coroutine):
    tokens = sentence.split(" ")
    for token in tokens:
        next_coroutine.send(token)
    
    next_coroutine.close()


# intermediat co-routine
def pattern_filter(pattern="ing", next_coroutine=None):
    try:
        while True:
            token = (yield)
            if pattern in token:
                next_coroutine.send(token)
                
    except GeneratorExit:
        print("Done with filtering!")


# sink
def print_token():
    print("I'm sink, i'll print tokens") 
    try:
        while True:
            token = (yield)
            print(token)
            
    except GeneratorExit:
        print("Done with printing!")


if __name__ == "__main__":
    pt = print_token()
    pt.__next__()
    pf = pattern_filter(next_coroutine=pt)
    pf.__next__()
    
    sentence = "Bob is running behind a fast moving car"
    producer(sentence, pf)