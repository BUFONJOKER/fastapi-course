
# 🏥 FastAPI Patient Management API(fastapi-course)

A **FastAPI** project from the **FastAPI Course** to manage patient data.  
Built with **Python** using **uvicorn** as the server and stored in **JSON**.  

GitHub Repo: [BUFONJOKER/fastapi-course](https://github.com/BUFONJOKER/fastapi-course)

---

## ✨ Features

- 📝 **Create** new patient records  
- 👀 **Read** all patients or a single patient by ID  
- ✏️ **Update** patient details  
- ❌ **Delete** patient records  
- 📊 **Sort** patients by height, weight, or BMI  
- 💪 **Computed Fields**:
  - BMI (Body Mass Index)  
  - Health verdict based on BMI  

---

## 🛠 Technologies Used

- Python 3.x 🐍  
- [FastAPI](https://fastapi.tiangolo.com/) ⚡  
- [Pydantic](https://pydantic-docs.helpmanual.io/) 📐  
- JSON file as simple database 🗄  
- uvicorn for running the server 🚀  

---

## 🚀 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/BUFONJOKER/fastapi-course.git
cd fastapi-course
````

2. **Create a uv project (optional but recommended):**

```bash
uv init
```

3. **Install dependencies:**

```bash
uv sync
```

---

## 🏃 Running the API

Start the server using **uvicorn**:

```bash
uvicorn main:app --reload
```

* API URL: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* Swagger UI (API docs): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📌 API Endpoints

| Method | Endpoint        | Description                                      |
| ------ | --------------- | ------------------------------------------------ |
| GET    | `/`             | 👋 Welcome message                               |
| GET    | `/about`        | ℹ️ About API                                     |
| GET    | `/view`         | 📋 View all patients                             |
| GET    | `/patient/{id}` | 🔎 View patient by ID                            |
| GET    | `/sort`         | 📊 Sort patients by `height`, `weight`, or `bmi` |
| POST   | `/create`       | ➕ Create a new patient                           |
| PUT    | `/update/{id}`  | ✏️ Update patient details by ID                  |
| DELETE | `/delete/{id}`  | ❌ Delete patient by ID                           |

---

## 👤 Patient Model

### Fields

* `id` (str) – Unique patient ID
* `name` (str) – Patient name
* `city` (str) – City of patient
* `age` (int) – Age (1-100)
* `gender` (Literal['male','female']) – Gender
* `height` (float) – Height in meters
* `weight` (float) – Weight in kilograms
* `bmi` (float, computed) – Body Mass Index
* `verdict` (str, computed) – Health status based on BMI

---

### 🏋️ BMI Verdicts

| BMI Range   | Verdict     |
| ----------- | ----------- |
| < 18.5      | Underweight |
| 18.5 - 24.9 | Normal      |
| 25 - 29.9   | Overweight  |
| ≥ 30        | Obesity     |

---

## 📊 Sorting Example

**Query Parameters**:

* `sort_by` – `height`, `weight`, or `bmi`
* `order_by` – `asc` or `desc` (default `asc`)

Example:

```
GET /sort?sort_by=bmi&order_by=desc
```

---

## 💾 Data Storage

* Data is stored in **`patients.json`**
* All CRUD operations directly read and write to this file

---

## 📜 License

This project is licensed under the **MIT License**

---
