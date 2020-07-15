from appPackage import ConvertUtil
if __name__ == '__main__':
    dateAD = '21/06/2020 23:23:11'
    print(dateAD)
    convd = ConvertUtil.dateBEtoAD(None,dateAD)
    print(convd)
    t='L001'
    nt = ConvertUtil.convert_truck(None, t)
    print(nt)