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
- **Database:** (MongoDB/PostgreSQL - to be determined)
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
#### **Endpoint:** `/generate-questions`
**Method:** `POST`
**Request Body:**
```json
{
  "employee_name": "John Doe",
  "role": "Software Engineer",
  "department": "IT",
  "experience": 5,
  "years_in_company": 2,
  "last_promotion_date": "2023-05-10",
  "last_training": "Advanced Python",
  "performance_feedback": "Exceeds Expectations",
  "career_goals": "Become a Tech Lead",
  "company_name": "TechCorp",
  "company_growth_strategy": "Expand AI capabilities",
  "available_trainings": "Leadership Training, AI Ethics",
  "internal_mobility_policies": "Open for internal transitions",
  "interview_type": "Career Development",
  "num_questions": 5
}
```

**Response:**
```json
{
  "interview_phase": "Career Development",
  "questions": [
    { "id": 1, "type": "career_growth", "question": "What new challenges would you like to take on?" },
    { "id": 2, "type": "training", "question": "What other skills do you wish to develop?" }
  ]
}
```

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

