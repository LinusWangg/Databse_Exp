import jaydebeapi
url = 'jdbc:postgresql://123.60.69.255:26000/db_test'
user = 'dboper'
password = 'abcd@123'
driver = 'org.postgresql.Driver'
jarFile = 'G:\postgresql.jar'
conn = jaydebeapi.connect(driver,url,[user,password],jarFile)
curs=conn.cursor()
sqlStr = 'select * from mytable'
curs.execute(sqlStr)
result=curs.fetchall()
print(result)
curs.close()
conn.close()