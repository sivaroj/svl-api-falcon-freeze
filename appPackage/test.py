d = [{'dn_no':'1234','source_point':'YARDL','dn_order':5,'in_out':1},{'dn_no':'1235','source_point':'YARDL','dn_order':5,'in_out':2}]
print(d)
for r in d:
    if r['dn_no']=='1234' and r['source_point']=='YARDL' and r['dn_order']==5:
        print(r['in_out'])
