-- 002_insert_sample_data.sql

-- Insert sample data into 'clientes' table
INSERT INTO clientes (id, nombre, fecha_nacimiento, cc, telefono, email, monto_deuda, fecha_vencimiento, estado_cuenta, historial_pagos)
VALUES
(1, 'Juan Pérez', '1980-05-15', '1234567890', '555-1010', 'juan.perez@example.com', 750.0, '2024-12-15', 'Pendiente', '2023-11-01:150,2023-10-15:100'),
(2, 'María López', '1992-08-25', '0987654321', '555-2020', 'maria.lopez@example.com', 1200.0, '2024-11-30', 'En mora', '2023-11-10:200,2023-09-20:300'),
(3, 'Carlos García', '1975-02-10', '1122334455', '555-3030', 'carlos.garcia@example.com', 0.0, '2023-10-01', 'Pagada', '2023-09-15:400,2023-08-15:600');

