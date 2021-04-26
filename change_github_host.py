from lxml import etree
import requests
import os

host_file = ""


def search_host_file():
    global host_file
    for disk in ["C", "D", "E"]:
        if os.path.exists(disk + ":\Windows\System32\drivers\etc\hosts"):
            host_file = disk + ":\Windows\System32\drivers\etc\hosts"


def get_ip(domain):
    try:
        selector = etree.HTML(requests.get("https://" + domain + ".ipaddress.com/").text)
        find_ip_address = False
        for t in selector.xpath('//main//section[1]//tr//text()'):
            if "IP Address" in t:
                find_ip_address = True
                continue
            if find_ip_address:
                return t
    except:
        pass

    try:
        selector = etree.HTML(requests.get("https://fastly.net.ipaddress.com/" + domain).text)
        find_ip_address = False
        for t in selector.xpath('//main//section[1]//tr//text()'):
            if "IP Address" in t:
                find_ip_address = True
                continue
            if find_ip_address:
                return t
    except:
        pass

    raise Exception("no ip find")


def read_host():
    f = open(host_file, encoding="utf-8", mode="r")
    host_text = f.read()
    f.close()
    return host_text


def append_to_host(text):
    old_host = read_host()
    if text in old_host:
        print(text + " 无需更新")
    else:
        try:
            f = open(host_file, encoding="utf-8", mode="w")
            f.write(text + "\n" + old_host)
            f.close()
            print(text)
        except Exception as e:
            print("大兄弟,写入host失败了，是不是没有用管理员方式运行bat？？？")
            raise e
            pass


def add_host(domain):
    append_data = get_ip(domain) + " " + domain
    append_to_host(append_data)


if __name__ == '__main__':
    search_host_file()

    print("设置host开始")
    add_host("github.com")
    add_host("github.global.ssl.fastly.net")
    print("设置host结束")

    print("----new host file--------")
    print(read_host())
