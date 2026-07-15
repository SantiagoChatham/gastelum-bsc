"""
Sincroniza bms.dbo.Anomalias_DiaSurtir (SQL Server, on-prem) -> Supabase.

Todas las credenciales se leen de variables de entorno (nunca hardcodeadas),
para poder correr esto tanto local como en GitHub Actions sin exponer nada
en el código.

Variables de entorno requeridas:
  SQLSERVER_HOST      -> ej. 170.247.128.23
  SQLSERVER_PORT      -> ej. 50001
  SQLSERVER_USER
  SQLSERVER_PASS
  SUPABASE_URL        -> ej. https://jiqykcjgkpkojnbhlwxo.supabase.co
  SUPABASE_SERVICE_KEY -> la key "service_role" (secreta), NO la anon key
"""

import os
import sys
from datetime import datetime, date
from decimal import Decimal

import pymssql
from supabase import create_client

ESTABLECIMIENTOS = ("1", "8", "15")
TABLE_NAME = "anomalias_diasurtir"
BATCH_SIZE = 500


def get_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        print(f"ERROR: falta la variable de entorno {name}", file=sys.stderr)
        sys.exit(1)
    return value


def fetch_from_sqlserver() -> list[dict]:
    conn = pymssql.connect(
        server=get_env("SQLSERVER_HOST"),
        port=get_env("SQLSERVER_PORT"),
        user=get_env("SQLSERVER_USER"),
        password=get_env("SQLSERVER_PASS"),
        database="bms",
        login_timeout=15,
        as_dict=True,
    )
    try:
        cursor = conn.cursor()
        placeholders = ",".join(["%s"] * len(ESTABLECIMIENTOS))
        query = f"""
            SELECT * FROM bms.dbo.Anomalias_DiaSurtir
            WHERE Establecimiento IN ({placeholders})
        """
        cursor.execute(query, ESTABLECIMIENTOS)
        rows = cursor.fetchall()
        print(f"Filas obtenidas de SQL Server: {len(rows)}")
        return rows
    finally:
        conn.close()


def normalize_row(row: dict) -> dict:
    """Convierte llaves a minúsculas y tipos de fecha a string ISO
    (el cliente de Supabase serializa a JSON, y datetime/date no son
    serializables directamente)."""
    normalized = {}
    for key, value in row.items():
        col = key.lower()
        if isinstance(value, (datetime, date)):
            normalized[col] = value.isoformat()
        elif isinstance(value, Decimal):
            normalized[col] = float(value)
        else:
            normalized[col] = value
    return normalized


def upload_to_supabase(rows: list[dict]) -> None:
    if not rows:
        print("No hay filas para subir.")
        return

    supabase = create_client(get_env("SUPABASE_URL"), get_env("SUPABASE_SERVICE_KEY"))
    normalized = [normalize_row(r) for r in rows]

    total = 0
    for i in range(0, len(normalized), BATCH_SIZE):
        batch = normalized[i : i + BATCH_SIZE]
        supabase.table(TABLE_NAME).upsert(batch, on_conflict="id").execute()
        total += len(batch)
        print(f"  Subidas {total}/{len(normalized)} filas...")

    print(f"Listo. {total} filas sincronizadas en '{TABLE_NAME}'.")


def main() -> None:
    rows = fetch_from_sqlserver()
    upload_to_supabase(rows)


if __name__ == "__main__":
    main()
