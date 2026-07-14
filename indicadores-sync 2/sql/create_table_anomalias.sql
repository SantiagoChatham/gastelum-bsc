-- Ejecuta esto UNA VEZ en Supabase Dashboard → SQL Editor
-- Crea la tabla destino equivalente a bms.dbo.Anomalias_DiaSurtir

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

-- Índice útil si vas a filtrar seguido por establecimiento
create index if not exists idx_anomalias_establecimiento
  on anomalias_diasurtir (establecimiento);

-- RLS activado sin políticas: la tabla queda cerrada para anon/authenticated.
-- El script de sincronización usa la service_role key, que siempre se salta RLS,
-- así que esto no le afecta — solo evita exponer los datos por accidente
-- si algún día usas la anon key en una app cliente.
alter table anomalias_diasurtir enable row level security;
