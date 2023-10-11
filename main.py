import cv2 as cv
import pytesseract
import requests
import re


img_count = 0

img_save_count = 0

img_type = ".png"

def get_captcha():

    global img_save_count, img_type
    

    url = "https://ceoelection.maharashtra.gov.in/search/Captcha.aspx"
    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "ASP.NET_SessionId=5qahrxkwxuiomnrusttlx0fd",
    "Dnt": "1",
    "Host": "ceoelection.maharashtra.gov.in",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }

    # Send the GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the image to a file
        img_name = "out-img"+ str(img_save_count)+img_type
        with open(img_name, "wb") as file:
            file.write(response.content)
        print("Original Image saved as {}".format(img_name))
        img_save_count += 1
    else:
        print("Request failed with status code:", response.status_code)

'''
def image_to_text1(gray_img):
    # Read image as grayscale
    img = cv.imread(gray_img, cv.IMREAD_GRAYSCALE)

    # Threshold at nearly white cutoff
    thr = cv.threshold(img, 224, 255, cv.THRESH_BINARY)[1]

    # Floodfill "background" with black
    ff = cv.floodFill(thr, None, (0, 0), 0)[1]

    # OCR using pytesseract
    text = pytesseract.image_to_string(ff, config='--psm 6').replace('\n', '').replace('\f', '')
    return text
'''

def image_to_text1(gray_img):
    # OCR using pytesseract
    img = cv.imread(gray_img, cv.IMREAD_GRAYSCALE)
    text = pytesseract.image_to_string(img, config='--psm 6').replace('\n', '').replace('\f', '')
    return text

def convert_BW(img_name):
    global img_count, img_type
    im = cv.imread(img_name, cv.IMREAD_GRAYSCALE)
    #cv.imshow('GRAY SCALE', im)
    (thresh, img) = cv.threshold(im, 50, 255, cv.THRESH_BINARY)
    out1 = cv.bitwise_not(img)
    out2 = cv.bitwise_not(out1)
    #cv.imshow('Black white image', out1)
    #cv.imshow('B7W with Threshold', out2) rcaptcha0.png
    out_img = "rcaptcha"+str(img_count)+img_type
    img_count += 1
    cv.imwrite(out_img, out2)
    print("Black and White Image saved as {}".format(out_img))

def perform_action(a, operator, b):
    if operator=="+":
        result = a+b
    elif operator=="-":
        result = abs(a-b)
    elif operator=="*":
        result = a*b
    elif operator=="/":
        result = a/b
    return result

def solving_text(text):
    stext = text

    pattern = r'(\d+)\s*([-+*/])\s*(\d+)='

    match1 = re.search(pattern, stext)

    if match1:
        a, operator, b = map(match1.group, [1,2,3])
        a = int(a)
        b = int(b)
        result = perform_action(a, operator, b)
        print('{} {} {}={}'.format(a,operator,b, result))
        return result
    else:
        print("from solving text text not matched")
    


#main method binding all the above functions together
def process():
    global img_type
    
    #first we need a captcha to read, below line will generate a captcha
    get_captcha()

    captcha_name = "out-img"+str(img_save_count-1)+img_type

    #calling function convert_BW, to convert this captcha_img into white on black background
    convert_BW(captcha_name)

    bw_captcha = "rcaptcha"+str(img_count - 1)+img_type

    result1 = image_to_text1(bw_captcha)

    print("This is result from image_to_text2 - ", result1)
    
    output = solving_text(result1)
    print('answer', output)
process()
















