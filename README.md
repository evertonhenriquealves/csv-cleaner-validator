# 🧹 CSV Cleaner & Validator

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?style=flat-square&logo=pandas)
![Pydantic](https://img.shields.io/badge/Pydantic-Data%20Validation-E92063?style=flat-square&logo=pydantic)

🇬🇧 A Data Quality and Sanitization pipeline built in Python to ingest raw CSV files, enforce strict schema validations, clean bad formatting, and split output records into clean datasets and detailed error reports.

🇧🇷 Um pipeline de Qualidade e Higienização de Dados desenvolvido em Python para ingerir arquivos CSV brutos, aplicar validações estritas de esquema, limpar formatações incorretas e separar os registros em conjuntos de dados limpos e relatórios detalhados de erros.
---

## 🏗️ Architecture & Data Flow

Pandas only reads the file (every column as text, so no value is silently converted). The cleaning and the validation rules live in the Pydantic model, and each row is checked one at a time.

```text
[ data/raw_input.csv ]
         │
         ▼
[ Pandas: read all columns as text, empty values as "" ]
         │
         ▼
[ Pydantic model, row by row: clean + validate ]
         ├── valid   ──► data/clean_records.csv
         └── invalid ──► data/error_report.csv (line number + reason)
```

---

## 🛡️ Validation Rules

| Field | Rule | Rejected when |
| --- | --- | --- |
| `id` | Must be an integer | Non-numeric or missing |
| `nome` | Leading and trailing spaces removed (`.strip()`); cannot be empty | Empty or only spaces |
| `email` | Checked with Pydantic `EmailStr` (`email-validator`) | No `@`, or nothing after it |
| `valor_compra` | Converted to `float`; must be greater than 0 | Negative, zero, text (`abc`) or empty/`NULL` |
| `data_transacao` | Accepts `YYYY-MM-DD`, `YYYY/MM/DD`, `DD-MM-YYYY`, `DD/MM/YYYY` and writes `YYYY-MM-DD` | Unknown format or a date that does not exist (e.g. `31/02/2026`) |

**Assumption:** a date such as `04-09-2026` is read as day first, so it becomes `2026-09-04`.

**Note on `NULL`:** Pandas reads the text `NULL` as a missing value, so the pipeline sees an empty string and rejects it as an invalid number.

---

## 📊 Result on the Sample Data

The sample file has 12 rows with intentional errors.

```text
Total lines read: 12
Approved:         6 (50.0%)
Rejected:         6 (50.0%)
```

| CSV line | Reason for rejection |
| --- | --- |
| 3 | Email without `@` |
| 4 | Empty name and a non-numeric value (`abc`) |
| 6 | Negative value (`-50.00`) |
| 8 | Email with nothing after `@` and a value of `0` |
| 10 | Value is `NULL` (read as empty) |
| 12 | Date that does not exist (`31/02/2026`) |

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Reading the file:** Pandas
* **Validation and cleaning:** Pydantic v2 and `email-validator`
* **Version control:** Git / GitHub

---

## 📁 Repository Structure

```text
.
├── data/
│   ├── raw_input.csv        # Input with intentional errors
│   ├── clean_records.csv    # Approved and cleaned rows
│   └── error_report.csv     # Rejected rows with line number and reason
├── main.py                  # Pipeline and validation model
├── requirements.txt         # Python dependencies
├── .gitignore
└── README.md
```

---

## ⚙️ Setup & Execution

1. Clone the repository:

```bash
git clone https://github.com/evertonhenriquealves/csv-cleaner-validator.git
cd csv-cleaner-validator
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Run the pipeline:

```bash
python main.py
```
