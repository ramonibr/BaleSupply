#!/usr/bin/env python3
import argparse, csv, sys, subprocess

def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        if p.stdout.strip():
            print(p.stdout.strip())
        if p.stderr.strip():
            print(p.stderr.strip(), file=sys.stderr)
        raise SystemExit(p.returncode)
    return p.stdout.strip()

def normalize_labels(s):
    s = (s or "").strip()
    if not s:
        return []
    out = []
    for x in s.split(","):
        x = x.strip()
        if x and x not in out:
            out.append(x)
    return out

def infer_dfd(title, labels):
    t = (title or "").lower()
    if "p1" in t or "crear solicitud" in t:
        return "P1 Crear Solicitud"
    if "p2" in t or "vendor confirma" in t or "confirma cantidad" in t:
        return "P2 Vendor Confirma Cantidad"
    if "p3" in t or "aprueba" in t or "rechaza" in t:
        return "P3 Admin Aprueba/Rechaza"
    if "p4" in t or "perfil" in t or "actualizar perfil" in t:
        return "P4 Actualizar Perfil"
    if "p5" in t or "búsqueda" in t or "busqueda" in t or "search" in t:
        return "P5 Búsqueda en el sitio"
    if "requests" in labels or "solicitud" in t:
        return "P1/P2/P3 (Solicitudes)"
    return "N/A (fuera del DFD)"

def infer_role(title, labels):
    labs = set(labels)
    tl = (title or "").lower()
    if "admin" in labs or "admin" in tl:
        return "admin"
    if "vendor" in labs or "vendor" in tl:
        return "vendor"
    if "buyer" in labs or "buyer" in tl:
        return "buyer"
    if "viewer" in labs or "viewer" in tl:
        return "viewer"
    return "N/A"

def kind_from_labels(labels):
    labs = set(labels)
    if "bug" in labs:
        return "bug"
    if "db" in labs:
        return "db"
    if "docs" in labs:
        return "docs"
    return "feature"

def ensure_primary_label(labels, kind):
    labs = list(labels)
    if kind not in labs:
        labs.insert(0, kind)
    return labs

def body_feature(desc, dfd, role):
    return f"""## Resumen corto
{desc}

## Proceso DFD relacionado
{dfd}

## Rol principal
{role}

## Historia de usuario
Como {role} quiero ______ para ______.

## Criterios de aceptación
- [ ] Validación server-side aplicada
- [ ] Control de acceso por rol verificado
- [ ] Se registra en audit_logs cuando corresponde
- [ ] UI/flujo probado en local

## UI / Mockup (si aplica)
Link o captura: ______

## Impacto en DB (si aplica)
Tablas/acciones: ______

## Definition of Done
- [ ] Funciona según criterios
- [ ] Sin accesos indebidos por rol
- [ ] Evidencia/captura si aplica
"""

def body_docs(desc):
    return f"""## Entregable / Documento
{desc}

## Qué se va a agregar o actualizar
- ______

## Ubicación en el repositorio
- ______ (ej. docs/dfd/, docs/mockups/, README.md)

## Checklist
- [ ] Link o captura verificable incluida
- [ ] Formato y subtítulos correctos
"""

def body_db(desc):
    return f"""## Objetivo del cambio
{desc}

## Tablas/objetos afectados
- users
- requests
- request_events
- audit_logs

## Migración / Script
- Archivo: ______
- Pasos: ______

## Rollback
- ______
"""

def body_bug(desc):
    return f"""## Resumen del bug
{desc}

## Pasos para reproducir
1. ______
2. ______
3. ______

## Comportamiento esperado
______

## Comportamiento actual
______

## Logs / Capturas
______

## Entorno
- Local (MAMP) / Staging / Producción: ______
"""

def build_body(kind, desc, dfd, role):
    if kind == "docs":
        return body_docs(desc)
    if kind == "db":
        return body_db(desc)
    if kind == "bug":
        return body_bug(desc)
    return body_feature(desc, dfd, role)

def gh_repo_from_cwd():
    return run(["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="", help="OWNER/REPO")
    ap.add_argument("--seed", default="kanban/issues_seed.csv")
    ap.add_argument("--project", default="BaleSupply")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    repo = args.repo.strip() or gh_repo_from_cwd()

    rows = []
    with open(args.seed, "r", encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if (r.get("title") or "").strip():
                rows.append(r)

    if args.limit and args.limit > 0:
        rows = rows[:args.limit]

    for r in rows:
        title = r["title"].strip()
        desc = (r.get("body") or "").strip()
        labels = normalize_labels(r.get("labels") or "")
        milestone = (r.get("milestone") or "").strip()

        kind = kind_from_labels(labels)
        labels = ensure_primary_label(labels, kind)

        dfd = infer_dfd(title, labels)
        role = infer_role(title, labels)
        body = build_body(kind, desc, dfd, role)

        cmd = ["gh", "issue", "create", "--repo", repo, "--title", title, "--body", body]
        if labels:
            cmd += ["--label", ",".join(labels)]
        if milestone:
            cmd += ["--milestone", milestone]
        if args.project.strip():
            cmd += ["--project", args.project.strip()]

        if args.dry_run:
            print("DRY:", " ".join(cmd))
        else:
            run(cmd)

    print(f"OK: created {len(rows)} issues in {repo}")

if __name__ == "__main__":
    main()
