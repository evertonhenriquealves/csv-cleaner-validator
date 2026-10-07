import os
from decimal import Decimal
import pandas as pd
from pydantic import BaseModel, EmailStr, Field, ValidationError, field_validator
from datetime import datetime

# Pathing setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
INPUT_FILE = os.path.join(DATA_DIR, "raw_input.csv")
CLEAN_FILE = os.path.join(DATA_DIR, "clean_records.csv")
ERROR_FILE = os.path.join(DATA_DIR, "error_report.csv")


class TransactionModel(BaseModel):
    id: int
    nome: str
    email: EmailStr
    valor_compra: Decimal = Field(gt=0, description="O valor deve ser estritamente positivo")
    data_transacao: str

    @field_validator("nome")
    def clean_nome(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("O campo 'nome' não pode ser vazio ou conter apenas espaços.")
        return cleaned

    @field_validator("data_transacao")
    def validate_and_format_date(cls, value: str) -> str:
        date_str = value.strip()

        # Lista de formatos aceitos para parsing (datas com dia primeiro, padrão brasileiro)
        formats_to_try = [
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%d-%m-%Y",
            "%d/%m/%Y"
        ]

        for fmt in formats_to_try:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                return parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                continue

        raise ValueError(f"Data '{value}' possui um formato inválido ou é uma data impossível.")


def format_validation_errors(error: ValidationError) -> str:
    """Transforma o erro do Pydantic em um texto curto: 'campo: mensagem | campo: mensagem'."""
    messages = []
    for err in error.errors():
        field = ".".join(str(part) for part in err["loc"])
        message = err["msg"].removeprefix("Value error, ")
        messages.append(f"{field}: {message}")
    return " | ".join(messages)


def process_csv():
    if not os.path.exists(INPUT_FILE):
        print(f"Erro: O arquivo de entrada '{INPUT_FILE}' não foi encontrado.")
        return

    print("Iniciando o processamento do arquivo CSV...\n")

    # Leitura do CSV bruto (trata valores em branco/NULL como string vazia)
    df_raw = pd.read_csv(INPUT_FILE, dtype=str).fillna("")

    total_processed = len(df_raw)
    if total_processed == 0:
        print("O arquivo não tem nenhuma linha de dados para processar.")
        return

    clean_records = []
    error_records = []

    for index, row in df_raw.iterrows():
        row_dict = row.to_dict()
        row_number = index + 2  # Linha física do arquivo (considerando o cabeçalho como linha 1)

        try:
            # Validação via Pydantic
            valid_record = TransactionModel(**row_dict)
            clean_records.append(valid_record.model_dump())
        except ValidationError as e:
            # Captura o motivo do erro e isola o registro inválido
            row_dict["linha_csv"] = row_number
            row_dict["motivo_erro"] = format_validation_errors(e)
            error_records.append(row_dict)

    # Salvando registros limpos
    df_clean = pd.DataFrame(clean_records)
    if not df_clean.empty:
        df_clean.to_csv(CLEAN_FILE, index=False)
        print(f"✅ Registros VÁLIDOS salvos em: {CLEAN_FILE} ({len(df_clean)} linhas)")
    else:
        print("⚠️ Nenhum registro válido foi encontrado.")

    # Salvando relatório de erros
    df_error = pd.DataFrame(error_records)
    if not df_error.empty:
        df_error.to_csv(ERROR_FILE, index=False)
        print(f"❌ Registros INVÁLIDOS salvos em: {ERROR_FILE} ({len(df_error)} linhas)")
    else:
        print("🎉 Nenhum erro encontrado no arquivo.")

    # Métricas de execução
    valid_count = len(clean_records)
    invalid_count = len(error_records)

    print("\n--- RESUMO DO PROCESSAMENTO ---")
    print(f"Total de linhas lidas: {total_processed}")
    print(f"Linhas Aprovadas:      {valid_count} ({(valid_count/total_processed)*100:.1f}%)")
    print(f"Linhas Rejeitadas:     {invalid_count} ({(invalid_count/total_processed)*100:.1f}%)")


if __name__ == "__main__":
    process_csv()
