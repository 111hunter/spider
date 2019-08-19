"""
下单
"""
from conf.constant import TourFlag
from conf.urls_conf import submitUrls
from net.NetUtils import eHttp
from train.PassengerDetails import PassengerDetails
from utils import TrainUtils
from utils.Utils import formatDate, check 
from utils.Log import Log

import json, re, time, requests, copy
from datetime import datetime
from colorama import Fore

class Submit(object):
    def __init__(self, ticketDetails):
        self.__ticket = ticketDetails
        self._urlInfo = submitUrls['dc']

    def __getPassengerInfo(self, passengersList):
        passengersDetails = {}
        for passengerJson in passengersList:
            passenger = PassengerDetails()
            passenger.passengerName = passengerJson.get('passenger_name') or ''
            passenger.code = passengerJson.get('code') or ''
            passenger.sexCode = passengerJson.get('sex_code') or ''
            passenger.sexName = passengerJson.get('sex_name') or ''
            passenger.bornDate = passengerJson.get('born_date') or ''
            passenger.countryCode = passengerJson.get('country_code') or ''
            passenger.passengerIdTypeCode = passengerJson.get('passenger_id_type_code') or ''
            passenger.passengerIdTypeName = passengerJson.get('passenger_id_type_name') or ''
            passenger.passengerIdNo = passengerJson.get('passenger_id_no') or ''
            passenger.passengerType = passengerJson.get('passenger_type') or ''
            passenger.passengerFlag = passengerJson.get('passenger_flag') or ''
            passenger.passengerTypeName = passengerJson.get('passenger_type_name') or ''
            passenger.mobileNo = passengerJson.get('mobile_no') or ''
            passenger.phoneNo = passengerJson.get('phone_no') or ''
            passenger.email = passengerJson.get('email') or ''
            passenger.address = passengerJson.get('address') or ''
            passenger.postalcode = passengerJson.get('postalcode') or ''
            passenger.firstLetter = passengerJson.get('first_letter') or ''
            passenger.recordCount = passengerJson.get('recordCount') or ''
            passenger.totalTimes = passengerJson.get('total_times') or ''
            passenger.indexId = passengerJson.get('index_id') or ''
            passenger.allEncStr = passengerJson.get('allEncStr') or ''
            #12306版本更新隐藏了证件号,直接取最后三位
            passengersDetails[passenger.passengerIdNo[-3:]] = passenger
        return passengersDetails

    # 1 checkUser++++++++++++++++++++++++++++++++++++++++++++++
    def _check_user(self,tourFlag = 'dc'):
        formData = {
            '_json_att': ''
        }
        check_user = copy.deepcopy(self._urlInfo['checkUser'])
        check_user['headers']['Referer'] = self._urlInfo['checkUser']['headers']['Referer']+ '?linktypeid='+tourFlag
        jsonRet = eHttp.post_custom(check_user,data = formData)
        return True,jsonRet.text    

    # 2 submitOrderRequest+++++++++++++++++++++++++++++++++++++
    def _submitOrderRequest(self, tourFlag='dc'):
        formData = {
            'secretStr': TrainUtils.undecodeSecretStr(self.__ticket.secretStr),
            'train_date': formatDate(self.__ticket.startDate),  # 2018-10-05
            'back_train_date': time.strftime("%Y-%m-%d", time.localtime()),  # query date:2017-12-31
            'tour_flag': tourFlag,
            'purpose_codes': self.__ticket.passengerType,
            'query_from_station_name': self.__ticket.fromStation,
            'query_to_station_name': self.__ticket.toStation,
            'undefined': '',
        }
        order_request = copy.deepcopy(self._urlInfo['submitOrderRequest'])
        order_request['headers']['Referer'] = self._urlInfo['submitOrderRequest']['headers']['Referer']+ '?linktypeid='+tourFlag
        response = eHttp.post_custom(order_request, data=formData)
        if response and response.status_code == 302:
            self._urlInfo['submitOrderRequest']['url'] = response.headers['Location']
            response = eHttp.post_custom(self._urlInfo['submitOrderRequest'], data=formData)
        if response and response.status_code == requests.codes.ok:
            return True,'ok'
        return False,'failed'

    # 3 initDC+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def _getExtraInfo(self):
        def getRepeatSubmitToken(html):
            repeatSubmitToken = re.findall(r"var globalRepeatSubmitToken = '(.*)'", html)[0]
            return repeatSubmitToken
        formData = {
            '_json_att': ''
        }
        extra_info = copy.deepcopy(self._urlInfo['getExtraInfo'])
        extra_info['headers']['Referer'] = self._urlInfo['getExtraInfo']['headers']['Referer']+ '?linktypeid='+self.__ticket.tourFlag
        response = eHttp.post_custom(extra_info,data=formData)
        if response and response.status_code == requests.codes.ok:
            html = response.text
        else:
            html = None
        if not check(html, 'getExtraInfoUrl: failed to visit %s' % self._urlInfo['getExtraInfo']['url']):
            return False
        self.__ticket.repeatSubmitToken = getRepeatSubmitToken(html)
        def decodeTicketInfoForPassengerForm(html):
            ticketInfoForPassengerForm = re.findall(r'var ticketInfoForPassengerForm=(.*);', html)[0]
            return json.loads(ticketInfoForPassengerForm.replace("'", "\""))
        self.__ticket.ticketInfoForPassengerForm = decodeTicketInfoForPassengerForm(html)
        return True
    
    # 4 getPassengerDTOs++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def _getPassengerDTOs(self):
        if not self._getExtraInfo():
            return False, '获取乘客信息失败', None
        formData = {
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.__ticket.repeatSubmitToken,
        }
        jsonRet = eHttp.send(self._urlInfo['getPassengerDTOs'], data=formData)
        passengersList = jsonRet['data']['normal_passengers']
        return jsonRet['status'] if 'status' in jsonRet else False, \
               jsonRet['messages'] if jsonRet and 'messages' in jsonRet else '无法获取乘客信息，请先进行添加!', \
               self.__getPassengerInfo(passengersList)

    # 5 checkOrderInfo++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def _checkOrderInfo(self, passengersDetails, seatType, ticketTypeCodes=1):
        formData = {
            'cancel_flag': self.__ticket.ticketInfoForPassengerForm['orderRequestDTO']['cancel_flag'] or '2',
            'bed_level_order_num': self.__ticket.ticketInfoForPassengerForm['orderRequestDTO'][
                                       'bed_level_order_num'] or '000000000000000000000000000000',
            'passengerTicketStr': TrainUtils.passengerTicketStrs(seatType, passengersDetails, ticketTypeCodes),
            'oldPassengerStr': TrainUtils.oldPassengerStrs(passengersDetails),
            'tour_flag': self.__ticket.ticketInfoForPassengerForm['tour_flag'] or 'dc',
            'randCode': '',
            'whatsSelect': '1',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.__ticket.repeatSubmitToken,
        }
        jsonRet = eHttp.send(self._urlInfo['checkOrderInfo'], data=formData)
        submitStatus = ''
        errMsg = ''
        if jsonRet['data']:
            submitStatus = jsonRet['data']['submitStatus']
            errMsg = jsonRet['data']['errMsg'] if 'errMsg' in jsonRet['data'] else 'submit falied'
        return jsonRet['status'], jsonRet['messages'], submitStatus, errMsg

    # 6 getQueueCount+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def _getQueueCount(self):
        formData = {
            'train_date': datetime.strptime(
                self.__ticket.ticketInfoForPassengerForm['queryLeftTicketRequestDTO']['train_date'], '%Y%m%d').strftime(
                '%b %a %d %Y 00:00:00 GMT+0800') + ' (中国标准时间)',
            'train_no': self.__ticket.ticketInfoForPassengerForm['queryLeftTicketRequestDTO']['train_no'],
            'stationTrainCode': self.__ticket.trainNo,
            'seatType': self.__ticket.seatType,
            'fromStationTelecode': self.__ticket.fromStationCode,
            'toStationTelecode': self.__ticket.toStationCode,
            'leftTicket': self.__ticket.ticketInfoForPassengerForm['leftTicketStr'],
            'purpose_codes': self.__ticket.ticketInfoForPassengerForm['purpose_codes'],
            'train_location': self.__ticket.ticketInfoForPassengerForm['train_location'],
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.__ticket.repeatSubmitToken,
        }
        jsonRet = eHttp.send(self._urlInfo['getQueueCount'], data=formData)
        return jsonRet['status'], jsonRet['messages'], \
               jsonRet['data']['ticket'] if 'data' in jsonRet and 'ticket' in jsonRet['data'] else -1, \
               jsonRet['data']['count'] if 'data' in jsonRet and 'count' in jsonRet['data'] else -1

    # 7 confirmSingleForQueue++++++++++++++++++++++++++++++++++++++++++++++++++
    def _confirmSingleOrGoForQueue(self, passengersDetails,choose_seat):
        formData = {
            'passengerTicketStr': TrainUtils.passengerTicketStrs(self.__ticket.seatType, passengersDetails, self.__ticket.ticketTypeCodes),
            'oldPassengerStr': TrainUtils.oldPassengerStrs(passengersDetails),
            'randCode': '',
            'purpose_codes': self.__ticket.ticketInfoForPassengerForm['purpose_codes'],
            'key_check_isChange': self.__ticket.ticketInfoForPassengerForm['key_check_isChange'],
            'leftTicketStr': self.__ticket.ticketInfoForPassengerForm['leftTicketStr'],
            'train_location': self.__ticket.ticketInfoForPassengerForm['train_location'],
            'choose_seats': ''.join(choose_seat) or '',
            'seatDetailType': '000',  # todo::make clear 000 comes from
            'whatsSelect': '1',
            'roomType': '00',  # todo::make clear this value comes from
            'dwAll': 'N',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.__ticket.repeatSubmitToken,
        }
        jsonRet = eHttp.send(self._urlInfo['confirmForQueue'], data=formData)
        return jsonRet['status'], jsonRet['messages'], jsonRet['data']['submitStatus'], jsonRet['data'][
            'errMsg'] if 'errMsg' in jsonRet['data'] else None
    

    # seatType:商务座(9),特等座(P),一等座(M),二等座(O),高级软卧(6),软卧(4),硬卧(3),软座(2),硬座(1),无座(1)
    # ticket_type_codes:成人票:1,儿童票:2,学生票:3,残军票:4
    def submit(self,choose_seat):
        self._check_user(self.__ticket.tourFlag)
        status, msg = self._submitOrderRequest(self.__ticket.tourFlag)
        if not check(status, 'submitOrderRequesst: %s' % msg):
            return False
        Log.v('提交订单请求成功!')
        status, msg, passengersDetailsList = self._getPassengerDTOs()
        if not check(status, 'getPassengerDTOs: %s' % msg):
            return False
        Log.v('获取乘客信息成功!')
        passengersDetails = []
        if len(self.__ticket.passengersId) >= self.__ticket.remindNum:
            for i in range(self.__ticket.remindNum):
                id = self.__ticket.passengersId[i]
                ticket_details = passengersDetailsList.get(id[-3:])
                ticket_details.passengerIdNo = id
                passengersDetails.append(ticket_details)
        else:
            for id in self.__ticket.passengersId:
                ticket_details = passengersDetailsList.get(id[-3:])
                ticket_details.passengerIdNo = id
                passengersDetails.append(ticket_details)
        time.sleep(0.2)
        status, msg0, submitStatus, errMsg = self._checkOrderInfo(passengersDetails, self.__ticket.seatType, self.__ticket.ticketTypeCodes)
        if not check(status, 'checkOrderInfo: %s' % msg0) or not check(submitStatus, 'checkOrderInfo: %s' % errMsg):
            return False
        Log.v('校验订单信息成功!')
        status, msg1, leftTickets, personsCount = self._getQueueCount()
        if not check(status, 'getQueueCount: %s' % msg1):
            return False
        Log.v('%s 剩余车票:%s ,目前排队人数: %s' % (self.__ticket.trainNo, leftTickets, personsCount))
        status, msg2, submitStatus, errMsg = self._confirmSingleOrGoForQueue(passengersDetails,choose_seat)
        if not check(status, 'confirmSingleOrGoForQueue: %s' % msg2) \
                or not check(submitStatus, 'confirmSingleOrGoForQueue: %s' % errMsg or '订单信息提交失败！'):
            return False
        return True