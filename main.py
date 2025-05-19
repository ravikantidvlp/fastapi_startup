from typing import Union

from fastapi import FastAPI,HTTPException
import MySQLdb
from model.item import Item
app = FastAPI()

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': 'srib@123',
    'db': 'srib',
}

# Create a connection to the database
conn = MySQLdb.connect(**db_config)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Route to read an item
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    cursor = conn.cursor()
    query = "SELECT * FROM items WHERE id=%s"
    cursor.execute(query, (item_id,))
    item = cursor.fetchone()
    cursor.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item[0], "itemname": item[1], "itemprice": item[2],"isactive": item[3]}

@app.get("/items")
def read_items():
    cursor = conn.cursor()
    my_list = []
    query = "SELECT * FROM items"
    cursor.execute(query)
    result = cursor.fetchall()

    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for all in result:
        print(all[0])
        my_list.append({'id':all[0],'name':all[1],'price':all[2],'isactive':all[3]})
    cursor.close()
    return my_list

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    cursor = conn.cursor()
    query = "INSERT INTO items (itemname, itemprice,isactive) VALUES (%s, %s, %s)"
    cursor.execute(query, (item.itemname, item.itemprice,item.isactive))
    conn.commit()
    item.id = cursor.lastrowid
    cursor.close()
    return item

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
