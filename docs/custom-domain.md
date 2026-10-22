# Connect tolaadelase.com after registration

Status: the domain has not been purchased. No DNS or custom-domain setting has changed. Availability and price are not guaranteed. The site remains at <https://tola-adelase.github.io/>.

1. Register the domain in your own registrar account. Check the renewal price as well as the first-year price.
2. Verify ownership in your GitHub account's Pages settings using GitHub's account-specific TXT record.
3. In `Tola-adelase/Tola-adelase.github.io` → Settings → Pages, save `tolaadelase.com` as the custom domain **before** pointing DNS at GitHub.
4. Add these DNS records. Replace conflicting parking records while preserving unrelated email and verification entries.

| Type | Host | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | Tola-adelase.github.io |

5. Wait for DNS checks and the certificate, then enable Enforce HTTPS in Pages. Propagation can take up to 24 hours. Avoid wildcard DNS entries.
6. Check both apex and www hostnames, including case-study, demo and PDF paths.
7. Update canonical/OG URLs, sitemap, robots.txt and profile/README links to the verified custom domain.

Official reference: <https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site>. Recheck current guidance when configuring. No `CNAME` has been added to this repository yet.
