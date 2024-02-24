def make_pkt(src_port,dest_port,seq_num,ack_num,window,payload: str|bytes,data_flag):
    if type(payload)==str:
        payload = payload.encode()
    
    header = f'{src_port:016b}{dest_port:016b}{seq_num:032b}{ack_num:032b}{len(payload):016b}{data_flag:01b}{window:016b}'.encode()


    packet = header + payload

    return packet

def extract(packet):
    src_port = int(packet[:16], 2)
    dest_port = int(packet[16:32], 2)
    seq_num = int(packet[32:64], 2)
    ack_num = int(packet[64:96], 2)
    window = int(packet[113:129], 2)
    data_flag = int(packet[112:113], 2)
    payload_length = int(packet[96:112], 2)
    payload = packet[129:129+payload_length]

    return {
        'src_port': src_port,
        'dest_port': dest_port,
        'seq_num': seq_num,
        'ack_num': ack_num,
        'window': window,
        'payload': payload,
        'data_flag': data_flag
    }

