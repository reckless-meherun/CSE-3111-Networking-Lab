# u=a
# v=b
# w=c
# x=d
# y=e
# z=f

adj = {
    'A':{
        'B':2,
        'C':5,
        'D':1,
    },
    'B': {
        'A':2,
        'C':3,
        'D':2,
    },
    'C': {
        'A':5,
        'B':3,
        'D':3,
        'E':1,
        'F':5,
    },
    'D':{
        'A':1,
        'B':2,
        'C':3,
        'E':1,
    },
    'E':{
        'C':1,
        'D':1,
        'F':2,
    },
    'F':{
        'C':5,
        'E':2,
    }
} 

# {
#     'A':{
#         'B':1,
#         'C':2
#     },
#     'B': {
#         'A':1,
#         'C':5,
#         'D':1
#     },
#     'C':{
#         'A':2,
#         'B':5,
#     },
#     'D': {
#         'B':1
#     }

# }