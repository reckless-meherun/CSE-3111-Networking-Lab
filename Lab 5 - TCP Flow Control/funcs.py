import struct

def create_tcp_packet(source_port, destination_port, sequence_number, acknowledgment_number,window_size, payload, data_flag=1):
    # TCP Header Format
    if type(payload) == str:
        payload = payload.encode()

    tcp_header = struct.pack('!HHLLLBL',
                             source_port,         
                             destination_port,    
                             sequence_number,     
                             acknowledgment_number,  
                             len(payload),  
                             data_flag,    
                             window_size,         
                             )                   
    tcp_packet = tcp_header+ payload

    return tcp_packet


def decode_tcp_packet(tcp_packet):
    # Unpack TCP header
    tcp_header = struct.unpack('!HHLLLBL', tcp_packet[:21])

    source_port = tcp_header[0]
    destination_port = tcp_header[1]
    sequence_number = tcp_header[2]
    acknowledgment_number = tcp_header[3]
    payload_length = tcp_header[4]
    data_flag = tcp_header[5]  
    window_size = tcp_header[6]

    # Extract payload
    payload:bytes = tcp_packet[21:]
    
    return {
        'source_port': source_port,
        'destination_port': destination_port,
        'sequence_number': sequence_number,
        'acknowledgment_number': acknowledgment_number,
        'payload_length':payload_length,
        'data_flag': data_flag,
        'window_size': window_size,
        'payload': payload
    }

