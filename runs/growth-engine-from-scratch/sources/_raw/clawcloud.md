# Repo: clawcloud

## README.md
```markdown
# clawcloud
claw on cloud

```

## .cursor/skills/clawcloud-azure-desktop-gallery-pipeline/SKILL.md
```markdown
---
name: clawcloud-azure-desktop-gallery-pipeline
description: Deploy and troubleshoot the ClawCloud Azure desktop runtime built on Ubuntu, KasmVNC, OpenClaw, Compute Gallery, builder VMs, and flexible VMSS. Use when creating or updating the Azure image pipeline, fixing VMSS desktop reachability, wiring OpenClaw gateway access, or reproducing the ClawCloud cloud desktop environment.
---

# ClawCloud Azure Desktop Gallery Pipeline

## Use This Skill When

- Working on `infra/azure/` scripts.
- Publishing a new gallery image for the cloud desktop runtime.
- Creating or repairing the builder VM or flexible VMSS.
- Fixing KasmVNC reachability, iframe embedding, or OpenClaw gateway exposure.
- Wiring backend control plane startup to Azure desktop instances.

## Source Of Truth

- `infra/azure/create_base_resources.sh`
- `infra/azure/create_gallery_image.sh`
- `infra/azure/install_desktop_runtime.sh`
- `infra/azure/create_builder_vm.sh`
- `infra/azure/create_vmss.sh`
- `backend/core/azure_vmss_provider.py`
- `backend/core/control_plane_service.py`

## Current Runtime Shape

- Base network is a single VNet + subnet with a shared NSG.
- Image is published through Azure Compute Gallery.
- A low-spec builder VM is kept for debugging.
- User-facing cloud desktops run on a flexible VMSS.
- Desktop transport is KasmVNC on `8444`.
- OpenClaw gateway is exposed on `18789`.
- Backend issues machine start/stop and desktop session requests, then talks directly to Azure and the remote OpenClaw gateway.

## Default Workflow

1. Verify Azure login and subscription context first.
2. Create or update base resources with `create_base_resources.sh`.
3. Build or refresh the gallery image with `create_gallery_image.sh`.
4. Keep one builder VM available for debugging with `create_builder_vm.sh`.
5. Create or update the flexible VMSS with `create_vmss.sh`.
6. Verify ports:
   - `22`
   - `8444`
   - `18789`
7. Verify runtime health:
   - `https://<ip>:8444`
   - `http://<ip>:18789/health`
8. If embedding the desktop in the frontend, confirm KasmVNC is running with `-disableBasicAuth`.

## Required Deployment Rules

- Prefer project scripts over ad hoc Azure commands.
- Reuse the project NSG instead of letting Azure auto-create NIC NSGs.
- Resolve gallery image version `latest` to the actual latest version name before VM or VMSS creation.
- Keep the builder VM separate from the image-build VM lifecycle.
- Use LF line endings for scripts uploaded to Linux.
- Treat `8444` and `18789` as first-class deployment ports, not optional debug ports.

## Windows Execution Guidance

- On Windows, prefer `powershell.exe -NoProfile -Command "& 'C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd' ..."` for Azure CLI automation.
- Avoid mixing Git Bash quoting rules with long `az.cmd` command lines.
- If a backend or script needs Azure CLI from Python, call the executable directly with argument arrays instead of shell-joined strings.
- For SSH and SCP on Windows, rely on executable argument arrays and explicit key paths.

## KasmVNC Rules

- `claw-kasmvnc.service` must start KasmVNC with `-disableBasicAuth` for iframe embedding in the workbench.
- A `401 Unauthorized` on `8444` means basic auth is still enabled and the right-side desktop pane will not embed cleanly.
- After patching the service unit, run:
  - `systemctl daemon-reload`
  - `systemctl restart claw-kasmvnc.service`
- For quick verification, external reachability matters more than local process state.

## OpenClaw Rules

- Gateway default port is `18789`.
- Remote runtime config must enable HTTP responses and chat completions endpoints.
- Backend startup should inject runtime config and env files into `/home/claw/.openclaw/`.
- Backend task dispatch should use the remote gateway only after `/health` is reachable.
- If the desktop is ready but the gateway is not, machine state should not become fully ready.

## Troubleshooting Checklist

- Gallery version stuck in `Creating`:
  - Check Azure activity log.
  - Confirm source managed image succeeded.
  - Continue with the managed image if gallery replication is the only blocker.
- VM or VMSS has public IP but `8444` times out:
  - Check subnet NSG.
  - Check NIC-level auto-created NSG.
  - Confirm the instance inherited or attached the intended NSG.
- `8444` returns `401`:
  - KasmVNC basic auth is still active.
- `18789` is unreachable:
  - NSG rule is missing, or OpenClaw gateway is not healthy.
- Backend can start the machine but chat still behaves like mock:
  - Confirm `CLOUD_MACHINE_PROVIDER=azure_vmss`.
  - Confirm the remote runtime config was pushed successfully.
  - Confirm `/v1/responses` is enabled on the gateway.
- Bash command works badly with Azure CLI on Windows:
  - Move the command to PowerShell or Python subprocess arrays.

## Known Pitfalls To Remember

- CRLF line endings break remote shell execution on Linux.
- `create_vmss.sh` needs real gallery version resolution and should not rely on `"latest"` as a literal version name.
- Omitting `--nsg` often leads Azure to create a fresh NIC NSG that only exposes SSH.
- KasmVNC package selection is tied to Ubuntu Jammy package naming.
- Gallery image generation must stay aligned with Hyper-V generation V2.
- Public desktop access and remote gateway access are separate concerns; opening `8444` does not make the gateway reachable.

## Validation Commands

```bash
curl -k -I https://<desktop-ip>:8444
curl http://<desktop-ip>:18789/health
```

```bash
az vm list -g <resource-group> -d -o table
az network nsg rule list -g <resource-group> --nsg-name <nsg-name> -o table
```

## When Updating This Skill

- Keep it aligned with the current scripts and provider implementation.
- Add newly discovered Azure or KasmVNC pitfalls here instead of scattering them across chat history.
- Prefer small, durable rules over long narrative notes.

```
