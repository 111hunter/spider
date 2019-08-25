from configure import *
from net.NetUtils import eHttp
from utils.Log import Log
from conf.urls_conf import loginUrls
from utils.Utils import do_fix_time, check
from train.login import Login
from train.Query import Query
from train.Submit import Submit
from utils.TrainUtils import passengerType2Desc
from conf.constant import SEAT_TYPE, SeatName, NUM_SEAT, LETTER_SEAT

import copy, random, time

def do_login(): 
    login = Login()
    Log.v('正在登录...')
    result,msg = login.login(USER_NAME,USER_PWD)
    eHttp.save_cookies(COOKIE_SAVE_ADDRESS)
    if not check(result, msg):
        Log.e(msg)
        return False,login
    Log.v('%s,登录成功' % msg)
    return True,login

def main():
    eHttp.load_cookies(COOKIE_SAVE_ADDRESS)
    cookies = {c.name: c.value for c in eHttp.get_session().cookies}
    if not ('uamtk' in cookies and 'RAIL_DEVICEID' in cookies):
            status,login = do_login()
            if not status:
                return
    else:
        response = eHttp.post_custom(loginUrls['normal']['conf'])
        if not response or not response.json():
            Log.d('登录状态检查失败,重新请求')
            status, login = do_login()
            if not status:
                return
        resp = response.json()
        login_status = resp.get('data').get('is_login')
        login_name = resp.get('data').get('name')
        Log.d('登录状态：%s'%login_status)
        if 'Y' != login_status:
            Log.d('登录状态已过期,重新请求')
            status, login = do_login()
            if not status:
                return
        login = Login()
        login._urlInfo = loginUrls['normal']
        if login_name is not None:
            Log.v(login_name + ': 已登录状态,开始寻找车票')

    count = 0
    while True:
        # 死循环查票直到下单成功
        try:
            nowTime, status = do_fix_time()
            if status:
                Log.v('当前时间:%s 处于23点到6点之间，12306处于维护状态，暂不处理下单业务' % nowTime)
                continue
            count += 1
            Log.v('\n第%d次访问12306网站' % count)
            print('-' * 40)
            ticketDetails = Query.loopQuery(TRAIN_DATE, FROM_STATION, TO_STATION,
                                            passengerType2Desc(PASSENGER_TYPE_CODE),
                                            TRAINS_NO, SEAT_TYPE_CODE, PASSENGERS_ID, 
                                            POLICY_BILL, QUERY_TICKET_REFERSH_INTERVAL)
            Log.v('已为您查询到可用余票:%s' % ticketDetails)
            ticketDetails.passengersId = PASSENGERS_ID
            ticketDetails.ticketTypeCodes = PASSENGER_TYPE_CODE
            ticketDetails.tourFlag = TOUR_FLAG
            submit = Submit(ticketDetails)
            seats_default = copy.deepcopy(CHOOSE_SEATS)
            if (ticketDetails.seatType == SEAT_TYPE[SeatName.FIRST_CLASS_SEAT] or ticketDetails.seatType == SEAT_TYPE[SeatName.SECOND_CLASS_SEAT]) and not seats_default:
                results_seat = []
                for i in range(len(PASSENGERS_ID)):
                    random_seat = random.choice(NUM_SEAT)+random.choice(LETTER_SEAT)
                    if random_seat in results_seat:
                        continue
                    results_seat.append(random_seat)
                seats_default.extend(results_seat)    
            if submit.submit(seats_default):
                Log.v("您已成功订购火车票！请在30分钟内前往12306官方网站进行支付")
                break
            else:
                Log.v("购票失败,重新请求")
                time.sleep(5)
        except Exception as e:
            Log.w(e)
            time.sleep(5)

if __name__ == '__main__':
    main()