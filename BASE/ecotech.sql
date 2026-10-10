CREATE DATABASE IF NOT EXISTS ecotech_db CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci;
USE ecotech_db;

CREATE TABLE IF NOT EXISTS empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    salario DECIMAL(10, 2) NOT NULL,
    rol VARCHAR(50) NOT NULL DEFAULT 'Empleado'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

CREATE TABLE IF NOT EXISTS proyectos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    fecha_inicio DATE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

CREATE TABLE IF NOT EXISTS registros_tiempo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    horas DECIMAL(5, 2) NOT NULL,
    descripcion_tarea VARCHAR(255) NOT NULL,
    fecha DATE NOT NULL,
    empleado_id INT NOT NULL,
    proyecto_id INT NOT NULL,
    CONSTRAINT fk_registro_empleado FOREIGN KEY (empleado_id) 
        REFERENCES empleados(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_registro_proyecto FOREIGN KEY (proyecto_id) 
        REFERENCES proyectos(id) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

INSERT INTO empleados (nombre, email, telefono, salario, rol) VALUES
('Ana Silva', 'ana.silva@ecotech.cl', '+56911111111', 1400000.00, 'Empleado'),
('Carlos Ruiz', 'carlos.ruiz@ecotech.cl', '+56922222222', 2200000.00, 'Gerente'),
('Beatriz Soto', 'beatriz.soto@ecotech.cl', '+56933333333', 1200000.00, 'Empleado');

INSERT INTO proyectos (nombre, descripcion, fecha_inicio) VALUES
('Parque Solar Atacama', 'Instalación de paneles solares fotovoltaicos', '2026-03-01'),
('Gestión Hídrica Central', 'Monitoreo de consumo de agua residual', '2026-04-15'),
('Auditoría Energética', 'Revisión de consumo en plantas industriales', '2026-05-10');

INSERT INTO registros_tiempo (horas, descripcion_tarea, fecha, empleado_id, proyecto_id) VALUES
(5.0, 'Diseño de circuitos eléctricos', '2026-04-01', 1, 1),
(8.0, 'Reunión de coordinación y presupuesto', '2026-04-02', 2, 1),
(4.5, 'Toma de muestras de caudal', '2026-04-05', 3, 2);
