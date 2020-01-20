#This is a TNFSH course table generator function of TNFSH absent query Bot
#gnsJhenJie 2020 Copyright
#臺南一中課表截圖

from urllib.parse import urlencode
from urllib.request import urlretrieve

start_class = input("請輸入起始班級:(請勿混年級)")
end_class = input("請輸入結束班級:(含)")
classes = list()
for i in range(int(start_class),int(end_class)+1):
    classes.append(str(i))
for class_number in classes:
    params = urlencode(dict(access_key="APIFLASH_ACCESS_KEY",
                        url="http://w3.tnfsh.tn.edu.tw/deanofstudies/course/C101" + class_number +".HTML",
                        format="jpeg",
                        full_page="true",
                        quality="100",
                        height="1000",
                        width="1200",
                        response_type="image"))
    urlretrieve("https://api.apiflash.com/v1/urltoimage?" + params, class_number + ".jpeg")