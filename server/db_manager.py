import json

import MySQLdb


class DBManager:
    def __init__(self, host, user, passwd, db):
        self.columns = ('temperature', 'humidity')
        self.db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
        self.cursor = self.db.cursor()

    def latest(self):
        self.cursor.execute("SELECT * FROM user_history ORDER BY stamp DESC LIMIT 1")
        self.db.commit()
        row = self.cursor.fetchone()
        row_dict = {self.columns[i]: row[i] for i in range(len(row) - 1)}
        return json.dumps(row_dict)

    def sound_alert(self):
        self.cursor.execute('SELECT * FROM sound_history ORDER BY stamp desc limit 1')
        self.db.commit()
        row = self.cursor.fetchone()
        if row:
            return json.dumps({'problem': row[0]})
        return json.dumps({'problem': 0})

    def temp_alert(self):
        self.cursor.execute('SELECT * FROM temp_history ORDER BY stamp desc limit 1')
        self.db.commit()
        row = self.cursor.fetchone()
        if row:
            return json.dumps({'problem': row[0]})
        return json.dumps({'problem': 0})

    def report(self, period):
        if period == 'weekly':
            self.cursor.execute("SELECT * FROM user_history WHERE stamp"
                                " between date_sub(now(),INTERVAL 1 WEEK) and now();")
        elif period == 'daily':
            self.cursor.execute("SELECT * FROM user_history WHERE DATE(stamp)=CURDATE()")
        elif period == '':
            self.cursor.execute("SELECT * FROM user_history ORDER BY stamp")
        self.db.commit()
        count = int(self.cursor.rowcount)
        ret_arr = []
        for i in range(count):
            row = self.cursor.fetchone()
            row_dict = {self.columns[i]: row[i] for i in range(len(row) - 1)}
            ret_arr.append(row_dict)
        return json.dumps({'scores': ret_arr})

    def get_insert_query(self, table, col_dict):
        command_str = 'Insert into ' + table
        val_str = 'Values('
        field_str = '('
        for field, value in col_dict.iteritems():
            field_str += field + ', '
            if value is None:
                val_str += 'NULL'
            elif isinstance(value, basestring):
                val_str += '"' + value + '"'
            else:
                val_str += str(value)
            val_str += ', '
        val_str = val_str[:-2] + ')'
        field_str = field_str[:-2] + ')'
        final_query = command_str + " " + field_str + " " + val_str
        return final_query
