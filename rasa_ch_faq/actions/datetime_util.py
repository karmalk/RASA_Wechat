from datetime import datetime, date

#当前日期汉字转换
def datetime_to_chi(num):
    _MAPPING = (u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', u'十',
                u'十一', u'十二', u'十三', u'十四', u'十五', u'十六',u'十七', u'十八', u'十九',u'二十',
                u"二十一",u"二十二",u"二十三",u"二十四",u"二十五",u"二十六",u"二十七",u"二十八",u"二十九",u"s三十",u"三十一"
        )
    if num <=100:
        return _MAPPING[num]
    else:
        result = ""
        for i in str(num):
            result += _MAPPING[int(i)]
        print(result)
        return result


#当前时间汉字转换
def time_to_chi(num):
    _MAPPING = (u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', u'十',
                u'十一', u'十二', u'十三', u'十四', u'十五', u'十六',u'十七', u'十八', u'十九',u'二十',
                u"二十一",u"二十二",u"二十三",u"二十四")
    _P0 = (u'', u'十', u'百', u'千',)
    # 小时直接Mapping
    if num <=24:
        return _MAPPING[num]
    #分钟做计算
    else:
        lst = []
        while num >= 10:
            lst.append(num%10)
            num = num/10
        lst.append(num)
        c = len(lst)
        result = u""
        for idx,val in enumerate(lst):
            val = int(val)
            if val != 0:
                result += _P0[idx] + _MAPPING[val]
                if idx < c-1 and lst[idx + 1] == 0:
                    result += u"零"
        return result[::-1]