create database if not exists ecotech_db character set utf8mb4 collate utf8mb4_spanish_ci;
use ecotech_db;

create table if not exists empleados (
    id int auto_increment primary key,
    nombre varchar(100) not null,
    email varchar(100) not null,
    telefono varchar(20) not null,
    salario decimal(10, 2) not null,
    rol varchar(50) not null default 'Empleado',
    departamento_id int null
) engine=innodb default charset=utf8mb4 collate=utf8mb4_spanish_ci;

create table if not exists departamentos (
    id int auto_increment primary key,
    nombre varchar(100) not null unique,
    descripcion varchar(255),
    gerente_id int null,
    constraint fk_depto_gerente foreign key (gerente_id)
        references empleados(id) on update cascade on delete set null
) engine=innodb default charset=utf8mb4 collate=utf8mb4_spanish_ci;

alter table empleados
    add constraint fk_emp_departamento foreign key (departamento_id)
        references departamentos(id) on update cascade on delete set null;

create table if not exists proyectos (
    id int auto_increment primary key,
    nombre varchar(100) not null,
    descripcion varchar(255) not null,
    fecha_inicio date not null
) engine=innodb default charset=utf8mb4 collate=utf8mb4_spanish_ci;

create table if not exists proyecto_empleados (
    proyecto_id int not null,
    empleado_id int not null,
    fecha_asignacion date not null,
    primary key (proyecto_id, empleado_id),
    constraint fk_pe_proyecto foreign key (proyecto_id)
        references proyectos(id) on update cascade on delete cascade,
    constraint fk_pe_empleado foreign key (empleado_id)
        references empleados(id) on update cascade on delete cascade
) engine=innodb default charset=utf8mb4 collate=utf8mb4_spanish_ci;

create table if not exists registros_tiempo (
    id int auto_increment primary key,
    horas decimal(5, 2) not null,
    descripcion_tarea varchar(255) not null,
    fecha date not null,
    empleado_id int not null,
    proyecto_id int not null,
    constraint fk_registro_empleado foreign key (empleado_id)
        references empleados(id) on update cascade on delete restrict,
    constraint fk_registro_proyecto foreign key (proyecto_id)
        references proyectos(id) on update cascade on delete restrict
) engine=innodb default charset=utf8mb4 collate=utf8mb4_spanish_ci;

insert into empleados (nombre, email, telefono, salario, rol) values
('Ana Silva', 'ana.silva@ecotech.cl', '+56911111111', 1400000.00, 'Empleado'),
('Carlos Ruiz', 'carlos.ruiz@ecotech.cl', '+56922222222', 2200000.00, 'Gerente'),
('Beatriz Soto', 'beatriz.soto@ecotech.cl', '+56933333333', 1200000.00, 'Empleado');

insert into departamentos (nombre, descripcion, gerente_id) values
('Ingenieria', 'Desarrollo y proyectos tecnicos', 2),
('Medio Ambiente', 'Sustentabilidad y monitoreo ambiental', 2);

update empleados set departamento_id = 1 where id in (1, 2);
update empleados set departamento_id = 2 where id = 3;

insert into proyectos (nombre, descripcion, fecha_inicio) values
('Parque Solar Atacama', 'Instalacion de paneles solares fotovoltaicos', '2026-03-01'),
('Gestion Hidrica Central', 'Monitoreo de consumo de agua residual', '2026-04-15'),
('Auditoria Energetica', 'Revision de consumo en plantas industriales', '2026-05-10');

insert into proyecto_empleados (proyecto_id, empleado_id, fecha_asignacion) values
(1, 1, '2026-03-05'),
(1, 2, '2026-03-05'),
(2, 3, '2026-04-20');

insert into registros_tiempo (horas, descripcion_tarea, fecha, empleado_id, proyecto_id) values
(5.0, 'Diseno de circuitos electricos', '2026-04-01', 1, 1),
(8.0, 'Reunion de coordinacion y presupuesto', '2026-04-02', 2, 1),
(4.5, 'Toma de muestras de caudal', '2026-04-05', 3, 2);
