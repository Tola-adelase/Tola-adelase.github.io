# Adetola Adelase — personal portfolio

[Live portfolio](https://tola-adelase.github.io/) · [Football Match Lab](https://tola-adelase.github.io/football-match-lab.html)

Personal and academic Data Science projects, professional background, football and writing. Employer data and private work projects are not published here.

## Run locally

Python 3.9+; no build step or Node packages:

```bash
python3 -m http.server 8765
```

Open <http://localhost:8765/>. The demo uses bundled analytical summaries; no API keys or live calls are needed.

## Rebuild Match Lab

```bash
python3 scripts/build_match_lab.py
python3 -m unittest discover -s tests -v
```

The standard-library script downloads two pinned source files into a local `research/` cache if absent and writes `data/match-lab.js`. It records SHA-256 hashes and upstream revision `4b73468fc5b0f1950f9f66fada70ad3a4f9327cb`. The source-to-summary checks reconcile 30 shots and six goals in match 3869685, exclude shootouts and verify per-player period totals. Raw event and lineup files must not be committed or redistributed. Published files contain analytical summaries only.

Data: [StatsBomb Open Data](https://github.com/hudl/open-data). Personal, non-commercial analytical use under [upstream terms](https://github.com/hudl/open-data/blob/master/LICENSE.pdf), with source credit and logo. Interpretations are independent and not endorsed by StatsBomb. It is descriptive analysis of one match, not a prediction model or player ranking. No adjustment is made for minutes, role or possession. xG is supplied by StatsBomb, not trained by me.

## Content

The homepage links three case studies, the interactive demo, a public CV summary and selected essays. Original notebooks remain in separate repositories. The original private CV is not included; the downloadable public summary uses portfolio-verified professional facts and public links.

The site includes keyboard focus states, native labelled controls, exact-value tables, reduced-motion support, canonical/sharing metadata, a sitemap, favicon and custom 404 page. These checks are not a full assistive-technology audit.

## Hosting

GitHub Pages publishes the root from `main`. [Domain setup](docs/custom-domain.md) is prepared for after registration. No custom domain is active yet. Keep internal profile details and working data out of the deployment.
