# API Documentation

## Base URL
`http://localhost:8000`

---

## 1. Register a Complaint
Register a new complaint for a missing bag.

### Endpoint
**POST** `/registerComplaint`

### Request Body
```json
{
  "color_hex": "#FF4500",  
  "size": "medium",        
  "embeddings": [0.1, 0.2, 0.3],  
  "images": ["image1.jpg", "image2.jpg"],  
  "owner_name": "John Doe",  
  "owner_contact": "john@example.com",  
  "owner_passport": "A12345678"  
}
```

### Response
```json
{
  "message": "Complaint registered successfully",
  "bag_uid": "f47ac10b-58cc-4372-a567-0e02b2c3d479",  
  "color_name": "Orange"  
}
```

### Example
```bash
curl -X POST "http://localhost:8000/registerComplaint" \
     -H "Content-Type: application/json" \
     -d '{
       "color_hex": "#FF4500",
       "size": "medium",
       "embeddings": [0.1, 0.2, 0.3],
       "images": ["image1.jpg", "image2.jpg"],
       "owner_name": "John Doe",
       "owner_contact": "john@example.com",
       "owner_passport": "A12345678"
     }'
```

---

## 2. Register a CCTV Observation
Register a CCTV observation for a specific bag.

### Endpoint
**POST** `/registerSeenOn`

### Request Body
```json
{
  "bag_uid": "f47ac10b-58cc-4372-a567-0e02b2c3d479",  
  "camera_id": "cam001",  
  "images": ["cctv1.jpg", "cctv2.jpg"],  
  "time": "2025-02-21 18:13:37",  
  "similarity_score": 0.95  
}
```

### Response
```json
{
  "message": "CCTV observation registered successfully"
}
```

### Example
```bash
curl -X POST "http://localhost:8000/registerSeenOn" \
     -H "Content-Type: application/json" \
     -d '{
       "bag_uid": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
       "camera_id": "cam001",
       "images": ["cctv1.jpg", "cctv2.jpg"],
       "time": "2025-02-21 18:13:37",
       "similarity_score": 0.95
     }'
```

---

## 3. Get All Complaints
Retrieve a list of all registered complaints.

### Endpoint
**GET** `/getAllComplaints`

### Response
```json
[
  {
    "uid": "f47ac10b-58cc-4372-a567-0e02b2c3d479",  
    "color": "Orange",  
    "color_hex": "#FF4500",  
    "size": "medium",  
    "embeddings": [0.1, 0.2, 0.3],  
    "images": ["image1.jpg", "image2.jpg"],  
    "owner_name": "John Doe",  
    "owner_contact": "john@example.com",  
    "owner_passport": "A12345678"  
  }
]
```

### Example
```bash
curl -X GET "http://localhost:8000/getAllComplaints"
```

---

## 4. Get Complaints by Color (HEX)
Retrieve complaints for a specific color using its HEX value.

### Endpoint
**GET** `/getComplaintByColor/{colorinHEX}`

### Path Parameter
- **colorinHEX**: The HEX value of the color (e.g., `#FF4500`).

### Response
```json
[
  {
    "uid": "f47ac10b-58cc-4372-a567-0e02b2c3d479",  
    "color": "Orange",  
    "color_hex": "#FF4500",  
    "size": "medium",  
    "embeddings": [0.1, 0.2, 0.3],  
    "images": ["image1.jpg", "image2.jpg"],  
    "owner_name": "John Doe",  
    "owner_contact": "john@example.com",  
    "owner_passport": "A12345678"  
  }
]
```

### Example
```bash
curl -X GET "http://localhost:8000/getComplaintByColor/FF4500"
```

#### Error Responses
- **Invalid HEX Color**
  ```json
  {
    "detail": "Invalid HEX color format. Please provide a valid HEX color (e.g., #FF0000)."
  }
  ```
- **No Complaints Found**
  ```json
  {
    "detail": "No complaints found for this color"
  }
  ```

---

## Summary of Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/registerComplaint` | **POST** | Register a new complaint for a missing bag. |
| `/registerSeenOn` | **POST** | Register a CCTV observation for a bag. |
| `/getAllComplaints` | **GET** | Retrieve a list of all complaints. |
| `/getComplaintByColor/{hex}` | **GET** | Retrieve complaints for a specific color. |

---

## Example Workflow
1. **Register a Complaint:**
   - Use `/registerComplaint` to register a new bag complaint.
   - The response will include a `bag_uid` for future reference.

2. **Register a CCTV Observation:**
   - Use `/registerSeenOn` with the `bag_uid` to register a CCTV observation.

3. **Retrieve Complaints:**
   - Use `/getAllComplaints` to retrieve all complaints.
   - Use `/getComplaintByColor/{hex}` to retrieve complaints for a specific color.

