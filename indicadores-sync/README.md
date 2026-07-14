# Sincronización de indicadores → Supabase

Sube automáticamente datos del SQL Server del cliente a Supabase. Pensado para
crecer: cada indicador nuevo se agrega como un script + un workflow más,
reutilizando las mismas credenciales.

```
indicadores-sync/
├── requirements.txt
├── scripts/
│   └── sync_anomalias.py          <- un script por indicador
├── sql/
│   └── create_table_anomalias.sql <- un SQL por indicador (solo se corre una vez)
└── .github/workflows/
    └── sync_anomalias.yml         <- un workflow por indicador (define hora/frecuencia)
```

## Primera vez: subir esto a GitHub

### 1. Crea una cuenta en GitHub (si no tienes)
https://github.com → registro gratis.

### 2. Crea un repositorio nuevo
- "New repository"
- Nombre: indicadores-sync
- Marca "Private"
- "Create repository"

### 3. Sube la carpeta completa
En el repo vacío, clic en "uploading an existing file", y arrastra la carpeta
`indicadores-sync` completa (incluye la carpeta oculta `.github`). "Commit changes".

### 4. Agrega los secrets (una sola vez, sirven para todos los indicadores)
Settings → Secrets and variables → Actions → New repository secret:

| Nombre | Valor |
|---|---|
| SQLSERVER_HOST | 170.247.128.23 |
| SQLSERVER_PORT | 50001 |
| SQLSERVER_USER | c0n1fokus |
| SQLSERVER_PASS | ICO10030 |
| SUPABASE_URL | https://jiqykcjgkpkojnbhlwxo.supabase.co |
| SUPABASE_SERVICE_KEY | (la key larga que empieza con eyJ...) |

### 5. Crea la tabla en Supabase
SQL Editor de Supabase → pega y corre `sql/create_table_anomalias.sql`.

### 6. Prueba manual
Pestaña "Actions" → "Sync Anomalias a Supabase" → "Run workflow".
Palomita verde ✅ = listo. Corre solo todos los días a las 9am (hora Pacífico).

---

## Cómo agregar un indicador nuevo (después de este)

Cuando tengas el siguiente query y tabla, dime y te preparo estos 3 archivos
listos para copiar-pegar:

1. `scripts/sync_<indicador>.py` — mismo patrón que `sync_anomalias.py`,
   cambia el query y el nombre de la tabla destino.
2. `sql/create_table_<indicador>.sql` — la tabla nueva en Supabase (la corres
   una sola vez en el SQL Editor).
3. `.github/workflows/sync_<indicador>.yml` — copia de
   `sync_anomalias.yml`, cambiando el nombre y, si quieres, la hora/frecuencia
   (el cron es independiente por indicador).

No hace falta tocar secrets ni nada más — todos los workflows reutilizan las
mismas 6 credenciales que ya configuraste. Solo subes los 3 archivos nuevos a
las carpetas correspondientes en el mismo repo (GitHub te deja arrastrar
archivos sueltos a una carpeta existente igual que la primera vez).
