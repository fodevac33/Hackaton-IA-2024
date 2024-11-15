-- 001_create_tables.sql

-- Create 'clientes' table
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    cc TEXT NOT NULL,
    telefono TEXT,
    email TEXT,
    monto_deuda REAL,
    fecha_vencimiento DATE,
    estado_cuenta TEXT CHECK(estado_cuenta IN ('Pendiente', 'En mora', 'Pagada')),
    historial_pagos TEXT
);

-- Create 'chats' table
CREATE TABLE IF NOT EXISTS mensajes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    enviado_por TEXT CHECK(enviado_por IN ('user', 'assistant')),
    mensaje TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES clientes (id)
);
