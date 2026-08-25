# GitHub README Setup Guide

## 1. Copy the files

Place these files in the root of your MIG repository:

```text
README.md
assets/
docs/
```

The image paths in the README are already relative, so they will render automatically on GitHub if the folder structure is preserved.

## 2. Keep the EDA image folder exactly here

```text
assets/eda/
```

The package contains the 13 charts extracted from the supplied EDA document and renamed clearly.

## 3. Add the final dashboard screenshot later

For an even stronger GitHub landing page, add your cleanest Control Tower screenshot to:

```text
assets/dashboard/
```

A strong placement is immediately after the opening badges and before the Executive Summary.

Suggested Markdown:

```html
<p align="center">
  <img src="assets/dashboard/control_tower_overview.png" width="100%" alt="MIG Cement Intelligence and Inventory Control Tower">
</p>
```

## 4. Add live links once final

After deployment, add two compact links near the top:

```markdown
[Open Live Control Tower](YOUR_DEPLOYED_APP_LINK) · [View Methodology](docs/EDA_BUSINESS_FINDINGS.md)
```

## 5. Replace targets with achieved results only when validated

The README deliberately labels the following as project targets:

- MAPE ≤ 15%
- ≥ 98% pour readiness
- 20% inventory utilisation improvement
- 30% material write-off reduction

Do not convert these into claimed results until the final evaluation supports them.

## 6. Final portfolio polish

Before publishing:

- add one strong dashboard screenshot
- insert the final winning model and validated test metrics
- add the deployed app URL
- verify all repository paths
- keep only the most decision-relevant charts in the main README
- leave the full EDA in `docs/EDA_BUSINESS_FINDINGS.md`
