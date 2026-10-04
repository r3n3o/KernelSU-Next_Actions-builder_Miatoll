# 📚 Documentation & Publication Templates (/.docs/)

Este directorio contiene las plantillas oficiales de publicación, guías y recursos de documentación para el kernel **NetHunter & KernelSU-Next** en la plataforma Xiaomi SM6250 (Miatoll).

---

## 🗂️ Índice de Documentos

| Archivo | Formato | Propósito / Destino |
| :--- | :--- | :--- |
| **[GITHUB_RELEASE_NOTES.md](./GITHUB_RELEASE_NOTES.md)** | Markdown | Plantilla completa para publicar un nuevo **Release en GitHub** (Tag: 3.4.0-A16-STABLE). Incluye changelog, advertencias de responsabilidad, guía paso a paso y capturas. |
| **[XDA_THREAD_TEMPLATE.md](./XDA_THREAD_TEMPLATE.md)** | XDA BBCode | Plantilla formateada con BBCode nativo (insignias, tablas, spoilers colapsables y capturas) lista para crear el hilo oficial en **XDA Developers** (*Xiaomi Redmi Note 9 Pro / Miatoll ROMs, Kernels, & Mods*). |

---

## 📱 Especificaciones de la Versión Actual

* **Kernel Version**: Linux `4.14.357-openela`
* **KernelSU-Next Engine**: `v3.4.0` (Build `33294` / UAPI `4`)
* **Manager APK Compatible**: KernelSU-Next Manager `v3.4.0` (`33294-4`) o superior
* **ROM de Referencia Validada**: **crDroid 16.0 Vanilla Edition** (Android 16 / SDK 36, sin GApps)
* **Dispositivo Probado en Hardware**: **Xiaomi Redmi Note 9 Pro (`joyeuse`)**
* **Árbol Unificado Compatible**: `joyeuse`, `curtana`, `gram`, `excalibur`

---

## 🔧 Notas de Integración Técnica

### Arquitectura KernelSU-Next v3.4.0 (No-GKI / SM6250)

| Componente | Ubicación | Método de Integración |
| :--- | :--- | :--- |
| Driver Core | `drivers/kernelsu/` (symlink → `KernelSU-Next/kernel/`) | `setup.sh` de **KernelSU-Next** (NO el de `tiann/KernelSU`) |
| VFS Hooks | `fs/exec.c`, `fs/open.c`, `fs/stat.c`, etc. | Inyección manual vía `patch_kernel.py` |
| Supercall (prctl) | `drivers/kernelsu/supercall/dispatch.c` | Nativo en KernelSU-Next v3.4.0 |
| APK Signing | `drivers/kernelsu/manager/apk_sign.c` | Patched por `patch_kernel.py` |
| ksud daemon | `ksud-aarch64-linux-android` (release oficial) | Descargado en GitHub Actions |

### ⚠️ Cambio Crítico vs. Versión Anterior

> **Problema raíz del error "Error al conceder root"**: El Manager de KernelSU-Next v3.4.0
> rechazaba la conexión del kernel porque el driver embebido antiguo (v0.9.5) reportaba una
> versión de API y un comportamiento incompatibles (UAPI v2 vs v4).
>
> **Corrección aplicada**: Se ha implementado un puente de compatibilidad (spoofing) directo
> en el Kernel. El driver emula ser la versión 33294 (v3.4.0), implementa el wrapper UAPI v4 (`supercall`),
> gestiona correctamente el handshake mágico (`0xdeadbeef`) en `sys_reboot`, e intercepta
> la detección del APK Manager (`com.rifsxd.ksunext`) a nivel de VFS. Todo esto desactivando
> el demonio incrustado original para permitir que el nuevo `ksud` tome el control total.

---

## ✍️ Créditos

* **Lead Developer**: r3n3o
* **Co-Developer**: Antigravity (Google DeepMind)
