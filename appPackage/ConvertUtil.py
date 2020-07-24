import time
import arrow

class ConvertUtil:
    def convert_date_format(self,date_to_convert,from_format,to_format):
        if from_format == '':
            convert_date = arrow.get(date_to_convert)
        else:
            convert_date  = arrow.get(date_to_convert,from_format)
        return convert_date.format(to_format)

    def dateBEtoAD(self, dateBE):
        # เปลี่ยน format วันที่ 21/06/2020 HH:mm:ss เป็น 2020-06-21 HH:mm:ss ถ้าไม่มีเวลาจะตัดทิ้ง
        d1 = dateBE[0:10]
        t = dateBE[11:]
        d = d1[6:] + "-" + d1[3:5] + "-" + d1[:2]
        BE = '{} {}'.format(d,t).strip()
        return BE

    def dateADtoBE(self,dateAD):
        # เปลี่ยน format วันที่ 2020-06-21 HH:mm:ss เป็น 21/06/2020 HH:mm:ss ถ้าไม่มีเวลาจะตัดทิ้ง
        d1 = dateAD[0:10].split('-')
        t = dateAD[11:]
        d = d1[2]+"/"+d1[1]+"/"+d1[0]
        AD = '{} {}'.format(d, t).strip()
        return AD

    def convert_truck(self, t):
        # เปลี่ยนเบอร์รถ L01 -> L001 ใช้่หาใน Norstra
        v_truck_no = t
        prefix = t[:1]
        suffix = t[1:]
        if suffix.__len__() < 3:
            v_truck_no = prefix + '0' + suffix
        return v_truck_no

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

    # วันที่เวลาโดย arrow format เวลาที่ได้จาก norstra เป็น format "2020-06-21T16:54:26"
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