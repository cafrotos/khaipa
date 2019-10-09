
import sys
import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict
import pandas as pd
import daemon

USERNAME = '0936149274'
PASSWORD = 'dominhkha1999'

cate_dict = {
    "music": [" hát", "hat", "bolero", "nhạc", "cải lương", "song ca","thơ"],
    "sport and travel": ["bóng chuyền", "volleyball", "thể thao", "bóng đá", "du lịch", "travel", "MU", "chelsea", "ronaldo","gải trí","trip"],
    "comic and film": ["conan", "doreamon", "truyện", "batman", "superman", "phim", "ant man", "spider man", "truyen", "siêu nhân","du ký"],
    "health and family": ["sức khỏe", "chăm sóc", "dưỡng", "cận thị", "lão", "gia đình","tổ quốc", "quê hương","phật","chúa","khổ nạn","a di","đạo","tín ngưỡng","bồ tát","nam mô","miền tây","tâm linh","con cháu","thuốc","ung thư","quê","bố","mẹ","ông","bà","cụ","chùa","làm đẹp","phẫu thuật"],
    "jobs": ["lương", "fresher", "việc", "viec", " tuyen", "tuyển", "lao động", "lao dong", "thiết kế", "thực tập","freelancer","nghề","dọn nhà"],
    "social learning": ["toán", "sử","gia sư" ,"địa", "tuyển sinh", "ôn thi", "học", "learning","tiếng anh" ],
    "love": ["tình cảm", "trái tim", "hạnh phúc", "hanh phuc", "girl", "hot boy", "sexy","oppa","buồn vui","thẩm mỹ","eva","hẹn hò","love","thư giãn","yêu","gái đẹp","trai đẹp","gay ","nỗi buồn"],
    "suport": ["thiện nguyện", "tình nguyện", "tình thương", "hỗ trợ"],
    "new": ["tin tức", "new", "vietnamnet", "vnexpress", "tạp chí", "báo", "thời tiết","thông tin","tin mới","cười","fun","giải trí"],
    "gaming": ["lol", "moba", "survival", "mine", "liên minh", "liên quân", "pubg", "dota", "game", "kiếm vương","pewpew","mixi","mộng tam quốc","casino","fifa"],
    "buy and sell": ["hàng", "chợ", "mua", "bán", "shop", "thời trang", "rao vặt", "dịch vụ", "thanh lý","nhà đất","giao dịch","kinh doanh",'cũ','đại lý',"siêu thị",'sieuthi','rẻ','đấu giá','free'],
    "club": ["chia sẻ","clb", "cộng đồng", "hội", "friends", "nhóm", "teen", "fc", "bạn bè","group","tình bạn","việt nam","hà nội","vetnam","club","nhậu","bạn hữu","kết nối","confession"],
    "school and class": ["lớp", "lop", "khoá", "fc", "trường","THPT","thpt","12b1","10b1","trung học","sinh viên","học sinh"]
}

base_url="https://www.facebook.com/groups/"

dict__ = {'__label__18-24': {'sport and travel': 0, 'buy and sell': 0, 'health and family': 0, 'jobs': 0, 'love': 0,
                            'social learning': 0, 'suport': 0, 'new': 0, 'comic and film': 0, 'music': 0, 'gaming': 0, 'school and class': 0,"club":0,"general":0}}

first_line=int(sys.argv[1])
last_line=int(sys.argv[2])
def login(session, email, password):

   
    response = session.post('https://m.facebook.com/login.php', data={
        'email': email,
        'pass': password
    }, allow_redirects=False)
    return session.cookies;

def getContents(fileName):
    f=open(fileName,'r')
    return f.readlines()


def checkInside(category, name):
    return any(x in name for x in category)

def getDict(session,line,cookies,index):
    line = line.split(" ")
    dict_ = defaultdict(dict)
    label = line[0]
    print(label)
    for i in cate_dict.keys():
        dict_[label][i] = 0
    dict_[label]["general"] = 0
    
    for i in line[1:]:
        url=base_url+i
        response = session.get(url, cookies=cookies, 
            allow_redirects=False)
        soup=BeautifulSoup(response.content,'html.parser')
        if soup.find("h1",id="seo_h1_tag") != None:
            name=soup.find("h1",id="seo_h1_tag").find('a').text.strip().lower()
            flag=False
            for j in cate_dict.keys():
                if(checkInside(cate_dict[j],name)):
                    dict_[label][j] += 1
                    flag=True
                    print(str(index)+" - "+name+" -> "+j)
                    break
            if flag==False:
                dict_[label]["general"] += 1
                print(name+" - general")
    return dict_

def crawl():
    try:
        contents=getContents("train.txt")
        session = requests.session()
        cookies = login(session, USERNAME, PASSWORD)
        df = pd.DataFrame.from_dict(dict__, orient='index')
        name="data_";
        for index,line in enumerate(contents[first_line:last_line]):
            index=index+first_line
            df1 = pd.DataFrame.from_dict(getDict(session,line,cookies,index), orient='index')
            df = pd.concat([df, df1],sort=False)
        name="data_"+str(first_line)+"_"+str(last_line)+".csv"
        df.to_csv(name,encoding='utf-8-sig')
    except:
        name="data_"+str(first_line)+"_"+str(index)+"error.csv"
        df.to_csv(name,encoding='utf-8-sig')

if __name__ == "__main__":
    with daemon.DaemonContext():
        crawl()