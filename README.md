# 🧹 CSV Cleaner & Validator

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?style=flat-square&logo=pandas)
![Pydantic](https://img.shields.io/badge/Pydantic-Data%20Validation-E92063?style=flat-square&logo=pydantic)

🇬🇧 A Data Quality and Sanitization pipeline built in Python to ingest raw CSV files, enforce strict schema validations, clean bad formatting, and split output records into clean datasets and detailed error reports.

🇧🇷 Um pipeline de Qualidade e Higienização de Dados desenvolvido em Python para ingerir arquivos CSV brutos, aplicar validações estritas de esquema, limpar formatações incorretas e separar os registros em conjuntos de dados limpos e relatórios detalhados de erros.

---

## 🏗️ Architecture & Data Flow

```text
[ Raw CSV Input ] ──► [ Pandas Ingestion ] ──► [ Pydantic Schema Validation ]
                                                         │
                                    ┌────────────────────┴────────────────────┐
                                    ▼                                         ▼
                        [ Valid Records (Cleaned) ]              [ Invalid Records (Isolated) ]
                                    │                                         │
                                    ▼                                         ▼
                         data/clean_records.csv                    data/error_report.csv

```

---

## 🛡️ Applied Validation Rules

| Field | Validation / Transformation Rule | Error Cause |
| --- | --- | --- |
| `id` | Must be a valid integer | Non-numeric or missing ID |
| `nome` | String whitespace stripping (`.strip()`); cannot be empty | Blank space or empty field |
| `email` | Validated against `EmailStr` syntax pattern | Invalid email structure |
| `valor_compra` | Converted to `float`; must be strictly positive (`gt=0`) | Negative numbers, text (`abc`), or `NULL` |
| `data_transacao` | Coerced to ISO 8601 format (`YYYY-MM-DD`) from multiple input formats | Unparseable date or impossible calendar date |

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Data Manipulation:** Pandas
* **Data Validation:** Pydantic v2 & `email-validator`
* **Version Control:** Git / GitHub

---

## 📁 Repository Structure

```text
.
├── data/
│   ├── raw_input.csv        # Raw incoming dataset with intentional errors
│   ├── clean_records.csv    # Approved and sanitized output dataset
│   └── error_report.csv     # Isolated rejected records with error messages
├── main.py                  # Pipeline execution and validation engine
├── requirements.txt         # Project Python dependencies
├── .gitignore               # Version control rules
└── README.md                # Technical documentation

```

---

## ⚙️ Setup & Execution

1. **Clone the repository:**
```bash
git clone [https://github.com/evertonhenriquealves/csv-cleaner-validator.git](https://github.com/evertonhenriquealves/csv-cleaner-validator.git)
cd csv-cleaner-validator

```


2. **Install Python dependencies:**
```bash
pip install -r requirements.txt

```


3. **Run the validation pipeline:**
```bash
python main.py

```
