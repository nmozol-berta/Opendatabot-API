import pandas as pd
import sqlite3


con = sqlite3.connect("./adm_tools/temp_tzov.db")
cur = con.cursor()
# cur.execute(
#     """create table if not exists temp_table(
#                     egrpou nvarchar(10),
#                     name nvarchar(500),
#                     name_short nvarchar(300),
#                     address nvarchar(1000)
#                     );
#                     """
# )
# con.commit()



df=pd.read_sql_query('select * from temp_table;',con)



df.to_excel('./adm_tools/file.xlsx',index=False)