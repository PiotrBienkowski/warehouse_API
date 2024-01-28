# API for Warehouse

This is the API that handles the basic functionality of the API needed for the warehouse.

## Framework

I chose Flask because this project has little functionality and is lightweight. In addition, Flask gives you a lot of flexibility when structuring your project (I gave up controllers because of the small functionality). Giving up controllers in such a project allows for greater clarity and easier code maintenance.  At the same time, the chosen framework does not block the ability to scale the project.

## Validation

For categories, the API allows you to create a tree where each category can have a different overarching category. Such a solution implies the need to use recursion when updating data, so that there is no situation where one vertex is its descendant and ancestor at the same time. 

In addition, the parent category cannot be removed if there is any part in the subtree. I used the BFS algorithm - DFS would also work in this case, but I decided not to use recursion in this method.

## Search Algorithm

In the search algorithm, I decided to add a coefficient to each part. I decided that this coefficient would be the smallest possible Levenshtein distance. I calculate the coefficient for each part, then sort the array and return the best matches.

## Instalation
<!-- TODO -->

## Endpoints

### Create Part

- **URL:** `/parts`
- **Metoda:** `POST`
- **Payload:** `{"serial_number": "X", "name": "X", "description": "X", "category": "id", "quantity": 100, "price": 0.10, "location": {"room": "A1", "bookcase": "B1", "shelf": "C1", "cuvette": "D1", "column": "E1", "row": "F1" }}`
- **Odpowiedź:** `Part updated successfully`

### Read Part

- **URL:** `/parts`
- **Metoda:** `GET`

### Read One Part

- **URL:** `/parts/{id}`
- **Metoda:** `GET`

### Update Part

- **URL:** `/parts/{id}`
- **Metoda:** `PUT`

### Delete Part

- **URL:** `/parts/{id}`
- **Metoda:** `PUT`

---

### Create Category

- **URL:** `/categories`
- **Metoda:** `POST`
- **Payload:** `{"name": "X", "parent_id": "id"}`
- **Odpowiedź:** `Part updated successfully`

### Read Category

- **URL:** `/categories`
- **Metoda:** `GET`

### Read One Part

- **URL:** `/categories/{id}`
- **Metoda:** `GET`

### Update Category

- **URL:** `/categories/{id}`
- **Metoda:** `PUT`

### Delete Category

- **URL:** `/categories/{id}`
- **Metoda:** `PUT`