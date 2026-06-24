# Paper Figures

All images for the SSRN paper are in this folder.

| File | Use in paper |
|------|----------------|
| `fig1_system_architecture.png` | Figure 1 — System architecture (Section 4) |
| `fig2_ml_workflow.png` | Figure 2 — ML workflow (Section 4) |
| `fig3_dashboard.png` | Figure 3 — Dashboard demo (Section 5) |
| `fig4_analyze_result.png` | Figure 4 — Transaction analyser (Section 5) |
| `fig4_analyze_form.png` | Optional — form before scoring |
| `fig5_policy_page.png` | Figure 5 — Policy module (Section 8) |

**View in paper:** Open `docs/SSRN_PAPER.md` — figures render in GitHub and in PDF exports.

**Export PDF with images:**
```bash
cd docs
pandoc SSRN_PAPER.md -o SSRN_PAPER.pdf --resource-path=.
```
