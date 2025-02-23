# API Documentation

## Flow
The process begins with the machine learning (ML) model identifying and defining the appropriate category for an input. Once the category is determined, the system retrieves a list of all available classes from the database. It then evaluates and selects the class that best matches the identified category. After determining the most suitable class, the system further refines the categorization by comparing the input with existing categories in the database to find the best match.

**Base URL**: `http://34.136.67.113:1234/`

---

## Endpoints

### 1. GET `/getEmbeddingsList`
Retrieve a list of unique identifiers (`uids`) for all entries under a specified class and category.

#### Parameters
- `className` (string, required): The name of the class (e.g., "Tools"). Case-insensitive.
- `categoryName` (string, optional): The name of the category under the class (e.g., "Hammer"). Case-insensitive. If not provided, all `uids` in the specified class will be returned, irrespective of category.

#### Response
- **200 OK**: List of `uids`.
  ```json
  {
    "uids": ["550e8400-e29b-41d4-a716-446655440000", "6ba7b810-9dad-11d1-80b4-00c04fd430c8"]
  }
  ```
- **404 Not Found**: If the class or category doesn’t exist.
  ```json
  {
    "detail": "Class or category not found"
  }
  ```

#### Example
```bash
curl "http://34.136.67.113:1234/getEmbeddingsList?className=Tools&categoryName=Hammer"
```

---

### 2. GET `/getEmbeddingsById`
Retrieve the details (embedding, metadata, and image) of a specific entry by its `uid` under a specified class.

#### Parameters
- `className` (string, required): The name of the class (e.g., "Tools"). Case-insensitive.
- `uid` (string, required): The unique identifier of the entry (e.g., "550e8400-e29b-41d4-a716-446655440000").

#### Response
- **200 OK**: Details of the entry.
  ```json
  {
    "embedding": [0.4, 0.5, 0.6],
    "metadata": {"color": "black", "material": "steel"},
    "image": "/images/hammer_003.jpg"
  }
  ```
- **404 Not Found**: If the entry or class doesn’t exist.
  ```json
  {
    "detail": "Entry not found"
  }
  ```

#### Example
```bash
curl "http://34.136.67.113:1234/getEmbeddingsById?className=Tools&uid=550e8400-e29b-41d4-a716-446655440000"
```

---

### 3. POST `/generateEntry`
Create a new entry under a specified class and category with an auto-generated `uid`.

#### Parameters
- `className` (string, required): The name of the class (e.g., "Tools"). Case-insensitive.
- `categoryName` (string, required): The name of the category under the class (e.g., "Hammer"). Case-insensitive.

#### Request Body
```json
{
  "embedding": [0.4, 0.5, 0.6],
  "metadata": {"color": "black", "material": "steel"},
  "image": "/images/hammer_003.jpg"
}
```

#### Response
- **200 OK**: Confirmation of entry creation with the generated `uid`.
  ```json
  {
    "message": "Entry created successfully under tools/hammer",
    "uid": "550e8400-e29b-41d4-a716-446655440000"
  }
  ```

#### Example
```bash
curl -X POST "http://34.136.67.113:1234/generateEntry?className=Tools&categoryName=Hammer" \
-H "Content-Type: application/json" \
-d '{"embedding": [0.4, 0.5, 0.6], "metadata": {"color": "black", "material": "steel"}, "image": "/images/hammer_003.jpg"}'
```

---

### 4. GET `/getAllClasses`
Retrieve a list of all unique class names in the database.

#### Parameters
- None

#### Response
- **200 OK**: List of class names.
  ```json
  {
    "classes": ["tools", "animals", "vehicles"]
  }
  ```
- **200 OK (empty)**: If no classes exist.
  ```json
  {
    "classes": []
  }
  ```

#### Example
```bash
curl "http://34.136.67.113:1234/getAllClasses"
```

---

### 5. GET `/getAllCategories`
Retrieve a list of all unique category names under a specified class.

#### Parameters
- `className` (string, required): The name of the class (e.g., "Tools"). Case-insensitive.

#### Response
- **200 OK**: List of category names.
  ```json
  {
    "categories": ["hammer", "screwdriver", "wrench"]
  }
  ```
- **404 Not Found**: If the class doesn’t exist.
  ```json
  {
    "detail": "Class not found"
  }
  ```

#### Example
```bash
curl "http://34.136.67.113:1234/getAllCategories?className=Tools"
```

---

## Notes

- **Case Insensitivity**: All `className` and `categoryName` parameters are converted to lowercase before querying the database.
- **Metadata Storage**: The `metadata` field is stored as a JSON string in Neo4j and deserialized to a dictionary in responses.
- **Image Handling**: The `image` field is assumed to be a string (e.g., file path or URL). Actual image data is not stored in the database.
- **Redundancy**: The `/generateEntry` endpoint uses `MERGE` to avoid duplicating `ClassNodes` and `CategoryNodes`. Use `/getAllClasses` and `/getAllCategories` to check existing entries before adding new ones.

## Database Structure

- **Master Node**: `:Class`
- **Class Nodes**: `:ClassNode {name: string}`
- **Category Nodes**: `:CategoryNode {name: string}`
- **Entry Nodes**: `:Entry {uid: string, embedding: [float], metadata: string, image: string}`

### Relationships
- `(Class)-[:HAS_CLASS]->(ClassNode)`
- `(ClassNode)-[:HAS_CATEGORY]->(CategoryNode)`
- `(CategoryNode)-[:HAS_ENTRY]->(Entry)`

