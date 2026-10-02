from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
import json


app = FastAPI()


class Item(BaseModel):
    id: int
    name: str
    category: str
    value: float
    updated_at: datetime
    active: bool


class ItemUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    value: float | None = None
    updated_at: datetime | None = None
    active: bool | None = None


def load_items_from_json(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        items_data = json.load(f)
    return [Item(**item) for item in items_data]


items = load_items_from_json('data/processed/normalized_items.json')


@app.get('/')
async def root():
    return {'message': 'Hi'}


@app.get('/api/items/')
def get_items(category: str | None = None):
    if category is None:
        return items

    return [
        item for item in items
        if item.category == category
    ]


@app.get('/api/items/{item_id}')
def get_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item

    raise HTTPException(
        status_code=404,
        detail='Item not found'
    )


@app.post('/api/items/')
def create_item(item: Item):
    if any(existing_item.id == item.id for existing_item in items):
        raise HTTPException(
            status_code=400,
            detail='Item with this ID already exists'
        )

    items.append(item)
    return item


@app.put('/api/items/{item_id}')
def put_item(item_id: int, updated_item: Item):
    for index, item in enumerate(items):
        if item.id == item_id:
            updated_item.id = item_id
            items[index] = updated_item
            return updated_item

    raise HTTPException(
        status_code=404,
        detail='Item not found'
    )


@app.patch('/api/items/{item_id}')
def patch_item(item_id: int, updated_fields: ItemUpdate):
    for index, item in enumerate(items):
        if item.id == item_id:
            data = item.model_dump()
            update_data = updated_fields.model_dump(exclude_unset=True)
            data.update(update_data)

            updated_item = Item(**data)
            items[index] = updated_item

            return updated_item

    raise HTTPException(
        status_code=404,
        detail='Item not found'
    )


@app.delete('/api/items/{item_id}')
def delete_item(item_id: int):
    for index, item in enumerate(items):
        if item.id == item_id:
            deleted_item = items.pop(index)
            return deleted_item

    raise HTTPException(
        status_code=404,
        detail='Item not found'
    )


@app.get('/dynamic', response_class=HTMLResponse)
def dynamic_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Dynamic items</title>
    </head>
    <body>
        <h1>Items</h1>
        <label for="category">Категория:</label>

        <select id="category">
            <option value="">Все</option>
            <option value="books">Books</option>
            <option value="electronics">Electronics</option>
            <option value="food">Food</option>
        </select>

        <button onclick="loadItems()">
            Загрузить данные
        </button>

        <table border="1">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Category</th>
                    <th>Value</th>
                    <th>Active</th>
                </tr>
            </thead>

            <tbody id="items"> </tbody>
        </table>

        <script>
            async function loadItems() {
                const category = document.getElementById('category').value;
                const url = category
                    ? `/api/items/?category=${category}`
                    : '/api/items';
                const response = await fetch(url);
                const data = await response.json();
                const table = document.getElementById('items');
                table.innerHTML = '';
                data.forEach(item => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${item.id}</td>
                        <td>${item.name}</td>
                        <td>${item.category}</td>
                        <td>${item.value}</td>
                        <td>${item.active}</td>
                    `;
                    table.appendChild(row);
                });
            }
        </script>
    </body>
    </html>
    """
