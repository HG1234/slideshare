from bs4 import BeautifulSoup
import requests
import img2pdf






def soup_maker(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'lxml')
    print("Made Soup",end='\r',flush=True)
    return soup
def total_slides_finder(url):
    soup = soup_maker(url)
    label = soup.find('label',class_='goToSlideLabel')
    total_slides = label.find('span',id='total-slides').text
    print(f'Total slides are {total_slides}')
    return total_slides

def image_link_maker(url):
    soup = soup_maker(url)
    image_seed = soup.find('img',class_='slide_image')['src']
    total_slides= total_slides_finder(url)
    all_img = []
    for i in range(1,int(total_slides)+1):

        splitter = image_seed.split('-')
        splitter[-2] = str(i)
        all_img.append('-'.join(splitter))
    print('Found all image links')
    return all_img


def image_downloader(url):
    k = 1
    imglist = []
    for url in image_link_maker(url):
        print(f'Downloading slide number {k}', end="\r", flush=True)
        with open(f'pic{k}.jpg', 'wb') as handle:
            imglist.append(f'pic{k}.jpg')
            response = requests.get(url, stream=True)
            k = k+1
            handle.write(response.content)

    return imglist

def convertor(imglist):
    with open("output.pdf", "wb") as f:
        f.write(img2pdf.convert([open(i,'rb' ) for i in imglist]))
    print('Done')
