# Using dpkt for parsing
import dpkt
import socket
import tabulate

# Global data structure for storing the dns
dns_db = {}

# function to modulize reading from the the pcap
def read_from_pcap(open_pcap):
    counter = 1
    for _, packet in open_pcap:
        ethernet_packet = dpkt.ethernet.Ethernet(packet)
        if isinstance(ethernet_packet.data, dpkt.ip.IP):
            if isinstance(ethernet_packet.data.data, dpkt.udp.UDP):
                udp = ethernet_packet.data.data
                if udp.sport == 53 or udp.dport == 53:
                    dns = dpkt.dns.DNS(udp.data)
                    if dns.opcode == dpkt.dns.DNS_QUERY and dns.qr == dpkt.dns.DNS_R:
                        query_list = []
                        answer_list = []
                        for query in dns.qd:
                            if query.type == dpkt.dns.DNS_A:
                                query_list.append(query.name)
                        for answer in dns.an:
                            if answer.type == dpkt.dns.DNS_A:
                                answer_list.append(socket.inet_ntoa(answer.ip))
                        if query_list and answer_list:
                            dns_db[counter] = {}
                            dns_db[counter]['Query'] = query_list
                            dns_db[counter][ 'Answer'] = answer_list
        counter += 1


def create_data():
    result_list = []
    for k, v in dns_db.items():
        loop_result = []
        loop_result.append(k) 
        loop_result.append(v [ 'Query']) 
        loop_result.append(v[ 'Answer'])
        result_list.append(loop_result)
    
    return result_list

def display(result_list):
    print(tabulate.tabulate(result_list, headers=['Packet ID', 'Query', 'Answers']))

def main():
    pcap = r'assets\week11_dns.pcap'
    # Read file from source 
    open_pcap = dpkt.pcap.Reader(open(pcap, 'rb'))
    read_from_pcap(open_pcap)
    data = create_data()
    display(data)

if __name__ == "__main__":
    main()