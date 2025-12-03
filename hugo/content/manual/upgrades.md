+++
title = "Upgrades"
weight = 70
chapter = false
+++

## Purpose
Collect upgrade notes and migration checklists for major versions.

## v10 → v11 highlights
- CSP-PC mode added (centralized position loop in CSP)
- Position-velocity-time (profile move) support
- Motor record PID fields still limited to 0..1.0 range; use values 100× smaller than native ecmc settings

### Migration checklist
- Auto-enable: move from motor record parameters to `axis.autoEnable` in YAML
- Master/slave synchronization: replace PLC state machines with native `addMasterSlaveSM.cmd`
- Limit logic: use `plcOverride` on limits and set `ax<id>.mon.*lim` in PLC code
- Drive safety: ensure SDO verification is run for every used channel (especially on multi-channel drives)

### Removed/changed
- `getAxisStatusStructV2` removed; rebuild plugins that depended on it
- Event*/CommandList*/DataRecorder* removed; replace with PLC logic
- Motor record `MtnCmd` mbbo indices updated; use string writes or adjust indices per new template
