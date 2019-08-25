'''
余票查询
'''
from configure import QUERY_TICKET_REFERSH_INTERVAL
from net.NetUtils import eHttp
from conf.city_code import city2code, code2city
from conf.urls_conf import queryUrls
from utils.Log import Log
from utils.Utils import do_fix_time
from utils import TrainUtils
from conf.constant import PASSENGER_TYPE_ADULT, SEAT_TYPE, POLICY_BILL_ALL
from train.TicketDetails import TicketDetails

import collections
from datetime import datetime
import time

'''
车次：3
start_station_code:起始站：4
end_station_code终点站：5
from_station_code:出发站：6
to_station_code:到达站：7
start_time:出发时间：8
arrive_time:达到时间：9
历时：10
商务特等座：32
一等座：31
二等座：30
高级软卧：21
软卧：23
动卧：33
硬卧：28
软座：24
硬座：29
无座：26
其他：22
备注：1
start_train_date:车票出发日期：13
secretStr：0
'''

class Query(object):

    @staticmethod
    def __decode(queryResults, passengerType):
        for queryResult in queryResults:
            info = queryResult.split('|')
            ticket = TicketDetails()
            ticket.passengerType = passengerType
            ticket.trainNo = info[3]
            ticket.startStationCode = info[4]
            ticket.endStationCode = info[5]
            ticket.fromStationCode = info[6]
            ticket.toStationCode = info[7]
            ticket.leaveTime = info[8]
            ticket.arriveTime = info[9]
            ticket.totalConsume = info[10]
            ticket.businessSeat = info[32]
            ticket.firstClassSeat = info[31]
            ticket.secondClassSeat = info[30]
            ticket.advancedSoftSleep = info[21]
            ticket.softSleep = info[23]
            ticket.moveSleep = info[33]
            ticket.hardSleep = info[28]
            ticket.softSeat = info[24]
            ticket.hardSeat = info[29]
            ticket.noSeat = info[28]
            ticket.other = info[22]
            ticket.mark = info[1]
            ticket.startStation = code2city(ticket.startStationCode)
            ticket.endStation = code2city(ticket.endStationCode)
            ticket.fromStation = code2city(ticket.fromStationCode)
            ticket.toStation = code2city(ticket.toStationCode)
            ticket.secretStr = info[0]
            ticket.startDate = info[13]
            yield ticket

    @staticmethod
    def query(flag, base_url, trainDate, fromStation, toStation, passengerType=PASSENGER_TYPE_ADULT):
        params = collections.OrderedDict()
        params['leftTicketDTO.train_date'] = trainDate
        params['leftTicketDTO.from_station'] = city2code(fromStation)
        params['leftTicketDTO.to_station'] = city2code(toStation)
        params['purpose_codes'] = passengerType
        jsonRet = eHttp.send(queryUrls['query'], params=params)    
        try:
            if jsonRet:
                return Query.__decode(jsonRet['data']['result'], passengerType)
        except Exception as e:
            Log.e(e)
        return []

    @staticmethod
    def querySpec(flag, base_url, trainDate, fromStation, toStation, passengerType=PASSENGER_TYPE_ADULT, trainsNo=[],
                  seatTypes=[SEAT_TYPE[key] for key in SEAT_TYPE], PASSENGERS_ID=[], POLICY_BILL=1):
        for ticket in Query.query(flag, base_url, trainDate, fromStation, toStation, passengerType):
            if not TrainUtils.filterTrain(ticket, trainsNo):
                continue
            for seatTypeName, seatTypeProperty in TrainUtils.seatWhich(seatTypes, ticket):
                if seatTypeProperty and seatTypeProperty != '无':
                    Log.v('%s %s: %s' % (ticket.trainNo, seatTypeName, seatTypeProperty))
                    try:
                        remind_num = int(seatTypeProperty)
                    except Exception as e:
                        remind_num = 100
                    if POLICY_BILL == POLICY_BILL_ALL and len(PASSENGERS_ID) > remind_num:
                        break
                    ticket.seatType = SEAT_TYPE[seatTypeName]
                    ticket.remindNum = remind_num
                    yield ticket
        return []

    @staticmethod
    def loopQuery(trainDate, fromStation, toStation, passengerType=PASSENGER_TYPE_ADULT, trainsNo=[],
                  seatTypes=[SEAT_TYPE[key] for key in SEAT_TYPE], PASSENGERS_ID=[], POLICY_BILL=1,
                  timeInterval=QUERY_TICKET_REFERSH_INTERVAL):
        count = 0
        base_query_url = queryUrls['query']['url']
        while True:
            nowTime, status = do_fix_time()
            if status:
                Log.v('当前时间:%s 处于23点到6点之间，12306处于维护状态，暂不处理下单业务' % nowTime)
                continue

            count += 1
            Log.v('正在为您第%d次刷票' % count + '，当前时间为:%s' % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            for ticketDetails in Query.querySpec(count, base_query_url, trainDate, fromStation, toStation,
                                                 passengerType, trainsNo, seatTypes,
                                                 PASSENGERS_ID, POLICY_BILL):
                if ticketDetails:
                    return ticketDetails
            time.sleep(timeInterval)