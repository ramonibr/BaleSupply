# BaleSupply

Sistema web para control de tráileres con pacas y gestión de solicitudes entre Buyer/Vendor, con aprobaciones de Admin y bitácora (audit log) de movimientos.

## Índice
1. Propuesta
2. Stack tecnológico
3. Roles
4. Procesos (DFD P1–P5)
5. Arquitectura y patrones de diseño
6. Estructura del repositorio
7. Instalación local (MAMP)
8. Base de datos (MySQL)
9. Flujo de Git (main/develop)
10. Licencia
11. Evidencias (GitHub)

---

## 1) Propuesta
BaleSupply centraliza:
- Solicitudes de compra/venta de pacas por tráiler.
- Confirmación de cantidad por Vendor.
- Aprobación/Rechazo por Admin.
- Actualización de perfil por cualquier rol.
- Búsqueda en el sitio (por solicitudes y usuarios).
- Registro de acciones (audit log) para trazabilidad.

---

## 2) Stack tecnológico
- Backend: PHP (MVC)
- Frontend: HTML + CSS + JavaScript (jQuery)
- Base de datos: MySQL
- Hosting/producción: BLUEHOST (Apache + PHP)
- Control de versiones: GitHub (repo público)

---

## 3) Roles
- Admin: gestiona usuarios, aprueba/rechaza solicitudes, consulta logs/estadísticas.
- Vendor: confirma cantidad para solicitudes asignadas, edita su perfil, busca.
- Buyer: crea solicitudes, edita su perfil, busca.
- Viewer: solo lectura (consultas), busca.

---

## 4) Procesos (DFD P1–P5)
DFD base (Mermaid):

```mermaid
flowchart TD
  %% ============ Actores ============
  B[Buyer] 
  V[Vendor]
  A[Admin]

  %% ============ Procesos ============
  P1((P1: Crear Solicitud))
  P2((P2: Vendor Confirma Cantidad))
  P3((P3: Admin Aprueba/Rechaza))
  P4((P4: Actualizar Perfil))
  P5((P5: Busqueda en el sitio))

  %% ============ Almacenes de datos ============
  DBU[(users)]
  DBR[(requests)]
  DBE[(request_events)]
  DBA[(audit_logs)]

  %% ============ Flujos ============
  B -->|Solicitud| P1
  P1 -->|INSERT| DBR
  P1 -->|INSERT| DBE
  P1 -->|INSERT log| DBA

  V -->|Confirmar| P2
  P2 -->|UPDATE| DBR
  P2 -->|INSERT evento| DBE
  P2 -->|INSERT log| DBA

  A -->|Aprobar/Rechazar| P3
  P3 -->|UPDATE| DBR
  P3 -->|INSERT evento| DBE
  P3 -->|INSERT log| DBA

  B -->|Editar perfil| P4
  V -->|Editar perfil| P4
  A -->|Editar perfil| P4
  P4 -->|UPDATE| DBU
  P4 -->|INSERT log| DBA
  
  B -->|Buscar| P5
  V -->|Buscar| P5
  A -->|Buscar| P5
  P5 -->|SELECT| DBR
  P5 -->|SELECT| DBU
  P5 -->|INSERT log| DBA
