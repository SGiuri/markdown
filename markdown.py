import re


def parse(markdown):
    lines = []

    for line in markdown.split("\n"):
        # search for bolds
        line = parse_bold(line)
        # search for italics
        line = parse_italics(line)
        # searching for headers
        line = parse_headers(line)
        # searching for unordered list
        line = parse_ul(line)

        lines.append(line)

    return "".join(lines)


def parse_italics(line):
    pattern = r"_(.*)_"
    return re.sub(pattern, r"<em>\g<1></em>", line)


def parse_bold(line):
    pattern = r"__(.*)__"
    return re.sub(pattern, r"<strong>\g<1></strong>", line)


def parse_headers(line):
    pattern = r"^#+"
    headers = re.findall(pattern, line)
    line = line.strip("# ")

    if headers:
        header_level = len(headers[0])
        header_open_tag = f"<h{header_level}>"
        header_closing_tag = f"</h{header_level}>"
        line = header_open_tag + line + header_closing_tag

    return line

def parse_ul(line):
    pattern = r"^\* (.*)"

    return re.sub(pattern, r"<li>\g<1></li>", line)


def old_parse(markdown):
    lines = markdown.split('\n')
    res = ''
    in_list = False
    in_list_append = False

    for i in lines:
        if re.match('###### (.*)', i) is not None:
            i = '<h6>' + i[7:] + '</h6>'
        elif re.match('## (.*)', i) is not None:
            i = '<h2>' + i[3:] + '</h2>'
        elif re.match('# (.*)', i) is not None:
            i = '<h1>' + i[2:] + '</h1>'
        m = re.match(r'\* (.*)', i)
        if m:
            if not in_list:
                in_list = True
                is_bold = False
                is_italic = False
                curr = m.group(1)
                m1 = re.match('(.*)__(.*)__(.*)', curr)
                if m1:
                    curr = m1.group(1) + '<strong>' + \
                           m1.group(2) + '</strong>' + m1.group(3)
                    is_bold = True
                m1 = re.match('(.*)_(.*)_(.*)', curr)
                if m1:
                    curr = m1.group(1) + '<em>' + m1.group(2) + \
                           '</em>' + m1.group(3)
                    is_italic = True
                i = '<ul><li>' + curr + '</li>'
            else:
                is_bold = False
                is_italic = False
                curr = m.group(1)
                m1 = re.match('(.*)__(.*)__(.*)', curr)
                if m1:
                    is_bold = True
                m1 = re.match('(.*)_(.*)_(.*)', curr)
                if m1:
                    is_italic = True
                if is_bold:
                    curr = m1.group(1) + '<strong>' + \
                           m1.group(2) + '</strong>' + m1.group(3)
                if is_italic:
                    curr = m1.group(1) + '<em>' + m1.group(2) + \
                           '</em>' + m1.group(3)
                i = '<li>' + curr + '</li>'
        else:
            if in_list:
                in_list_append = True
                in_list = False

        m = re.match('<h|<ul|<p|<li', i)
        if not m:
            i = '<p>' + i + '</p>'
        m = re.match('(.*)__(.*)__(.*)', i)
        if m:
            i = m.group(1) + '<strong>' + m.group(2) + '</strong>' + m.group(3)
        m = re.match('(.*)_(.*)_(.*)', i)
        if m:
            i = m.group(1) + '<em>' + m.group(2) + '</em>' + m.group(3)
        if in_list_append:
            i = '</ul>' + i
            in_list_append = False
        res += i
    if in_list:
        res += '</ul>'
    return res
#
# print("original")
# print(old_parse("# Start _a_ list\n* Item 1\n* Item 2\nEnd a list"))
# print("modified")
# print(parse("# Start _a_ list\n* Item 1\n* Item 2\nEnd a list"))
