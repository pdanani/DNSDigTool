import dns.message
import dns.query
import datetime
import time

roots = ["198.41.0.4", "199.9.14.201", "192.33.4.12", "199.7.91.13", "192.203.230.10", "192.5.5.241", "192.112.36.4",
         "198.97.190.53", "192.36.148.17", "192.58.128.30", "193.0.14.129", "199.7.83.42", "202.12.27.33"]
root = roots[1]
global initDomain


def main(domain: str):
    return ResolveDNS(domain, root)


def ResolveDNS(domain: str, server):
    query = dns.message.make_query(domain, 'A')
    response = dns.query.udp(query, server)

    if (len(response.answer) > 0):
        strAnswer = response.answer[0].to_text()
        first = strAnswer.split(' ')[0]
        second = strAnswer.split(' ')[1]
        third = strAnswer.split(' ')[2]
        fourth = strAnswer.split(' ')[3]
        fifth = strAnswer.split(' ')[4]
        if ("CNAME" in fourth):  # resolve CNAME
            return ResolveDNS(fifth, root)
        if ("A" in fourth):  # this means we have resolved ip
            ## Now deal with printing the response given from udp

            if (initDomain == domain):
                print(str(response)[str(response).find("QUESTION"):str(response).find(
                    "AUTHORITY")])  # slices string to question and answer only
                                                          # find total length

            return response.answer
    elif (len(response.additional) > 0):
        i = 0
        while response.additional[i] != None:  # check additional to collect an ip if available
            if "AA" not in response.additional[i].to_text().split(' ')[3]:  # anything with more than one A is ejected
                give=response.additional[i].to_text().split(' ')[4].split('\n')[0]
                return ResolveDNS(domain, give)  # resolve
            i += 1
    else:  # resolve name server if must

        try:
            i = 0
            ns = response.authority[i].to_text()  # collect nameserver
            ns = ns.split('\n')[0]  # this splits authority and takes first ns available
            while (ns != None):
                nstoip = ResolveDNS(ns.split(' ')[4], root)  # first find the ip related to the name server
                return ResolveDNS(domain, nstoip[0].to_text().split(' ')[4])  #
        except dns.exception.DNSException:
            exit()


if __name__ == '__main__':
    domain = input("Input a domain:")
    initDomain = domain
    start = time.time()
    try:
        main(domain)
    except dns.exception.DNSException:
        exit()
    finish = time.time()
    total = finish - start
    print("Query", total, "Seconds")
    stamp = datetime.datetime.now()
    print("\nWhen:", stamp)
