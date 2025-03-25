#include <stdio.h> 
#include <stdlib.h>
#include <pcap.h>
#include <arpa/inet.h>
#include <netinet/ether.h>
#include <ctype.h>  // isprint() 함수 쓰려면 필요

/* Ethernet Header */
struct ethheader {
    u_char ether_dhost[6]; /* destination host address */
    u_char ether_shost[6]; /* source host address */
    u_short ether_type;    /* protocol type (IP, ARP, RARP, etc) */
};

/* IP Header */
struct ipheader {
    unsigned char      iph_ihl:4, //IP header length
										   iph_ver:4; //IP version
    unsigned char      iph_tos; //Type of service
    unsigned short int iph_len; //IP Packet length (data + header)
    unsigned short int iph_ident; //Identification
    unsigned short int iph_flag:3, //Fragmentation flags
									     iph_offset:13; //Flags offset
    unsigned char      iph_ttl; //Time to Live
    unsigned char      iph_protocol; //Protocol type
    unsigned short int iph_chksum; //IP datagram checksum
    struct in_addr     iph_sourceip; //Source IP address
    struct in_addr     iph_destip; //Destination IP address
};

/* TCP Header */
struct tcpheader {
    u_short tcp_sport;      /* source port */
    u_short tcp_dport;      /* destination port */
    u_int   tcp_seq;        /* sequence number */
    u_int   tcp_ack;        /* acknowledgement number */
    u_char  tcp_offx2;      /* data offset, rsvd */
#define TH_OFF(th)  (((th)->tcp_offx2 & 0xF0) >> 4)
    u_char  tcp_flags;
    u_short tcp_win;        /* window */
    u_short tcp_sum;        /* checksum */
    u_short tcp_urp;        /* urgent pointer */
};

/* 패킷 처리 함수 */
void got_packet(u_char *args, const struct pcap_pkthdr *header, const u_char *packet) {
    struct ethheader *eth = (struct ethheader *)packet;

    // IP 패킷인지 확인
    if (ntohs(eth->ether_type) == 0x0800) {
        struct ipheader *ip = (struct ipheader *)(packet + sizeof(struct ethheader));

        // TCP 프로토콜만 처리
        if (ip->iph_protocol == IPPROTO_TCP) {
            int ip_header_len = ip->iph_ihl * 4;
            struct tcpheader *tcp = (struct tcpheader *)(packet + sizeof(struct ethheader) + ip_header_len);

            // Ethernet Header 출력
            printf("==== Ethernet Header ====\n");
            printf("Src MAC: %02x:%02x:%02x:%02x:%02x:%02x\n",
                   eth->ether_shost[0], eth->ether_shost[1], eth->ether_shost[2],
                   eth->ether_shost[3], eth->ether_shost[4], eth->ether_shost[5]);
            printf("Dst MAC: %02x:%02x:%02x:%02x:%02x:%02x\n",
                   eth->ether_dhost[0], eth->ether_dhost[1], eth->ether_dhost[2],
                   eth->ether_dhost[3], eth->ether_dhost[4], eth->ether_dhost[5]);

            // IP Header 출력
            printf("==== IP Header ====\n");
            printf("Src IP: %s\n", inet_ntoa(ip->iph_sourceip));
            printf("Dst IP: %s\n", inet_ntoa(ip->iph_destip));

            // TCP Header 출력
            printf("==== TCP Header ====\n");
            printf("Src Port: %u\n", ntohs(tcp->tcp_sport));
            printf("Dst Port: %u\n", ntohs(tcp->tcp_dport));

            int tcp_header_len = TH_OFF(tcp) * 4;
            int total_header_size = sizeof(struct ethheader) + ip_header_len + tcp_header_len;
            int payload_len = header->caplen - total_header_size;
            const u_char *payload = packet + total_header_size;

            printf("==== Payload (%d bytes) ====\n", payload_len);
            for (int i = 0; i < payload_len && i < 64; i++) {
                if (isprint(payload[i])) printf("%c", payload[i]);
                else printf(".");
            }
            printf("\n");

            printf("\n...........Next One..........\n");
        }
    }
}

int main()
{
  pcap_t *handle;
  char errbuf[PCAP_ERRBUF_SIZE];
  struct bpf_program fp;
  char filter_exp[] = "tcp";
  bpf_u_int32 net;

  // Step 1: Open live pcap session on NIC with name enp0s3
  handle = pcap_open_live("enp0s3", BUFSIZ, 1, 1000, errbuf);
  if (handle == NULL) {
      fprintf(stderr, "Couldn't open device enp0s3: %s\n", errbuf);
      return 2;
  }

  // Step 2: Compile filter_exp into BPF pseudo-code
  if (pcap_compile(handle, &fp, filter_exp, 0, net) == -1) {
      pcap_perror(handle, "Compile Error:");
      return 2;
  }
  if (pcap_setfilter(handle, &fp) != 0) {
      pcap_perror(handle, "Filter Error:");
      return 2;
  }

  // Step 3: Capture packets
  printf("Start sniffing TCP packets...\n");
  pcap_loop(handle, -1, got_packet, NULL);

  pcap_close(handle);   // Close the handle
  return 0;
}
