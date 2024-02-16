import random
import pickle

def build_query(message:str,ques_no=1) -> tuple[int,bytes]:
    message,type = message.split()
    id = random.randint(0,65536)
    flag = 0
    ques_no = ques_no
    ans_rr = 0
    auth_rr = 0
    add_rr = 0

    data = {
        'header': {
            'id':id,
            'flag':flag,
            'ques_no': ques_no,
            'ans_rr': ans_rr,
            'auth_rr': auth_rr,
            'add_rr': add_rr,
        },
        'body': {
            'name':message,
            'type':type
        }
    }

    return id,pickle.dumps(data)

def extract_query(data:bytes) -> dict[str,str]:
    return pickle.loads(data)


def build_response(name,answer:tuple[int],ques_id, ans_no=1) -> bytes:
    id = ques_id
    flag = 0
    ques_no = 0
    ans_rr = 1
    auth_rr = 0
    add_rr = 0
    value,type,ttl = answer
    answer = name,value,type,ttl

    data = {
        'header': {
            'id':id,
            'flag':flag,
            'ques_no': ques_no,
            'ans_rr': ans_rr,
            'auth_rr': auth_rr,
            'add_rr': add_rr,
        },
        'body': answer
    }

    return pickle.dumps(data)

def extract_response(data:bytes) -> list[tuple[int,int,int,int]]:
    return pickle.loads(data)



