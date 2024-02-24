def extract(packet):
    src_port = int(packet[:16], 2)
    dest_port = int(packet[16:32], 2)
    seq_num = int(packet[32:64], 2)
    ack_num = int(packet[64:96], 2)
    window = int(packet[96:112], 2)
    data_flag = int(packet[112:113], 2)
    payload_length = int(packet[113:129], 2)
    payload = packet[129:129+payload_length].decode()

    return {
        'src_port': src_port,
        'dest_port': dest_port,
        'seq_num': seq_num,
        'ack_num': ack_num,
        'window': window,
        'payload': payload,
        'data_flag': data_flag
    }
