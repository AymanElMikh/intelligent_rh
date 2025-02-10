
# 📌 Intelligent HR Interview Assistant

## 🏆 **Project Overview**
The **Intelligent HR Interview Assistant** is a backend-powered system designed to streamline and enhance professional interviews within companies. This solution leverages **LLMs (Large Language Models)** to facilitate HR processes by:

- **Generating dynamic interview questions** tailored to employees.
- **Interpreting and analyzing employee responses** to extract key insights.
- **Enhancing HR decision-making** through AI-driven evaluations.

---

## 🚀 **Key Features**
### 🎤 **Professional Interview Question Generation**
- Automatically generates **customized interview questions** based on:
  - Employee role
  - Experience level
  - Career aspirations
  - Internal company policies
- Supports **structured interview formats** for mandatory HR assessments.

### 📊 **Response Interpretation & Analysis**
- Uses AI to **interpret employee responses** and assess:
  - Job satisfaction
  - Career growth opportunities
  - Training needs
  - Potential internal mobility

### 🏢 **HR Compliance & Professional Development**
- Aligns with company HR policies and **legally mandated professional interviews** (biennial and six-year assessments).
- Supports **training recommendations** and skill development insights.

---

## 🔧 **Tech Stack**
- **Backend Framework:** FastAPI (Python 3.12)
- **AI & NLP:** OpenAI API (GPT-4 Turbo)
- **Database:** MongoDB
- **Dependency Management:** Poetry
- **Server:** Uvicorn

---

## 🛠 **Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/AymanElMikh/intelligent_rh.git
cd intelligent_rh
```

### **2️⃣ Setup Virtual Environment (Using Poetry)**
```bash
poetry install
```

### **3️⃣ Configure Environment Variables**
Create a `.env` file in the root directory and add:
```ini
OPENAI_API_KEY=your_api_key_here
MONGO_URI=mogo_db_data_base_url
DATABASE_NAME=data_base_name
CORS_ORIGINS="*"
HTTP_METHODS="*"
```

### **4️⃣ Run the API**
```bash
poetry run start
```
OR manually run:
```bash
poetry run uvicorn rh_api.main:app --reload
```

---

## 🎯 **Usage**
### **Generate Interview Questions**
#### **Endpoint:** `/generate-questions/{employee_id}/{interview_phase}`
**Method:** `POST`

### Path Parameters:
- `employee_id`: The unique identifier of the employee (string).
- `interview_phase`: The specific interview phase to generate questions for (e.g., `"career_review"`).

### Response:
- `true`: If the request was successfully processed.

---

## 📌 **Project Structure**
```
intelligent_rh/
│── rh_api/
│   ├── main.py  # FastAPI entry point
│   ├── modules/
│   │   ├── interviewer/
│   │   │   ├── dto/
│   │   │   ├── prompts/
│   │   │   ├── services/
│── pyproject.toml  # Poetry dependencies
│── .env  # API keys & config
│── README.md  # Project documentation
```

---

## 📖 **Future Improvements**
- ✅ **Enhance NLP models** for better response analysis.
- ✅ **Implement database integration** for logging interviews.
- ✅ **Add authentication & role-based access** for HR users.

---

## 🏆 **Contributing**
Contributions are welcome! Feel free to:
- **Submit issues** for bugs or feature requests.
- **Create pull requests** for improvements.

---

## 📄 **License**
This project is licensed under the **MIT License**.

---

## 📩 **Contact**
💡 **Author:** Ayman ElMikh  
📧 **Email:** aymanmikh7@gmail.com  
🔗 **GitHub:** [AymanElMikh](https://github.com/AymanElMikh)
