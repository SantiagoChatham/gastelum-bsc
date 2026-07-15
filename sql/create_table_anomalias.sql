-- Ejecuta esto UNA VEZ en Supabase Dashboard → SQL Editor
-- Crea la tabla destino equivalente a bms.dbo.Anomalias_DiaSurtir
-- (Ya la creaste antes, este archivo es solo de respaldo/referencia)

create table if not exists anomalias_diasurtir (
  id               bigint primary key,
  fecha_insercion  date,
  folio            text,
  obra             text,
  nombre           text,
  fecha            timestamp,
  tipo_atencion    text,
  notas            text,
  transaccion      text,
  usuariocaptura   text,
  surtidor         text,
  notas_pendiente  text,
  importe          numeric(14,2),
  anomalia         text,
  fecha_anomalia   timestamp,
  notas_anomalia   text,
  establecimiento  integer,
  synced_at        timestamptz default now()
);

create index if not exists idx_anomalias_establecimiento
  on anomalias_diasurtir (establecimiento);

alter table anomalias_diasurtir enable row level security;
