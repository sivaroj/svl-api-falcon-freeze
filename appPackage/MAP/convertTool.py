import time
import arrow
class ConvertTool():
    def __init__(self):
        pass

    def convertTimeFormat(sec):
        if int(sec) == sec:
            seconds = sec % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            return "%d:%02d:%02d" % (hour, minutes, seconds)
        else:
            return ''

    def tzToBangkok(inputdate):
        offset = (time.timezone if (time.localtime().tm_isdst == 0) else time.altzone) / 60 / 60 * -1
        d = arrow.get(inputdate)
        d = d.to('Asia/Bangkok')
        return d.format('DD/MM/YYYY HH:mm:ss')

    def tzToBangkokAD(inputdate):
        # format วันที่ YYYY-MM-DD
        offset = (time.timezone if (time.localtime().tm_isdst == 0) else time.altzone) / 60 / 60 * -1
        d = arrow.get(inputdate)
        d = d.to('Asia/Bangkok')
        return d.format('YYYY-MM-DD HH:mm:ss')

    def tzToStr(inputDate):
        d = arrow.get(inputDate)
        return d.format('DD/MM/YYYY HH:mm:ss')

    def tzToStrAD(inputDate):
        d = arrow.get(inputDate);
        return d.format('YYYY-MM-DD HH:mm:ss')