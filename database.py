from sqlite3 import connect, Error

class CRUD:
    def __init__(self, name):
        self.name = name  # 'name' parametrini saqlash

    def createtable(self):
        """Creates the 'category' table."""
        try: 
            c = connect('resataran.db')
            cursor = c.cursor()
            cursor.execute(""" 
                CREATE TABLE IF NOT EXISTS category (
                    id INTEGER PRIMARY KEY NOT NULL,
                    name TEXT NOT NULL
                ); 
            """)
            c.commit()
        except Exception as e:
            print('Error:', e)
        finally:
            if c:
                cursor.close()
                c.close()
        return 'bajarildi'

    def creatproduct(self):
        """Creates the 'Products' table."""
        try: 
            c = connect('resataran.db')
            cursor = c.cursor()
            cursor.execute(""" 
                CREATE TABLE IF NOT EXISTS Products (
                    id INTEGER PRIMARY KEY NOT NULL,
                    name TEXT NOT NULL,
                    narxi INTEGER NOT NULL,
                    category_id INTEGER NOT NULL
                ); 
            """)
            c.commit()
        except Exception as e:
            print('Error:', e)
        finally:
            if c:
                cursor.close()
                c.close()
        return 'bajarildi'

    def Insertcategory(self, nomi):
        try:
            c = connect('resataran.db')
            cursor = c.cursor()
            cursor.execute(f"INSERT INTO category (name) VALUES (?)", (nomi,))
            c.commit()
        except Exception as e:
            print('xatolik', e)
        finally:
            if c:
                cursor.close()
                c.close()
        return 'bajarildi'

    def readcategory(self):
        """Reads all categories from the 'category' table."""
        try: 
            c = connect('resataran.db')
            cursor = c.cursor()
            cursor.execute("SELECT * FROM category")
            result = cursor.fetchall()
            return result
        except Exception as e:
            print('Error:', e)
        finally:
            if c:
                cursor.close()
                c.close()
        return 'bajarildi'


    def InsertProduct(self, nomi,narxi,rasm ,category_id):
        try:
            c = connect('resataran.db')
            cursor = c.cursor()
            cursor.execute(f"INSERT INTO category (name) VALUES (?)", (nomi,narxi,rasm ,category_id))
            c.commit()
        except Exception as e:
            print('xatolik', e)
        finally:
            if c:
                cursor.close()
                c.close()
        return 'bajarildi'

    def readproduct(self):
        """Reads all categories from the 'category' table."""
        try: 
            c = connect('resataran.db')
            cursor = c.cursor()
            cursor.execute("SELECT * FROM Products")
            result = cursor.fetchall()
            return result
        except Exception as e:
            print('Error:', e)
        finally:
            if c:
                cursor.close()
                c.close()
        return 'bajarildi'




