import urllib.request
import argparse
import json
import re


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


type = "domain"
url = "https://otx.alienvault.com/api/v1/indicators/{type}/{item}/passive_dns"

parser = argparse.ArgumentParser()
parser.add_argument("item", type=str, help="domain, host or IPv4")
args = parser.parse_args()

pattern_ipv4 = "^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$"
if re.match(pattern_ipv4, args.item):
    type = "IPv4"

r = urllib.request.urlopen(url.format(type=type, item=args.item))
data = r.read().decode("utf-8")
json = json.loads(data)

print(
    "{header} HOSTNAME, RECORD_TYPE, ADDRESS, ASN, FIRST SEEN, LAST SEEN {end}".format(
        header=bcolors.HEADER, end=bcolors.ENDC
    )
)

for result in json["passive_dns"]:
    print(
        "{green} {hostname} {end} {underline} {record_type} {end} "
        "{green} {address} {end} {blue} {asn} {end} {fail} {first_seen} "
        "{end} {warning} {last_seen} {end}".format(
            green=bcolors.OKGREEN,
            hostname=result["hostname"],
            record_type=result["record_type"],
            address=result["address"],
            end=bcolors.ENDC,
            blue=bcolors.OKBLUE,
            asn=result["asn"],
            first_seen=result["first"],
            last_seen=result["last"],
            fail=bcolors.FAIL,
            warning=bcolors.WARNING,
            underline=bcolors.UNDERLINE,
        )
    )
