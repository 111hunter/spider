'''
购票必要信息
'''

#cookie存放地址
COOKIE_SAVE_ADDRESS = 'cookie.txt'

USER_NAME = ''
USER_PWD = ''

FROM_STATION = '上海'
TO_STATION = '重庆'

# 乘车日期（格式: YYYY-mm-dd）
TRAIN_DATE = '2019-09-12'

# 购票人身份证号
PASSENGERS_ID = ['']
# 票类型（单程:dc 往返:wc）
TOUR_FLAG = 'dc'

#订票策略,1表示必须全部一起预定，2表示可以部分提交
POLICY_BILL = 1

# 过滤车次,填入选择范围
TRAINS_NO = ['D352','D2206','D2212','D2216','G1974','D3056']

# 座位类别（商务座(9),特等座(P),一等座(M) ,二等座(O),高级软卧(6),软卧(4),硬卧(3),软座(2),硬座(1),无座(1)）
SEAT_TYPE_CODE = ['O']

# 购票人类别（成人票:1,儿童票:2,学生票:3,残军票:4）
PASSENGER_TYPE_CODE = '1'

# 座位选择 eg:['1A','2A'],有多少张票就填多少个,其中，A靠窗，B中间，C过道,D过道,F靠窗
#解释：如果你有三个人，那么你就可以选择['1A','2A','2B']，这里的1和2代表的是排数(选座默认出现两排图形位置)。也就是'1A','2A','2B'三个元素代表3个人，A和B代表座位的位置，1和2代表的是排数
CHOOSE_SEATS = []

# 刷票间隔(单位:s)
QUERY_TICKET_REFERSH_INTERVAL = 5