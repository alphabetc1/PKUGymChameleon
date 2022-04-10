from matplotlib import pyplot as plt
import cv2
import random

def get_track(distance):
    '''
    拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
    匀变速运动基本公式：
    ①v=v0+at
    ②s=v0t+(1/2)at²
    ③v²-v0²=2as

    :param distance: 需要移动的距离
    :return: 存放每0.2秒移动的距离
    '''
    # 初速度
    v=0
    # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
    t=0.5
    # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
    tracks=[]
    # 当前的位移
    current=0
    # 到达mid值开始减速
    mid=distance * 5/8

    distance += 10  # 先滑过一点，最后再反着滑动回来
    
    while current < distance:
        if current < mid:
            # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
            a = random.randint(5,10)  # 加速运动
        else:
            a = -random.randint(5,10) # 减速运动

        # 初速度
        v0 = v
        # 0.2秒时间内的位移
        s = v0*t+0.5*a*(t**2)
        # 当前的位置
        current += s
        # 添加到轨迹列表
        tracks.append(round(s))

        # 速度已经达到v,该速度作为下次的初速度
        v= v0+a*t

    # 反着滑动到大概准确位置
    tracks.append(distance - current - 5)
    # for i in range(4):
    #    tracks.append(-random.randint(1,3))
    return tracks


def img_compute_edge():
    left_path = './pics/left.png'
    right_path = './pics/right.png'
    left_img = cv2.imread(left_path)
    right_img = cv2.imread(right_path)
    left_gray = cv2.cvtColor(left_img, cv2.COLOR_BGR2RGB) # Converting BGR to RGB
    right_gray = cv2.cvtColor(right_img, cv2.COLOR_BGR2RGB) # Converting BGR to RGB
    left_canny = cv2.Canny(left_gray, 300, 300)
    right_canny = cv2.Canny(right_gray, 300, 300)
    left_contours, _ = cv2.findContours(left_canny, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    dx, dy, dw, dh = 0, 0, 0, 0
    for i, contour in enumerate(left_contours):
        x, y, w, h = cv2.boundingRect(contour)
        if (w > dw) or (h > dh):
            dx, dy, dw, dh = x, y, w, h
    cv2.rectangle(left_img, (dx, dy), (dx + dw, dy + dh), (0, 0, 255), 2)
    print(dx, dy, dw, dh)
    plt.imshow(left_img)
    plt.savefig('mygraph1_edge.png')
    right_contours, _ = cv2.findContours(right_canny, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    
    delta = 9999
    ndx, ndy, ndw, ndh = 0, 0, 0, 0
    for i, contour in enumerate(right_contours):
        x, y, w, h = cv2.boundingRect(contour)
        # ndelta = abs(y - dy + w - dw + h - dh)
        ndelta = abs(y - dy) + abs(w - dw) + abs(h - dh)
        
        if ndelta < delta:
            # print(x, y, w, h)
            ndx, ndy, ndw, ndh = x, y, w, h
            delta = ndelta
    print(ndx, ndy, ndw, ndh)
    cv2.rectangle(right_img, (ndx, ndy), (ndx + ndw, ndy + ndh), (0, 0, 255), 2)
    plt.imshow(right_img)
    plt.savefig('mygraph2_edge.png')

    return ndx


def img_compute_bg():
    left_path = './pics/right.png'
    left_img = cv2.imread(left_path)
    left_gray = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY) # Converting BGR to RGB
    ret, left_gray = cv2.threshold(left_gray, 127, 255, cv2.THRESH_BINARY)
    left_contours, left_hierarchy = cv2.findContours(left_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(left_img, left_contours, -1, (0, 0, 255), 3)
    dx, dy, dw, dh = 0, 0, 0, 0
    for i, contour in enumerate(left_contours):
        x, y, w, h = cv2.boundingRect(contour)
        # print (x, y, w, h)
        if (w > dw) and (h > dh):
            dx, dy, dw, dh = x, y, w, h
    # print(dx, dy, dw, dh)
    # cv2.rectangle(left_img, (x, y), (x + dw, y + dh), (0, 0, 255), 2)
    # plt.imshow(left_img)
    # plt.savefig('mygraph2.png')

if __name__ == '__main__':
    img_compute_edge()
    # img_compute_bg()