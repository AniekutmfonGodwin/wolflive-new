import csv
import os
class dborm:
    """
    docstring
    """
    def __init__(self,*args, **kwargs):
        self.fields = kwargs.get('fields')
        self._file_dir = os.path.dirname(__file__)
        self._class_name = type(self).__name__
        self._db_path = os.path.join(self._file_dir,f"{self._class_name}.csv")
        self.initiator()

    
    def save(self,*args, **kwargs):
        pass

    def exists(self,*args, **kwargs):
        data = self.get_list() 
        def condition(item):
            return all([item.get(x).strip() in kwargs.get(x) for x in kwargs])
        return list(filter(condition,data))


    def initiator(self,*args, **kwargs):
        if os.path.isfile(self._db_path):
            with open(self._db_path,'r',newline='\n',encoding='utf-8') as file:
                reader = csv.DictReader(file,delimiter='|',quotechar='|')
                try:
                    if sorted([x[0] for x in csv.reader(reader.fieldnames)]) != sorted(self.fields):
                        self.create()
                except:
                    pass
                    
        elif not os.path.isfile(self._db_path):
            
            
            self.create()




    def create(self,*args, **kwargs):
        with open(self._db_path, 'w',newline='\n',encoding='utf-8') as csvfile:
            fieldnames = self.fields
            writer = csv.DictWriter(csvfile,delimiter='|', fieldnames=fieldnames)
            writer.writeheader()

    def write(self,data,*args, **kwargs):
        with open(self._db_path, 'w', newline='\n',encoding='utf-8') as csvfile:
            fieldnames = self.fields
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter='|')
            writer.writeheader()
            writer.writerows(data)
    

    def get(self,*args, **kwargs):
        
        return self.exists(*args, **kwargs)

    def get_list(self,*args, **kwargs):
        with open(self._db_path,'r',newline='\n',encoding='utf-8') as file:
            reader = (x for x in list(csv.DictReader(file,delimiter='|',quotechar='|')))
        return reader

    

    def add(self,*args, **kwargs):
        with open(self._db_path, 'a',newline='\n',encoding='utf-8') as csvfile:
            fieldnames = self.fields
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter='|')
            writer.writerow(kwargs)
        return kwargs

    def update(self,data,*args, **kwargs):
        assert len(kwargs)!= 0,'conditions cant be empty\nobj.update(data,condition1=value1,condition2=value2)'
        query_list = list(self.get_list())
        updated_data = []
        def condition(item):
            if all([item.get(x).strip() in kwargs.get(x) for x in kwargs]):
                updated_data.append({**item,**data})
                return {**item,**data}
            # if list(item) !=self.fields:print(item)
            return item
        result = list(map(condition,query_list))
        self.write(result)
        return updated_data
        
        
        

    def delete(self,*args, **kwargs):
        assert len(kwargs)!= 0,'conditions cant be empty\nobj.update(data,condition1=value1,condition2=value2)'
        query_list = list(self.get_list())
        def condition(item):
            return any([item.get(x)!=kwargs.get(x) for x in kwargs])
        result = list(filter(condition,query_list))
        self.write(result)
        return True








if __name__ == '__main__':
    db = dborm(fields=['image','count'])
    # print(db.add(image='textimage.jpg',count=22))
    # print(list(db.get_list()))
    # print(db.delete(image='hhgsfs.dd'))
    # print(db.add(count='11',image='hhgsfs.dd'))
    print(bool(db.exists()))
        