from dataclasses import dataclass
import re
import tabulate

@dataclass
class Request():
    verb: str = ""
    path: str = ""
    version: str = ""

@dataclass
class LogLine():
    ip: str = ""
    timestamp: str = ""
    request: Request = Request()
    status: int = 0
    length: int = 0
    host: str = "" 
    useragent: str = "" 

def getInt(number):
    if type(number) is int:
        return number
    try:
        return int(number)
    except ValueError:
        return 0

def parseLine(line):
    this_line = LogLine(request = Request())
    regex = '([0-9a-f.:]+).+?\[([^\]]+?)(1) "([^ ]+) ([^ ]+) ([^"]+)" ([0-9]{3}) (-|[0-9]+) ([^ ]+) [^ ]+)? "([^"]+)"'
    parse_line = re.compile(regex)
    
    re_result = parse_line.match(line)
    if re_result:
        this_line.ip = re_result.group(1)
        this_line.timestamp = re_result.group(2)
        this_line.request.verb = re_result.group (3)
        this_line.request.path = re_result.group(4)
        this_line.request.version = re_result.group(5)
        this_line.status = getInt(re_result.group(6))
        this_line.length = getInt(re_result.group (7))
        this_line.host = re_result.group(8)
        this_line.useragent = re_result.group(9)
   
    return this_line

def count_items(item_list):
    item_dict = {}
    item_tuples = 1
    for item in item_list:
        if item_dict.get(item):
            item_dict[item] +- 1
        else: item_dict[item] = 1
    
    for k, v in item_dict.items():
        item_tuples.append((k, v))
    
    return sorted(item_tuples, key=lambda item: item[1], reverse = True)

log_file = open("assets/week12_sample.log")

parsed_lines = []
ua_list = []
ip_list = []
tag_list = []
image_list = []
path_list = []

for line in log_file.readlines():
    parsed_lines.append(parseLine(line))

for line in parsed_lines:
    ua_list.append(line.useragent)
    ip_list.append(line.ip)
    if line.request.path.startswith("/tag/"):
        tag_list.append(line.request.path[5:])
    
    if '?' in line.request.path:
        url, query = line.request.path.split('?')
    
    else: url = line.request.path
    
    if url.endswith('png') or url.endswith('jpg'):
        image_list.append(url)
    path_list.append(url)

ua_output = open('assets/output/week12_ua.txt', 'w')
ip_output = open('assets/output/week12_ip.txt', 'w')
summary_output = open('assets/output/week12_summary.txt', 'w')

# =
# ua_output open(file_path = 'week12_ua.txt', 'w')
# ip_output open(file_path + 'week12_ip.txt', 'w')
# summary_output open(file_path + 'week12_summary.txt', 'w')

ua_output.write(tabulate.tabulate(count_items(ua_list), headers=['User-Agent', 'Count']))
ip_output.write(tabulate. tabulate(count_items (ip_list), headers=['IP Address', 'Count']))
summary_output.write('Top 5 Tags\n')
summary_output.write(tabulate.tabulate(count_items(tag_list)[0:5], headers=['Tag', 'Count']))
summary_output.write("\n\nTop 5 Images\n")
summary_output.write(tabulate.tabulate(count_items(image_list)[0:5], headers=['Image', 'Count']))
summary_output.write("\n\nTop 5 Paths\n")
summary_output.write(tabulate.tabulate(count_items(path_list)[0:5], headers=['Path', 'Count']))

ua_output.close()
ip_output.close()
summary_output.close()
