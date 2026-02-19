# BaleSupply

Sistema web MVC (PHP + MySQL) para gestionar solicitudes de pacas por tráiler entre roles `buyer`, `vendor`, `admin` y `viewer`, con trazabilidad en `request_events` y `audit_logs`.

## Funcionalidad implementada
- Autenticación por sesión (login/logout) con CSRF.
- Control de acceso por rol (middleware RBAC).
- P1: Buyer crea solicitudes.
- P2: Vendor confirma cantidad.
- P3: Admin aprueba o rechaza.
- P4: Todos los roles actualizan su perfil.
- P5: Búsqueda en solicitudes y usuarios (usuarios solo admin).
- Dashboard con métricas básicas y actividad reciente.
- Bitácora de auditoría (`audit_logs`) y eventos por solicitud (`request_events`).

## Estructura del repositorio
- `app/`
  - `Controllers/` lógica de rutas
  - `Core/` router, DB, auth, view, helpers
  - `Middleware/` auth/guest/role
  - `Models/` acceso a datos
  - `Views/` plantillas
- `config/` configuración app/db
- `public/` entrada web y assets
- `routes/` rutas HTTP
- `database/migrations/` esquema SQL
- `database/seeds/` datos demo
- `storage/` logs/cache/sessions
- `kanban/` script para crear issues en GitHub
- `docs/` documentación de flujo

## Requisitos locales
- MAMP (Apache + MySQL + PHP)
- MySQL con acceso a `root`

## Instalación local (MAMP)
1. Coloca el proyecto en:
   `/Applications/MAMP/htdocs/BaleSupply`
2. Crea el archivo `.env` desde el ejemplo:
   ```bash
   cp .env.example .env
   ```
3. Crea la DB y tablas ejecutando:
   - `database/migrations/001_init.sql`
   - `database/seeds/001_seed.sql`
4. Ajusta credenciales en `.env` si tu MySQL usa otra contraseña.
5. Entra en el navegador:
   `http://localhost/BaleSupply/public/`

## Usuarios demo
Todos usan contraseña: `password`
- admin: `admin@balesupply.local`
- vendor: `vendor@balesupply.local`
- buyer: `buyer@balesupply.local`
- viewer: `viewer@balesupply.local`

## Flujo de uso sugerido
1. Inicia sesión como `buyer`, crea solicitud.
2. Inicia sesión como `vendor`, confirma cantidad.
3. Inicia sesión como `admin`, aprueba/rechaza.
4. Revisa historial en detalle de solicitud y `Audit Logs`.

## Notas
- El punto de entrada es `public/index.php`.
- `APP_BASE_PATH` está configurado para MAMP en `.env.example`.

## Licencia
MIT (ver `LICENSE`).
